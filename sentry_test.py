import os
import sentry_sdk

dsn = os.environ.get("SENTRY_DSN")

if not dsn:
    raise SystemExit("Ошибка: переменная SENTRY_DSN не задана")

sentry_sdk.init(
    dsn=dsn,
    send_default_pii=True,
    traces_sample_rate=0.0,
    environment="netology-lab",
    release="sentry-homework@1.0.0",
)

sentry_sdk.set_tag("homework", "16-sentry")
sentry_sdk.set_tag("vm_os", "Debian 12")
sentry_sdk.set_context("virtual_machine", {
    "hostname": "sentry",
    "ip": "192.168.1.98",
})

sentry_sdk.capture_message("Netology Sentry test message", level="warning")

try:
    division_by_zero = 1 / 0
except ZeroDivisionError as error:
    sentry_sdk.capture_exception(error)

sentry_sdk.flush(timeout=5)

print("Sentry test events sent")
