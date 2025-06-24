# Ultimate Sensor Monitor - Backend Development Plan & Onboarding Guide

## 1. Project Overview

Welcome to the Ultimate Sensor Monitor backend! This FastAPI-based Python application serves as the data hub for sensor information, providing:

*   **Real-time sensor data:** Via WebSocket connections.
*   **REST APIs:** For managing sensor configurations, dashboard presets, and other application settings.
*   **Modular Sensor Integration:** Supports various hardware monitoring tools (LibreHardwareMonitor, HWiNFO, Mock data) through a common interface.

**Key Technologies:**
*   Python 3.9+
*   FastAPI: For high-performance web APIs.
*   Pydantic: For data validation and settings management.
*   Uvicorn: ASGI server.
*   WebSockets: For real-time communication.

## 2. Current State & Goals

The backend is currently undergoing a significant refactoring effort to improve its robustness, maintainability, and overall professionalism. Some foundational Pydantic models and core utilities are in place, but several areas require attention.

**Overall Goal:** To establish a clean, well-structured, and thoroughly tested backend that is easy to extend and maintain.

## 3. Key Refactoring & Development Tasks

This plan outlines the critical tasks to achieve our goal.

### I. Project Structure & Cleanup

1.  **Consolidate Configuration:**
    *   **Task:** Remove the redundant `server/app/config.py`.
    *   **Action:** Standardize all configuration loading using `server/app/core/config.py` (`AppSettings` Pydantic model). Ensure all modules use `get_settings()` from this file.
    *   **Why:** Single source of truth for configuration, better organization.

2.  **Consolidate Data Models:**
    *   **Task:** Remove the redundant `server/app/models.py`.
    *   **Action:** Ensure all Pydantic data models reside within the `server/app/models/` directory, organized into logical files (e.g., `sensor.py`, `widget.py`, `websocket.py`). Use `server/app/models/__init__.py` for clean exports.
    *   **Why:** Clearer model organization, avoids duplication.

### II. Core Application Setup (`main.py`)

1.  **Restore and Enhance `server/app/main.py`:**
    *   **Task:** The current `main.py` is minimal (used for debugging). Restore its original functionality or recreate it based on best practices.
    *   **Action:** The `main.py` should:
        *   Initialize the FastAPI application instance.
        *   Load application settings from `core.config.get_settings()`.
        *   Set up CORS middleware (`CORSMiddleware`).
        *   Set up security headers middleware (from `core.security`).
        *   Initialize logging (from `core.logging.setup_logging()`).
        *   Register global exception handlers (using `core.exceptions`).
        *   Include API routers (from `app.api` package).
        *   Define the main WebSocket endpoint (`/ws/{client_id}`).
        *   Implement application startup and shutdown event handlers (e.g., to initialize/close sensor manager, WebSocket manager).
    *   **Why:** Centralized application setup, proper lifecycle management.

### III. API Development

1.  **Modularize API Routes:**
    *   **Task:** Create a dedicated `server/app/api/` package.
    *   **Action:**
        *   Move existing API endpoint logic (or create new logic) into separate files within `app/api/` using `APIRouter` (e.g., `api_sensors.py`, `api_presets.py`, `api_system.py`).
        *   Each router should handle a specific domain of the API.
        *   Import and include these routers in `main.py`.
    *   **Why:** Better organization, scalability, and separation of concerns for API endpoints.
    *   **Reference:** `docs/API_DOCUMENTATION.md` for endpoint definitions.

### IV. WebSocket Enhancements

1.  **Refine `server/app/websocket_manager.py`:**
    *   **Task:** Improve robustness, message handling, and configuration.
    *   **Action:**
        *   **Pydantic Models:** Use models from `app.models.websocket` for both incoming message parsing (`parse_websocket_message`) and outgoing message construction.
        *   **Client ID:** Utilize the `client_id` from the WebSocket URL for connection tracking.
        *   **Configuration:** Use `AppSettings` for settings like heartbeat intervals, max connections, etc. (avoid hardcoding).
        *   **Heartbeats:** Implement proper client-server heartbeat mechanism (`MessageType.HEARTBEAT`, `MessageType.HEARTBEAT_RESPONSE`).
        *   **Logging:** Use `get_logger("websocket_manager")` from `core.logging`.
        *   **Error Handling:** Send structured `ErrorMessage` (Pydantic model) to clients.
    *   **Why:** Reliable and type-safe real-time communication.

### V. Sensor Integration

1.  **Finalize `BaseSensor` Interface (`app/sensors/base.py`):**
    *   **Task:** Ensure the abstract base class for sensor providers is complete and uses `async` methods and Pydantic models (`SensorDefinition`, `SensorReading`).
    *   **Action:** Verify methods: `async initialize(self, app_settings: AppSettings)`, `async close()`, `async is_available()`, `async get_available_sensors() -> List[SensorDefinition]`, `async get_current_data() -> List[SensorReading]`.
    *   **Why:** Standardized interface for all sensor modules.

