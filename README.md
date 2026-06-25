# Домашнее задание к занятию 16 «Платформа мониторинга Sentry» - Юрочкин В.А.

## Информация о стенде

Для выполнения домашнего задания использовался облачный сервис **Sentry Cloud Free account** и отдельная виртуальная машина **Debian 12** (на своём сервере) для запуска Python-проекта с подключённым Sentry SDK.

<img width="3071" height="1749" alt="image" src="https://github.com/user-attachments/assets/35bf8e2b-3688-403b-8777-d3e54948b9be" />


<img width="3071" height="1347" alt="image" src="https://github.com/user-attachments/assets/c52e018e-99e8-40f2-b0a7-4317a8374ffb" />


Виртуальная машина:

- ОС: `Debian 12`;
- Hostname: `sentry`;
- IP-адрес: `192.168.1.98`;
- директория проекта: `/opt/16-monitoring-04-sentry`.

<img width="2557" height="1157" alt="image" src="https://github.com/user-attachments/assets/2c285b29-be70-4b11-aabc-84008ee94617" />


Self-Hosted Sentry не устанавливался, так как для выполнения задания использовался облачный Free Cloud account.

---

## Задание 1. Создание аккаунта и проекта в Sentry

Был создан аккаунт Sentry Cloud с авторизацией через GitHub.

В Sentry был создан проект:

- платформа: `Python`;
- имя проекта: `python-sentry-lab`.

<img width="3071" height="858" alt="image" src="https://github.com/user-attachments/assets/6e7373cd-902c-48ed-bd54-e0ff541b8e7a" />


---

## Задание 2. Генерация события, изучение Stack Trace и перевод события в Resolved

В проекте `python-sentry-lab` было сгенерировано тестовое событие.

После генерации события был открыт список Issues, выбран issue `ZeroDivisionError: division by zero` и изучена информация по событию, включая Stack Trace.


<img width="2048" height="712" alt="image" src="https://github.com/user-attachments/assets/cd09865f-b353-440f-a1fe-348334547b12" />


<img width="2048" height="1167" alt="image" src="https://github.com/user-attachments/assets/354e5278-d56c-467e-8b66-f833e4e6d59c" />


После изучения событие было переведено в статус `Resolved`.

<img width="2048" height="1164" alt="image" src="https://github.com/user-attachments/assets/8aacbd3c-8507-4e42-a43d-c9744c8d7849" />

<img width="2048" height="708" alt="image" src="https://github.com/user-attachments/assets/c01a8280-4495-4013-9b9b-e3c9ad0af4e2" />


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


<img width="2048" height="1602" alt="image" src="https://github.com/user-attachments/assets/e1a76b48-67f4-46ab-a928-66682df34622" />


После создания правила было сгенерировано новое событие `KeyError: 'missing_key'`.

<img width="2048" height="1157" alt="image" src="https://github.com/user-attachments/assets/85ab245f-4492-4057-b7e4-2a622e4cfcf7" />


Алёрт сработал, после чего на почту, привязанную к аккаунту Sentry/GitHub, пришло уведомление.

<img width="1937" height="1727" alt="image" src="https://github.com/user-attachments/assets/fae3aafd-5997-4808-bb52-7c918a172675" />


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

<img width="1542" height="340" alt="image" src="https://github.com/user-attachments/assets/2205a508-87f5-4615-ae6b-3eac99db603a" />


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

<img width="2048" height="1161" alt="image" src="https://github.com/user-attachments/assets/15bb1a87-779c-4d05-8d42-6296fe0e42d6" />

<img width="3071" height="1745" alt="image" src="https://github.com/user-attachments/assets/aeb011ac-3267-4f46-964d-05d38bb99aec" />

<img width="2532" height="1738" alt="image" src="https://github.com/user-attachments/assets/037d1ce7-1b38-4f68-afb0-bc19a1c695a9" />


---

## Вывод

В ходе выполнения домашнего задания был создан проект в Sentry Cloud, сгенерированы тестовые события, изучен Stack Trace, выполнен перевод события в статус `Resolved`, настроено правило алёртинга с email-уведомлением, а также реализован Python-проект с подключением `sentry-sdk` и отправкой тестовых событий в Sentry.
