# LR-11

## Лабораторная работа №11: Контейнеризация мультиязычных приложений

**Автор:** Кузьмищев Родион Ильич  
**Группа:** 221331  
**Вариант:** 8

---

## Журнал промптов (PROMPT_LOG)

### Методология: Agentic Engineering

Этот журнал документирует все шаги разработки лабораторной работы №11 с использованием итеративного подхода: планирование → код → тесты → рефакторинг → коммит.

---

## Этап 1: Go-сервис

### Prompt 1.1 (🔴 RED)
**Промпт:** "Напиши тесты для Go-сервиса: проверка эндпоинта `/health` (JSON, статус 200) и поддержки переменной окружения `PORT` (дефолт 8080). Тесты должны падать."

**Результат:** 
- Создан `main_test.go` с тестами `TestHealthEndpoint`, `TestPortEnvVar`, `TestDefaultPort`.
- Запуск `go test -v` показал FAIL.
- **Коммит:** `a58a074 test(go): add failing tests for health endpoint - RED`

### Prompt 1.2 (🟢 GREEN)
**Промпт:** "Реализуй минимальный код Go-сервера, чтобы тесты прошли. Нужны эндпоинты `/health` (JSON `{"status":"healthy"}`) и `/` ("OK"), чтение `PORT` из окружения."

**Результат:**
- Написан `main.go` с `setupRouter()` и обработчиками.
- Тесты пройдены (`go test -v`).
- **Коммит:** `f692651 feet(go): implement health endpoint with JSON response - GREEN`

### Prompt 1.3 (🐳 Docker)
**Промпт:** "Напиши многоэтапный Dockerfile для Go: `builder` на `golang:1.22-alpine`, финальный образ на `scratch`. Отключи CGO, скопируй только бинарник. Добавь `HEALTHCHECK` с вызовом `/server healthcheck` и переменную `PORT`."

**Результат:**
- Создан `Dockerfile` (multi-stage: `golang:1.22-alpine` → `scratch`).
- `CGO_ENABLED=0`, флаги `-ldflags="-w -s"`.
- В код добавлена обработка аргумента `healthcheck`.
- Разбор образа: `7.76MB`.
- **Коммит:** `0cfbd82 docker(go): add multi-stage Dockerfile with scratch and healthcheck`

---

## Этап 2: Python-сервис

### Prompt 2.1 (🔴 RED)
**Промпт:** "Напиши тесты для Python-сервиса (FastAPI) на эндпоинты `/health` и `/`, проверку `PORT` из окружения. Тесты должны падать."

**Результат:**
- Создан `test_app.py` с использованием `pytest` и `httpx`.
- **Коммит:** `0b25b6e test(python): add failing tests for health endpoint - RED`

### Prompt 2.2 (🟢 GREEN)
**Промпт:** "Реализуй FastAPI-приложение, проходящее тесты. Добавь `/health` (JSON), `/` ("OK"), чтение `PORT` и `DEBUG`."

**Результат:**
- Написан `app.py` на FastAPI с `uvicorn`.
- Тесты пройдены.
- **Коммит:** `b13abdb feet(python): implement health endpoint with JSON response - GREEN`

### Prompt 2.3 (🐳 Docker)
**Промпт:** "Создай Dockerfile для Python с оптимизацией: используй slim-образ, многоэтапную сборку для кэширования зависимостей, `HEALTHCHECK` через `curl` или Python."

**Результат:**
- Создан `Dockerfile` на основе `python:3.14-slim`.
- `HEALTHCHECK` через `python -c "import urllib.request..."`.
- Размер образа: `207MB`.
- **Коммит:** `ba4b324 docker(python): add Docker for Python service`

---

## Этап 3: Docker Compose (Go + Python)

### Prompt 3.1 (🚀 Compose)
**Промпт:** "Напиши `docker-compose.yml`, объединяющий Go и Python сервисы. Добавь общую сеть, проброс портов из `.env`, `healthcheck` из Dockerfile."

**Результат:**
- Создан `docker-compose.yml` с сервисами `go-service`, `python-service`.
- Добавлен `.env.example` с переменными `GO_PORT`, `PYTHON_PORT`, `DEBUG`.
- **Коммит:** `469edec chore(docker): add docker-compose with healthcheck for Go and Python services`

---

## Этап 4: Повышенная сложность (Rust + Watchtower)

### Prompt 4.1 (🦀 Rust)
**Промпт:** "Собери Rust-приложение с `actix-web`. Нужна полностью статическая сборка с `musl`. Финальный образ — `alpine` (для `curl` в `HEALTHCHECK`). Размер образа должен быть минимальным."

**Результат:**
- Создана структура `rust-service` с `Cargo.toml` и `src/main.rs`.
- `Dockerfile`: `rust:1.85-alpine` → сборка на `x86_64-unknown-linux-musl` → финальный `alpine:latest`.
- `HEALTHCHECK` через `curl -f http://localhost:$PORT/health`.
- Размер образа: `3.76MB`.
- **Коммит:** `8a286e7 feet(rust): add a Rust service with actix-web and static assembly of musl`

### Prompt 4.2 (🔧 Watchtower)
**Промпт:** "Добавь в `docker-compose.yml` сервис `watchtower` для автоматического обновления контейнеров. Нужен интервал проверки 60 секунд, автоочистка образов. Добавь `rust-service` в оркестрацию."

**Результат:**
- Обновлён `docker-compose.yml`: добавлены `rust-service` и `watchtower`.
- Watchtower использует `DOCKER_API_VERSION=1.40` для совместимости.
- **Коммит:** `9478a58 feet(docker-compose): add rust-service and watchtower`

### Prompt 4.3 (⚙️ Env)
**Промпт:** "Добавь переменные для Rust-сервиса в `.env` и `.env.example`."

**Результат:**
- Добавлена `RUST_PORT=8081`.
- **Коммит:** `8f3d452 chore(env): add variables for the Rust service`

---

## Этап 5: Документирование и завершение

### Prompt 5.1 (📄 README)
**Промпт:** "Создай подробный `README.md` с описанием проекта, инструкцией по запуску, результатами оптимизации и таблицей размеров образов."

**Результат:**
- Создан `README.md` с полным описанием лабораторной работы.
- **Коммит:** `docs: add comprehensive README.md`

### Prompt 5.2 (🚫 .gitignore)
**Промпт:** "Добавь `.gitignore`, чтобы исключить временные файлы, `.env`, `__pycache__`, `target/` и т.д."

**Результат:**
- Создан `.gitignore` для Python, Go, Rust, IDE и ОС.
- **Коммит:** `chore: add .gitignore`

---

## Итоги

**Общее количество промптов/итераций:** 13  
**Git-коммитов:** 13  

**Результаты:**
- Go-сервис: Dockerfile (multi-stage, scratch), размер **7.76 MB**.
- Python-сервис: Dockerfile (slim), размер **207 MB**.
- Rust-сервис: Dockerfile (musl, alpine), размер **3.76 MB**.
- Watchtower: автоматическое обновление контейнеров.
- Все сервисы имеют `HEALTHCHECK` и используют переменные окружения.

**Репозиторий:** [https://github.com/MunyTa/Lab-11](https://github.com/MunyTa/Lab-11)