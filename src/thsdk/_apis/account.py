from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from typing import Any

from ._base import (
    BlockInput,
    ObjectParams,
    SecurityInput,
    _call_none,
    _call_securities,
    _call_string,
    _call_typed,
)


def account_permissions(*, timeout: float | None = None) -> Any:
    """调用原生 ``AccountPermissions``，返回 ``AccountPermissions``。"""

    return _call_none("account_permissions", timeout=timeout)


def add_account_watchlist_group_securities(
    params: ObjectParams | None = None,
    *,
    group_id: int | None = None,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``AddAccountWatchlistGroupSecurities``；请求 ``AccountWatchlistGroupSecuritiesRequest``，返回 ``AccountWatchlistGroups``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "add_account_watchlist_group_securities",
        params,
        {
            "group_id": group_id,
            "securities": securities,
        },
        required=("group_id", "securities"),
        timeout=timeout,
    )


def add_account_watchlist_securities(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    add_to_front: bool | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``AddAccountWatchlistSecurities``；请求 ``AddAccountWatchlistSecuritiesRequest``，返回 ``AccountWatchlistUpdate``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "add_account_watchlist_securities",
        params,
        {
            "securities": securities,
            "add_to_front": add_to_front,
        },
        required=("securities",),
        timeout=timeout,
    )


def clear_account_watchlist(*, timeout: float | None = None) -> Any:
    """调用原生 ``ClearAccountWatchlist``，返回 ``AccountWatchlistUpdate``。 会修改当前账号的远端数据。"""

    return _call_none("clear_account_watchlist", timeout=timeout)


def create_account_watchlist_group(
    params: ObjectParams | None = None,
    *,
    name: str | None = None,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``CreateAccountWatchlistGroup``；请求 ``CreateAccountWatchlistGroupRequest``，返回 ``AccountWatchlistGroups``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "create_account_watchlist_group",
        params,
        {
            "name": name,
            "securities": securities,
        },
        required=("name",),
        timeout=timeout,
    )


def delete_account_watchlist_group(
    params: ObjectParams | None = None,
    *,
    group_id: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``DeleteAccountWatchlistGroup``；请求 ``DeleteAccountWatchlistGroupRequest``，返回 ``AccountWatchlistGroups``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "delete_account_watchlist_group",
        params,
        {
            "group_id": group_id,
        },
        required=("group_id",),
        timeout=timeout,
    )


def get_account_watchlist(*, timeout: float | None = None) -> Any:
    """调用原生 ``GetAccountWatchlist``，返回 ``AccountWatchlistSnapshot``。"""

    return _call_none("get_account_watchlist", timeout=timeout)


def get_account_watchlist_groups(*, timeout: float | None = None) -> Any:
    """调用原生 ``GetAccountWatchlistGroups``，返回 ``AccountWatchlistGroups``。"""

    return _call_none("get_account_watchlist_groups", timeout=timeout)


def remove_account_watchlist_group_securities(
    params: ObjectParams | None = None,
    *,
    group_id: int | None = None,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``RemoveAccountWatchlistGroupSecurities``；请求 ``AccountWatchlistGroupSecuritiesRequest``，返回 ``AccountWatchlistGroups``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "remove_account_watchlist_group_securities",
        params,
        {
            "group_id": group_id,
            "securities": securities,
        },
        required=("group_id", "securities"),
        timeout=timeout,
    )


def remove_account_watchlist_securities(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``RemoveAccountWatchlistSecurities``；请求 ``RemoveAccountWatchlistSecuritiesRequest``，返回 ``AccountWatchlistUpdate``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "remove_account_watchlist_securities",
        params,
        {
            "securities": securities,
        },
        required=("securities",),
        timeout=timeout,
    )


def rename_account_watchlist_group(
    params: ObjectParams | None = None,
    *,
    group_id: int | None = None,
    name: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``RenameAccountWatchlistGroup``；请求 ``RenameAccountWatchlistGroupRequest``，返回 ``AccountWatchlistGroups``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "rename_account_watchlist_group",
        params,
        {
            "group_id": group_id,
            "name": name,
        },
        required=("group_id", "name"),
        timeout=timeout,
    )


def replace_account_watchlist_group_securities(
    params: ObjectParams | None = None,
    *,
    group_id: int | None = None,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ReplaceAccountWatchlistGroupSecurities``；请求 ``AccountWatchlistGroupSecuritiesRequest``，返回 ``AccountWatchlistGroups``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "replace_account_watchlist_group_securities",
        params,
        {
            "group_id": group_id,
            "securities": securities,
        },
        required=("group_id", "securities"),
        timeout=timeout,
    )


def replace_account_watchlist_securities(
    params: ObjectParams | None = None,
    *,
    version: int | None = None,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ReplaceAccountWatchlistSecurities``；请求 ``ReplaceAccountWatchlistSecuritiesRequest``，返回 ``AccountWatchlistUpdate``。 会修改当前账号的远端数据。"""

    return _call_typed(
        "replace_account_watchlist_securities",
        params,
        {
            "version": version,
            "securities": securities,
        },
        required=("version", "securities"),
        timeout=timeout,
    )


__all__ = [
    "account_permissions",
    "add_account_watchlist_group_securities",
    "add_account_watchlist_securities",
    "clear_account_watchlist",
    "create_account_watchlist_group",
    "delete_account_watchlist_group",
    "get_account_watchlist",
    "get_account_watchlist_groups",
    "remove_account_watchlist_group_securities",
    "remove_account_watchlist_securities",
    "rename_account_watchlist_group",
    "replace_account_watchlist_group_securities",
    "replace_account_watchlist_securities",
]

