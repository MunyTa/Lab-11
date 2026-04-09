# Этап 1: Сборка бинарника
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Копируем go.mod (у вас его пока нет, создадим)
COPY go.mod go.sum* ./
RUN if [ -f go.mod ]; then go mod download; fi

# Копируем исходники и собираем
COPY *.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server .

# Этап 2: Финальный минимальный образ
FROM scratch

# Копируем бинарник из builder
COPY --from=builder /app/server /server

# Указываем порт
EXPOSE 8080

# Переменные окружения
ENV PORT=8080

# Healthcheck (используем встроенную команду)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["/server", "healthcheck"]

# Запуск
CMD ["/server"]