# Ultimate Sensor Monitor - Developer Guide (Version 2.0.0 - Svelte 5 Edition)

This guide provides information for developers looking to contribute to Ultimate Sensor Monitor, understand its architecture, or build custom integrations. It emphasizes adherence to the project's **Svelte 5** technology stack.

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Project Architecture](#2-project-architecture)
*   [2.1. Backend (FastAPI, Python)](#21-backend-fastapi-python)
*   [2.2. Frontend (Svelte 5, TypeScript)](#22-frontend-svelte-5-typescript)
*   [2.3. Real-time Communication (WebSockets)](#23-real-time-communication-websockets)
3.  [Development Setup](#3-development-setup)
*   [3.1. Prerequisites](#31-prerequisites)
*   [3.2. Installation](#32-installation)
*   [3.3. Running the Application](#33-running-the-application)
4.  [Coding Standards and Practices](#4-coding-standards-and-practices)
*   [4.1. General](#41-general)
*   [4.2. Python (Backend)](#42-python-backend)
*   [4.3. TypeScript/Svelte 5 (Frontend)](#43-typescriptsvelte-5-frontend)
*   [4.4. Version Control (Git)](#44-version-control-git)
5.  [Backend Development](#5-backend-development)
*   [5.1. Directory Structure](#51-directory-structure)
*   [5.2. Adding New Sensor Modules](#52-adding-new-sensor-modules)
*   [5.3. API Endpoint Development](#53-api-endpoint-development)
*   [5.4. WebSocket Event Handling](#54-websocket-event-handling)
6.  [Frontend Development (Svelte 5)](#6-frontend-development-svelte-5)
*   [6.1. Directory Structure](#61-directory-structure)
*   [6.2. Svelte 5 Core Concepts (Runes)](#62-svelte-5-core-concepts-runes)
*   [6.3. State Management (Svelte 5 Runes & Stores)](#63-state-management-svelte-5-runes--stores)
*   [6.4. Creating New Components](#64-creating-new-components)
*   [6.5. Custom Widget Development (Svelte 5)](#65-custom-widget-development-svelte-5)
*   [6.6. Styling with Tailwind CSS](#66-styling-with-tailwind-css)
7.  [Testing](#7-testing)
*   [7.1. Backend Tests (pytest)](#71-backend-tests-pytest)
*   [7.2. Frontend Tests (Vitest)](#72-frontend-tests-vitest)
*   [7.3. End-to-End Tests (Playwright - if configured)](#73-end-to-end-tests-playwright---if-configured)
8.  [Building for Production](#8-building-for-production)
9.  [Docker and CI/CD](#9-docker-and-cicd)
10. [Contributing](#10-contributing)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Introduction

Version 2.0.0 of Ultimate Sensor Monitor marks a significant architectural upgrade, focusing on stability, scalability, security, and developer experience. This guide is tailored for development using **Svelte 5** for the frontend, leveraging its new Rune-based reactivity model.

## 2. Project Architecture

The application is divided into two main parts: a Python-based backend and a Svelte 5-based frontend.

### 2.1. Backend (FastAPI, Python)

-   **Framework**: FastAPI for high-performance asynchronous API endpoints.
-   **Sensor Integration**: Modular system for integrating various hardware monitoring libraries (e.g., `LibreHardwareMonitor`). See `server/app/sensors/`.
-   **Data Models**: Pydantic models for data validation and serialization.
-   **Configuration**: Environment-based configuration using `python-dotenv` and Pydantic settings.
-   **Logging**: Structured logging for better traceability.

### 2.2. Frontend (Svelte 5, TypeScript)

-   **Framework**: Svelte 5.x.x. This project **utilizes Svelte 5 features, primarily Runes (`$state`, `$derived`, `$props`, `$effect`)** for reactivity and state management.
-   **Language**: TypeScript for type safety.
-   **Styling**: Tailwind CSS for utility-first styling.
-   **Build Tool**: Vite for fast development and optimized builds.
-   **State Management**: Svelte 5 Runes for component-local state and derived computations. Svelte stores (`writable`, `readable`, `derived`) can still be used for global or cross-component state where appropriate. Global stores are located in `client/src/lib/stores/`.
-   **Component Architecture**: Modular components, with UI elements in `client/src/lib/components/ui/` and feature-specific components elsewhere.

### 2.3. Real-time Communication (WebSockets)

-   The backend exposes a WebSocket endpoint (`/ws`) for broadcasting real-time sensor data.
-   The frontend establishes a WebSocket connection to receive live updates. See `client/src/lib/services/websocket.ts` and `server/app/websockets.py`.

## 3. Development Setup

### 3.1. Prerequisites
-   Python 3.9+
-   Node.js 18+
-   pnpm (recommended) or npm
-   Git

### 3.2. Installation
1.  **Clone the repository:**
\`\`\`bash
git clone <repository-url>
cd UltimateSensorMonitor
\`\`\`
2.  **Install All Workspace Dependencies (Root Directory):**
\`\`\`bash
# From the UltimateSensorMonitor root directory
pnpm install
\`\`\`
3.  **Backend Python Dependencies:**
\`\`\`bash
cd server
pip install -r requirements.txt
cd ..
\`\`\`
4.  **Environment Variables:**
Create `.env` files in `client/` and `server/` directories based on the `.env.example` files. Adjust URLs and ports as necessary.

### 3.3. Running the Application
-   **Windows Launchers**: Use `start_ultimon_full.bat` or `start_ultimon_quick.bat`.
-   **Manual Start**:
1.  **Start Backend Server:**
    \`\`\`bash
    cd server
    python -m app.main 
    # Or: uvicorn app.main:app --reload --port 8000 
    \`\`\`
2.  **Start Frontend Dev Server:**
    \`\`\`bash
    cd client
    pnpm dev # or npm run dev
    \`\`\`
The application should be available at `http://localhost:5173` (frontend) and `http://localhost:8000` (backend).

## 4. Coding Standards and Practices

### 4.1. General
-   Follow a consistent code style (formatting, naming conventions).
-   Write clear, concise, and well-commented code where logic is not immediately obvious.

### 4.2. Python (Backend)
-   Follow PEP 8 guidelines.
-   Use type hints extensively.
-   Utilize asynchronous programming (`async/await`) for I/O-bound operations.

### 4.3. TypeScript/Svelte 5 (Frontend)
-   **Strictly adhere to the [Svelte 5 Standards](SVELTE_STANDARDS.md) document.** This is mandatory.
-   Utilize Svelte 5 Runes (`$state`, `$derived`, `$props`, `$effect`) for component state, derived data, props, and side effects.
-   Use TypeScript for all Svelte script blocks (`<script lang="ts">`).
-   Define types in `client/src/lib/types/`.
-   Event handling should use the Svelte 5 syntax (e.g., `onclick={handler}`).

### 4.4. Version Control (Git)
-   Follow conventional commit messages (e.g., `feat: add new widget`, `fix: resolve sensor display bug`).
-   Create feature branches for new development (`feature/my-new-feature`).
-   Submit pull requests for review before merging to main branches.

## 5. Backend Development

### 5.1. Directory Structure (Server)
\`\`\`
server/
├── app/
│   ├── main.py         # FastAPI application entry point
│   ├── core/           # Core components (config, logging, security)
│   ├── models/         # Pydantic data models
│   ├── sensors/        # Hardware sensor integration modules
│   ├── api/            # API route definitions (if separated)
│   └── websockets.py   # WebSocket handling logic
├── tests/              # Pytest tests
├── .env.example
├── requirements.txt
└── ...
\`\`\`

### 5.2. Adding New Sensor Modules
1.  Create a new Python module in `server/app/sensors/`.
2.  Implement the sensor logic, adhering to any base sensor class or interface defined.
3.  Register the new sensor source in the main application logic so it's discovered and data is collected.
4.  Update Pydantic models and API responses if necessary.

### 5.3. API Endpoint Development
-   Define API routes in `app/main.py` or dedicated router files.
-   Use Pydantic models for request body validation and response serialization.
-   Follow RESTful principles.

### 5.4. WebSocket Event Handling
-   Modify `server/app/websockets.py` to handle new message types or broadcast different data.
-   Ensure WebSocket messages conform to defined Pydantic models.

## 6. Frontend Development (Svelte 5)

### 6.1. Directory Structure (Client)
\`\`\`
client/
├── src/
│   ├── app.html          # Main HTML template
│   ├── app.d.ts          # Global TypeScript declarations for SvelteKit
│   ├── app.css           # Global styles (Tailwind base)
│   ├── hooks.server.ts   # SvelteKit server hooks (if any)
│   ├── lib/
│   │   ├── components/   # Reusable Svelte components (ui/, widgets/, etc.)
│   │   ├── stores/       # Svelte stores (for global/cross-component state)
│   │   ├── services/     # API clients, WebSocket service
│   │   ├── types/        # TypeScript type definitions
│   │   └── utils/        # Utility functions
│   ├── routes/           # SvelteKit file-based routing
│   └── service-worker.ts # (If PWA features are used)
├── static/               # Static assets (images, fonts)
├── tests/                # Vitest tests
├── vite.config.ts
├── svelte.config.js
├── tsconfig.json
├── postcss.config.js
├── tailwind.config.js
├── package.json
└── pnpm-lock.yaml (or package-lock.json)
\`\`\`

### 6.2. Svelte 5 Core Concepts (Runes)
-   **State**: `let count = $state(0);`
-   **Derived State**: `const doubled = $derived(count * 2);`
-   **Props**: `let { title, description = 'Default' } = $props();`
-   **Effects**: `$effect(() => { console.log(count); });`
-   **Event Handling**: `onclick={handler}` or `on:eventname={handler}` (Svelte 5 allows both, prefer `onclick` for simplicity where appropriate, but `on:` is still valid and sometimes necessary for custom events or modifiers).
-   **Bindings**: `bind:value` remains, but `$bindable()` can be used for props intended to be two-way bound from parent.
-   Refer to the [Svelte 5 Standards](SVELTE_STANDARDS.md) for detailed examples and rules.

### 6.3. State Management (Svelte 5 Runes & Stores)
-   Prioritize Svelte 5 Runes (`$state`, `$derived`) for component-local and intra-component reactive state.
-   Use Svelte stores (`writable`, `readable`, `derived` from `svelte/store`) for state that needs to be shared across multiple, unrelated components or for complex global state.
-   Organize global stores logically in `client/src/lib/stores/`.

### 6.4. Creating New Components
1.  Create a `.svelte` file (e.g., `MyWidget.svelte`) in the appropriate `lib/components/` subdirectory.
2.  Use `<script lang="ts">` for component logic.
3.  Define props using `let {...} = $props();`.
4.  Implement template and scoped styles (if not solely using Tailwind).
5.  Ensure adherence to Svelte 5 syntax and Runes.

### 6.5. Custom Widget Development (Svelte 5)
For detailed instructions on creating new widget types using Svelte 5, refer to the [Custom Widget Development Guide (Svelte 5)](CUSTOM_WIDGET_DEVELOPMENT.md). This guide has been updated to reflect Svelte 5 practices.

### 6.6. Styling with Tailwind CSS
-   Primarily use Tailwind utility classes in your Svelte templates.
-   Configure `tailwind.config.js` for custom themes, colors, and plugins.
-   Use `@apply` in `<style>` blocks sparingly for complex component-specific styles not easily achieved with utilities.

## 7. Testing

### 7.1. Backend Tests (pytest)
-   Write tests for API endpoints, sensor logic, and utility functions.
-   Place tests in the `server/tests/` directory.
-   Run with `cd server && pytest`.

### 7.2. Frontend Tests (Vitest)
-   Write unit tests for Svelte components, stores, and utility functions, considering the new Rune-based reactivity.
-   Place tests typically alongside the files they test (e.g., `MyComponent.test.ts`) or in a `client/tests/` directory.
-   Run with `cd client && pnpm test` (or `npm test`).

### 7.3. End-to-End Tests (Playwright - if configured)
-   If E2E tests are set up (e.g., using Playwright), write tests to cover critical user flows.
-   Run with the configured E2E test command (e.g., `pnpm test:e2e`).

## 8. Building for Production

-   **Frontend**: `cd client && pnpm build` (This will use Vite to create an optimized static build in `client/dist` or `client/.svelte-kit/output` depending on SvelteKit adapter).
-   **Backend**: The Python backend is typically run using an ASGI server like Uvicorn behind a reverse proxy (e.g., Nginx) in production. Docker setup handles this.

## 9. Docker and CI/CD

-   **Docker**: Use `docker-compose up --build` to build and run the application locally in containers. The `Dockerfile` for client and server, and `docker-compose.yml` define the containerized setup.
-   **CI/CD**: GitHub Actions are configured in `.github/workflows/ci.yml` for automated linting, testing, and building on pushes/pull requests. Ensure CI scripts are compatible with Svelte 5.

## 10. Contributing

-   We welcome contributions! Please follow the guidelines outlined in the main `README.md`.
-   Ensure your code adheres to the project's Svelte 5 standards and passes all checks/tests.
-   Create clear and descriptive pull requests.

## 11. Troubleshooting

-   Refer to the [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues.
-   Check backend logs (`server/logs/`) and browser developer console for errors.
-   Ensure environment variables are correctly set.

This guide should provide a solid foundation for developing within the Ultimate Sensor Monitor project using Svelte 5.
