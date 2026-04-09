use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use serde_json::json;
use std::env;

async fn health() -> impl Responder {
    HttpResponse::Ok().json(json!({"status": "healthy"}))
}

async fn index() -> impl Responder {
    HttpResponse::Ok().body("OK")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let port = port.parse::<u16>().unwrap_or(8080);
    
    println!("Rust server running on port {}", port);
    
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
            .route("/health", web::get().to(health))
    })
    .bind(("0.0.0.0", port))?
    .run()
    .await
}