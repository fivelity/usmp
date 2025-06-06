# Ultimate Sensor Monitor - Build & Deployment Commands

.PHONY: help build-backend build-frontend build-all test-backend test-frontend clean dev prod

help: ## Show this help message
	@echo "Ultimate Sensor Monitor - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Build Commands
build-backend: ## Build backend Docker image
	@echo "🐍 Building backend..."
	docker build -f server/Dockerfile -t ultimon-backend:latest .

build-frontend: ## Build frontend Docker image
	@echo "🎨 Building frontend..."
	docker build -f client/Dockerfile -t ultimon-frontend:latest ./client

build-all: ## Build both backend and frontend
	@echo "🚀 Building all services..."
	docker-compose build

# Test Build Commands
test-backend: ## Test backend build and run
	@echo "🧪 Testing backend build..."
	docker build -f server/Dockerfile -t ultimon-backend:test .
	docker run --rm -d --name ultimon-backend-test -p 8101:8100 ultimon-backend:test
	@echo "⏳ Waiting for backend to start..."
	@sleep 10
	@echo "🔍 Testing backend health..."
	curl -f http://localhost:8101/health && echo "✅ Backend test passed!" || echo "❌ Backend test failed!"
	docker stop ultimon-backend-test

test-frontend: ## Test frontend build
	@echo "🧪 Testing frontend build..."
	docker build -f client/Dockerfile -t ultimon-frontend:test ./client
	@echo "✅ Frontend build test passed!"

# Development Commands
dev: ## Start development environment
	@echo "🔧 Starting development environment..."
	docker-compose --profile development up -d

prod: ## Start production environment
	@echo "🚀 Starting production environment..."
	docker-compose --profile frontend up -d

backend-only: ## Start only backend service
	@echo "🐍 Starting backend only..."
	docker-compose up -d backend

# Utility Commands
clean: ## Clean up Docker images and containers
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f
	docker image prune -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

shell-backend: ## Open shell in backend container
	docker-compose exec backend bash

# Quick Commands
quick-test: build-all test-backend test-frontend ## Quick build and test all services

deploy: build-all ## Build and deploy all services
	@echo "🚀 Deploying Ultimate Sensor Monitor..."
	docker-compose --profile frontend up -d
	@echo "✅ Deployment complete!"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "🔧 Backend API: http://localhost:8100"
	@echo "📊 Health Check: http://localhost:8100/health"
