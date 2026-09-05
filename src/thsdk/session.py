from __future__ import annotations

import atexit
import hashlib
import math
import os
import time
from pathlib import Path
from threading import RLock
from typing import Any

from ._qr_display import print_qr_challenge
from ._runtime import _RuntimeBridge
from .exceptions import APIError, AuthenticationError, NotAuthenticatedError


_ACCOUNT_MAC_SEED = b"thsdk-account-mac-v1\0"
_ENV_USERNAME = "THS_USERNAME"
_ENV_PASSWORD = "THS_PASSWORD"
_MAX_TIMEOUT_SECONDS = 600
_MIN_QR_POLL_SECONDS = 0.5
_MAX_QR_POLL_SECONDS = 30
_MAX_RATE_LIMIT_RETRY_MS = 1_000


def _validate_seconds(value: float, name: str, *, minimum: float, maximum: float) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < minimum
        or value > maximum
    ):
        raise ValueError(f"{name} 必须在 {minimum:g} 到 {maximum:g} 秒之间")
    return float(value)


def _timeout_milliseconds(value: float) -> int:
    return max(1, math.ceil(value * 1000))


def _derive_account_mac(username: str) -> str:
    """Map one account name to a stable, locally administered unicast MAC."""
    digest = hashlib.sha256(_ACCOUNT_MAC_SEED + username.encode("utf-8")).digest()
    octets = bytearray(digest[:6])
    octets[0] = (octets[0] & 0xFC) | 0x02
    return ":".join(f"{value:02x}" for value in octets)


def _environment_credentials() -> tuple[str, str] | None:
    username = os.getenv(_ENV_USERNAME)
    password = os.getenv(_ENV_PASSWORD)
    if username is None and password is None:
        return None
    if username is None or password is None or not username.strip() or not password:
        raise AuthenticationError(
            "环境变量 THS_USERNAME 和 THS_PASSWORD 必须同时设置且不能为空"
        )
    return username, password


