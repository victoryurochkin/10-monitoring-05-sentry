# Домашнее задание к занятию 16 «Платформа мониторинга Sentry»

## Информация о стенде

Для выполнения домашнего задания использовался облачный сервис **Sentry Cloud Free account** и отдельная виртуальная машина **Debian 12** для запуска Python-проекта с подключённым Sentry SDK.

Виртуальная машина:

- ОС: `Debian 12`;
- Hostname: `sentry`;
- IP-адрес: `192.168.1.98`;
- директория проекта: `/opt/16-monitoring-04-sentry`.

Self-Hosted Sentry не устанавливался, так как для выполнения задания использовался облачный Free Cloud account.

---

## Задание 1. Создание аккаунта и проекта в Sentry

Был создан аккаунт Sentry Cloud с авторизацией через GitHub.

В Sentry был создан проект:

- платформа: `Python`;
- имя проекта: `python-sentry-lab`.

Скриншот меню Projects:

<!-- Вставить скриншот меню Projects с проектом python-sentry-lab -->

---

## Задание 2. Генерация события, изучение Stack Trace и перевод события в Resolved

В проекте `python-sentry-lab` было сгенерировано тестовое событие.

После генерации события был открыт список Issues, выбран issue `ZeroDivisionError: division by zero` и изучена информация по событию, включая Stack Trace.

Скриншот Stack Trace:

<!-- Вставить скриншот Stack Trace события ZeroDivisionError -->

После изучения событие было переведено в статус `Resolved`.

Скриншот списка Issues после перевода события в `Resolved`:

<!-- Вставить скриншот Issues с фильтром is:resolved -->

---

## Задание 3. Настройка правила алёртинга

В Sentry было создано дефолтное правило алёртинга для проекта `python-sentry-lab`.

Параметры правила:

- источник: все Issues выбранного проекта;
- проект: `python-sentry-lab`;
- окружения: `All Environments`;
- условие: новое issue или изменение состояния issue;
- фильтр: `Any event`;
- действие: уведомить suggested assignees, а если они не найдены — всех участников проекта.

После создания правила было сгенерировано новое событие `KeyError: 'missing_key'`.

Алёрт сработал, после чего на почту, привязанную к аккаунту Sentry/GitHub, пришло уведомление.

Скриншот письма-оповещения:

<!-- Вставить скриншот письма от Sentry -->

---

## Задание повышенной сложности. Python-проект с sentry-sdk

На виртуальной машине Debian 12 был создан Python-проект, подключён `sentry-sdk` и отправлены тестовые события в Sentry.

### Структура проекта

```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── sentry_alert_test.py
└── sentry_test.py
```

### Установка зависимостей

```bash
apt update
apt install -y python3 python3-venv python3-pip git tree

mkdir -p /opt/16-monitoring-04-sentry
cd /opt/16-monitoring-04-sentry

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install "sentry-sdk"
pip freeze > requirements.txt
```

### Переменная окружения

DSN был взят из настроек проекта Sentry.

Для безопасного хранения DSN использовался файл `.env`:

```bash
SENTRY_DSN="https://examplePublicKey@o000000.ingest.sentry.io/000000"
```

Файл `.env` не добавляется в GitHub, так как указан в `.gitignore`.

### Файл .gitignore

```gitignore
venv/
.env
__pycache__/
*.pyc
```

### Код sentry_test.py

```python
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
```

### Код sentry_alert_test.py

```python
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
```

### Запуск первого теста

```bash
cd /opt/16-monitoring-04-sentry
source venv/bin/activate

set -a
source .env
set +a

python3 sentry_test.py
```

Результат выполнения:

```text
Sentry test events sent
```

После запуска в Sentry появились события:

- `ZeroDivisionError: division by zero`;
- `Netology Sentry test message`.

Скриншот Issues после отправки событий через Python SDK:

<!-- Вставить скриншот Issues со списком ZeroDivisionError и Netology Sentry test message -->

### Запуск теста для проверки алёрта

```bash
cd /opt/16-monitoring-04-sentry
source venv/bin/activate

set -a
source .env
set +a

python3 sentry_alert_test.py
```

Результат выполнения:

```text
Sentry alert test event sent
```

После запуска в Sentry появилось событие:

- `KeyError: 'missing_key'`.

На созданное issue сработало правило алёртинга.

---

## Вывод

В ходе выполнения домашнего задания был создан проект в Sentry Cloud, сгенерированы тестовые события, изучен Stack Trace, выполнен перевод события в статус `Resolved`, настроено правило алёртинга с email-уведомлением, а также реализован Python-проект с подключением `sentry-sdk` и отправкой тестовых событий в Sentry.
