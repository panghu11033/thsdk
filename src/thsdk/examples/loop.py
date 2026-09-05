"""紧密调用同一接口，观察运行组件的 50ms 限频。"""

import time

import thsdk


CALLS = 100
# 短于 50ms 限频窗口，使 SDK 无法在本次 deadline 内等待并自动重试，
# 从而把 rate_limited 和 retry_after_ms 暴露给示例。
TIMEOUT_SECONDS = 0.001

thsdk.auth()
# 先占用一次 account_permissions 的调用窗口；它只读取本地权限快照。
thsdk.account_permissions()

succeeded = 0
limited = 0
rate_limit_message = ""
events: list[str] = []
for index in range(1, CALLS + 1):
    started_at = time.perf_counter()
    try:
        result = thsdk.account_permissions()
    except thsdk.APIError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        if exc.code != "rate_limited":
            raise
        limited += 1
        rate_limit_message = exc.message
        events.append(
            f"第 {index:03d} 次：限频，耗时 {elapsed_ms:.3f} ms，"
            f"retry_after_ms={exc.retry_after_ms}"
        )
    else:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        succeeded += 1
        events.append(f"第 {index:03d} 次：成功，耗时 {elapsed_ms:.3f} ms")

print("\n".join(events))
print(f"完成：成功 {succeeded} 次，限频 {limited} 次，共 {CALLS} 次")
if limited:
    print(f"限频消息：{rate_limit_message}")
else:
    print("未观察到显式限频：当前环境中的单次调用可能已超过 50ms。")