class _Client:
    """Process-local owner of the single THSDK client.

    The default instance is created lazily so its session directory is the
    process working directory at the first THSDK call, not the package install
    directory. Authentication is deliberately explicit: data methods never
    restore a disk session behind the caller's back.
    """

    def __init__(self, session_dir: str | Path | None = None, runtime: _RuntimeBridge | Any | None = None):
        self.session_dir = Path(session_dir or Path.cwd()).expanduser().resolve()
        self._runtime = runtime
        self._state_lock = RLock()
        self._auth_lock = RLock()
        self._authenticated = False

    @property
    def runtime(self) -> _RuntimeBridge | Any:
        with self._state_lock:
            if self._runtime is None:
                self._runtime = _RuntimeBridge()
            return self._runtime

    @staticmethod
    def _error(response: dict[str, Any]) -> tuple[str, str, int | None]:
        value = response.get("error") or {}
        if not isinstance(value, dict):
            return "unknown_error", str(value), None
        retry_after = value.get("retry_after_ms")
        if isinstance(retry_after, bool) or not isinstance(retry_after, int) or retry_after <= 0:
            retry_after = None
        return (
            str(value.get("code") or "unknown_error"),
            str(value.get("message") or "unknown error"),
            retry_after,
        )

    def _invoke(self, method: str, params: Any = None, *, timeout_ms: int | None = None) -> Any:
        deadline = None if timeout_ms is None else time.monotonic() + timeout_ms / 1000
        call_timeout_ms = timeout_ms
        for attempt in range(2):
            response = self.runtime.call(method, params, timeout_ms=call_timeout_ms)
            if response.get("ok"):
                return response.get("data")
            code, message, retry_after_ms = self._error(response)
            can_retry = (
                attempt == 0
                and code == "rate_limited"
                and retry_after_ms is not None
                and retry_after_ms <= _MAX_RATE_LIMIT_RETRY_MS
            )
            if can_retry and deadline is not None:
                can_retry = time.monotonic() + retry_after_ms / 1000 < deadline
            if not can_retry:
                raise APIError(code, message, retry_after_ms=retry_after_ms)
            time.sleep(retry_after_ms / 1000)
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise APIError(code, message, retry_after_ms=retry_after_ms)
                call_timeout_ms = _timeout_milliseconds(remaining)
        raise AssertionError("unreachable")

    def auth(
        self,
        username: str | None = None,
        password: str | None = None,
        mac: str | None = None,
        *,
        timeout: float = 60,
    ) -> bool:
        """Authenticate from explicit, environment, session, or temporary credentials."""
        timeout = _validate_seconds(
            timeout,
            "timeout",
            minimum=1e-9,
            maximum=_MAX_TIMEOUT_SECONDS,
        )
        if (username is None) != (password is None):
            raise AuthenticationError("账号和密码必须同时提供")
        if username is not None and (not username.strip() or not password):
            raise AuthenticationError("账号和密码不能为空")
        if mac is not None and username is None:
            raise AuthenticationError("mac 只能与账号和密码同时提供")

        credentials: tuple[str, str, str | None] | None
        if username is not None:
            credentials = (username, password, mac)
        else:
            environment = _environment_credentials()
            credentials = None if environment is None else (*environment, None)

        deadline = time.monotonic() + timeout

        def authenticate(params: dict[str, Any]) -> bool:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise AuthenticationError("认证超时")
            data = self._invoke(
                "auth",
                params,
                timeout_ms=_timeout_milliseconds(remaining),
            ) or {}
            if not isinstance(data, dict) or not data.get("authenticated"):
                raise AuthenticationError("认证未完成")
            with self._state_lock:
                self._authenticated = True
            return True

        def account_params(values: tuple[str, str, str | None]) -> dict[str, Any]:
            account, secret, device = values
            return {
                "session_dir": str(self.session_dir),
                "username": account,
                "password": secret,
                "mac": device if device is not None else _derive_account_mac(account),
            }

        with self._auth_lock:
            if credentials is not None:
                try:
                    return authenticate(account_params(credentials))
                except APIError as exc:
                    raise AuthenticationError(str(exc)) from exc

            with self._state_lock:
                if self._authenticated:
                    return True

            session_params = {"session_dir": str(self.session_dir)}
            if (self.session_dir / "account.session").is_file():
                try:
                    return authenticate(session_params)
                except APIError as exc:
                    if exc.code != "session_unavailable":
                        raise AuthenticationError(str(exc)) from exc

            from ._temporary_accounts import acquire_temporary_account

            temporary_username, temporary_password, temporary_mac = (
                acquire_temporary_account()
            )
            try:
                return authenticate(
                    account_params(
                        (temporary_username, temporary_password, temporary_mac)
                    )
                )
            except APIError as exc:
                raise AuthenticationError(str(exc)) from exc
            finally:
                temporary_username = temporary_password = temporary_mac = None

    def auth_qrcode(
        self,
        *,
        timeout: float = 120,
        poll_interval: float = 1,
    ) -> bool:
        """Restore the local session first, otherwise complete one QR login job."""
        timeout = _validate_seconds(
            timeout,
            "timeout",
            minimum=1e-9,
            maximum=_MAX_TIMEOUT_SECONDS,
        )
        poll_interval = _validate_seconds(
            poll_interval,
            "poll_interval",
            minimum=_MIN_QR_POLL_SECONDS,
            maximum=_MAX_QR_POLL_SECONDS,
        )

        deadline = time.monotonic() + timeout
        start_params = {
            "session_dir": str(self.session_dir),
            "timeout_seconds": max(1, math.ceil(timeout)),
            "poll_interval_ms": _timeout_milliseconds(poll_interval),
        }
        with self._auth_lock:
            try:
                remaining_ms = _timeout_milliseconds(deadline - time.monotonic())
                state = self._invoke(
                    "auth_qrcode",
                    start_params,
                    timeout_ms=min(20_000, remaining_ms),
                ) or {}
            except APIError as exc:
                raise AuthenticationError(str(exc)) from exc

            if state.get("authenticated") or state.get("state") == "authenticated":
                with self._state_lock:
                    self._authenticated = True
                return True

            shown_challenge: tuple[str, str] | None = None

            def show_challenge(value: dict[str, Any]) -> None:
                nonlocal shown_challenge
                challenge = (str(value.get("scan_url") or ""), str(value.get("image_url") or ""))
                if challenge == ("", "") or challenge == shown_challenge:
                    return
                shown_challenge = challenge
                try:
                    print_qr_challenge(
                        value,
                        render_timeout=max(0.0, deadline - time.monotonic()),
                    )
                except Exception:
                    pass

            completed = False
            try:
                show_challenge(state)
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    state = self._invoke(
                        "auth_qrcode",
                        timeout_ms=_timeout_milliseconds(remaining),
                    ) or {}
                    show_challenge(state)
                    if state.get("authenticated") or state.get("state") == "authenticated":
                        with self._state_lock:
                            self._authenticated = True
                        completed = True
                        return True
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    time.sleep(min(max(0.1, poll_interval), remaining))
            except APIError as exc:
                raise AuthenticationError(str(exc)) from exc
            finally:
                if not completed:
                    try:
                        self._invoke("auth_qrcode", {"cancel": True})
                    except APIError:
                        pass
            raise AuthenticationError("二维码登录超时")

    def _request(self, method: str, params: Any = None, *, timeout: float | None = None) -> Any:
        """Execute one package-defined data request after explicit authentication."""
        with self._auth_lock:
            with self._state_lock:
                authenticated = self._authenticated
            if not authenticated:
                raise NotAuthenticatedError(
                    "尚未认证；请先调用 auth_qrcode() 或 auth(...)"
                )
            if timeout is not None:
                timeout = _validate_seconds(
                    timeout,
                    "timeout",
                    minimum=1e-9,
                    maximum=_MAX_TIMEOUT_SECONDS,
                )
            timeout_ms = None if timeout is None else _timeout_milliseconds(timeout)
            return self._invoke(method, params, timeout_ms=timeout_ms)

    def logout(self) -> None:
        with self._auth_lock:
            try:
                self._invoke("logout", {"session_dir": str(self.session_dir)})
            finally:
                with self._state_lock:
                    self._authenticated = False

    def _close(self) -> None:
        with self._auth_lock:
            try:
                self._invoke("_close")
            finally:
                with self._state_lock:
                    self._authenticated = False


_default_client: _Client | None = None
_default_client_lock = RLock()


def _get_client() -> _Client:
    global _default_client
    with _default_client_lock:
        if _default_client is None:
            _default_client = _Client()
        return _default_client


def _set_client_for_tests(client: _Client | None) -> None:
    """Replace the process client for isolated tests; never exported by the package."""
    global _default_client
    with _default_client_lock:
        _default_client = client


def _close_at_exit() -> None:
    with _default_client_lock:
        client = _default_client
    if client is None:
        return
    with client._state_lock:
        if client._runtime is None:
            return
    try:
        client._close()
    except Exception:
        pass


atexit.register(_close_at_exit)


__all__: list[str] = []
