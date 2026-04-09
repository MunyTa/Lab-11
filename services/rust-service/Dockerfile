# Этап 1: Сборка с musl (используем Rust 1.90)
FROM rust:1.90-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app

COPY Cargo.toml Cargo.lock* ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release --target x86_64-unknown-linux-musl

COPY src ./src
RUN touch src/main.rs
RUN cargo build --release --target x86_64-unknown-linux-musl

# Этап 2: Финальный образ
FROM scratch

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/rust-service /rust-service

ENV PORT=8080

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["/rust-service", "healthcheck"]

CMD ["/rust-service"]