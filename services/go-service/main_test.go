package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
	"time"
)

func TestHealthEndpoint(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()

	router := setupRouter()

	router.ServeHTTP(w, req)

	res := w.Result()
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", res.StatusCode)
	}

	var response map[string]string
	if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
		t.Errorf("Expected JSON response, got error: %v", err)
	}

	if status, ok := response["status"]; !ok || status != "healthy" {
		t.Errorf("Expected status='healthy', got %v", response)
	}
}

func TestPortEnvVar(t *testing.T) {
	testPort := "9090"
	os.Setenv("PORT", testPort)
	defer os.Unsetenv("PORT")

	go main()

	time.Sleep(100 * time.Millisecond)

	resp, err := http.Get("http://localhost:" + testPort + "/health")
	if err != nil {
		t.Fatalf("Server not listening on port %s: %v", testPort, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected 200 OK, got %d", resp.StatusCode)
	}
}

func TestDefaultPort(t *testing.T) {
	os.Unsetenv("PORT")

	go main()

	time.Sleep(100 * time.Millisecond)

	resp, err := http.Get("http://localhost:8080/health")
	if err != nil {
		t.Fatalf("Server not listening on default port 8080: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected 200 OK, got %d", resp.StatusCode)
	}
}

func TestHealthcheckCommand(t *testing.T) {
	os.Setenv("PORT", "8080")
	defer os.Unsetenv("PORT")

	go main()
	time.Sleep(100 * time.Millisecond)

	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"server", "healthcheck"}

	resp, err := http.Get("http://localhost:8080/health")
	if err != nil {
		t.Fatalf("Healthcheck failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Healthcheck endpoint returned %d", resp.StatusCode)
	}
}
