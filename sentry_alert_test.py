import os
import sentry_sdk

dsn = os.environ.get("SENTRY_DSN")

if not dsn:
    raise SystemExit("Ошибка: переменная SENTRY_DSN не задана")

sentry_sdk.init(
    dsn=dsn,
    send_default_pii=True,
    traces_sample_rate=0.0,
    environment="netology-alert-test",
    release="sentry-homework@1.0.1",
)

sentry_sdk.set_tag("homework", "16-sentry-alert")
sentry_sdk.set_tag("alert_test", "true")

try:
    data = {"project": "sentry-homework"}
    print(data["missing_key"])
except KeyError as error:
    sentry_sdk.capture_exception(error)

sentry_sdk.flush(timeout=5)

print("Sentry alert test event sent")