2.  **Refactor Sensor Implementations:**
    *   **Task:** Update `MockSensor`, `LHMSensor`, and `HWiNFOSensor` to conform to the new `BaseSensor` interface.
    *   **Action (`MockSensor`):** Complete refactoring to use async methods and Pydantic models (partially done).
    *   **Action (`LHMSensor`):
        *   Replace local dataclasses with Pydantic models from `app.models.sensor`.
        *   Use `app_settings` for configuration.
        *   Manage internal polling with an `asyncio.Task`.
        *   Wrap blocking calls (DLL/package interaction) with `await asyncio.to_thread()`.
    *   **Action (Other Sensors):** Apply similar refactoring.
    *   **Logging:** Use `get_logger()` in all sensor modules.
    *   **Why:** Consistent, asynchronous, and robust sensor data providers.

3.  **Implement `SensorManager` Service:**
    *   **Task:** Create a new service (e.g., `app/services/sensor_manager.py`).
    *   **Action:**
        *   Discover, instantiate, and `async initialize` all configured sensor providers.
        *   Run a main `asyncio.Task` to periodically call `get_current_data()` on active sensors.
        *   Aggregate and cache sensor readings.
        *   Provide `async` methods for the API layer and `WebSocketManager` to access data.
        *   Handle graceful shutdown of sensor providers via `async close()`.
    *   **Why:** Centralized control and data flow for all sensors.

### VI. Core Services & Utilities

1.  **Implement `core/security.py`:**
    *   **Task:** Implement actual API key/token validation.
    *   **Action:** Replace placeholder `verify_api_key` with robust logic (e.g., check against environment variables, database, or validate JWTs using `settings.secret_key`).
    *   Integrate `SecurityHeaders` middleware in `main.py`.
    *   **Why:** Secure the application.

2.  **Enhance `core/logging.py`:**
    *   **Task:** Add production-ready logging features.
    *   **Action:**
        *   Implement file-based logging (e.g., `RotatingFileHandler`), configurable via `settings`.
        *   Consider an option for structured JSON logging for production.
    *   **Why:** Better observability and debugging in production.

3.  **Utilize `core/exceptions.py`:**
    *   **Task:** Ensure custom exceptions are used and handled.
    *   **Action:** Raise specific exceptions (e.g., `SensorException`) throughout the application. Register global exception handlers in `main.py` to convert them to appropriate HTTP responses.
    *   **Why:** Consistent and informative error reporting.

### VII. Code Quality & DevOps

1.  **Code Formatting & Linting:**
    *   **Task:** Enforce consistent code style.
    *   **Action:** Configure and use `black` for formatting and `ruff` (or `flake8` + `isort`) for linting. Integrate into pre-commit hooks if possible.
    *   **Why:** Readability and maintainability.

2.  **Testing:**
    *   **Task:** Implement comprehensive tests.
    *   **Action:** Write unit tests (`pytest`) for individual components (models, utilities, sensor logic) and integration tests for API endpoints and WebSocket interactions. Aim for good test coverage.
    *   **Why:** Ensure reliability and prevent regressions.

3.  **Documentation:**
    *   **Task:** Maintain and expand documentation.
    *   **Action:** Keep `DEVELOPER_GUIDE.md` and `API_DOCUMENTATION.md` up-to-date. Add comprehensive docstrings to all modules, classes, and functions.
    *   **Why:** Easier onboarding and understanding of the codebase.

4.  **Dependency Management:**
    *   **Task:** Ensure `requirements.txt` is accurate and up-to-date.
    *   **Action:** Regularly update dependencies and consider using a more advanced tool like `poetry` or `pdm` for better dependency resolution and packaging.
    *   **Why:** Reproducible builds and easier dependency management.

## 4. Development Workflow & Best Practices

*   **Version Control:** Use Git. Create feature branches for new work, rebase/merge into `main` (or `develop`) frequently.
*   **Code Reviews:** All significant changes should be peer-reviewed.
*   **Run Linters/Formatters:** Before committing code.
*   **Run Tests:** Before pushing changes and after pulling updates.
*   **Communicate:** Discuss design decisions and challenges with the team.

## 5. Getting Started

*   **Key Directories:**
    *   `server/app/`: Main application code.
    *   `server/app/core/`: Core utilities (config, logging, security, exceptions).
    *   `server/app/models/`: Pydantic data models.
    *   `server/app/sensors/`: Sensor provider implementations.
    *   `server/app/api/`: API route definitions (to be created).
    *   `server/app/services/`: Business logic services (e.g., SensorManager - to be created).
*   **Running the Server:**
    1.  Navigate to the `server/` directory.
    2.  Ensure your `.env` file is configured (see `core/config.py` for expected variables, prefixed with `ULTIMON_`).
    3.  Run: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8100` (the `--reload` flag is useful for development).

This plan provides a roadmap for enhancing the backend. Prioritize tasks based on impact and dependencies. Good luck!
