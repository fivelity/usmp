---
trigger: always_on
description: 
globs: 
---
# 01-project-structure
## Project Structure
### Directory layout, file naming conventions, and separation of concerns.
STRICT REQUIREMENT:
Client (`client/`) Directory Structure:
- SvelteKit project structure
- Global CSS: `src/app.css`
- Common styles: `src/lib/styles/common.css`
- UI components: `src/lib/components/ui/`
- Core widgets: `src/lib/components/core/widgets/`
- Stores: `src/lib/stores/` (e.g., `sensorData.svelte.ts`, `connectionStatus.ts`)
- Services: `src/lib/services/`
- Type definitions: `src/lib/types/`

Server (`server/`) Directory Structure:
- FastAPI application entry point: `server/app/main.py`
- Core configuration: `server/app/core/config.py`
- Sensor-specific logic: `server/app/sensors/`
- Pydantic models: `server/app/models/`

- Virtual environment: Managed by `venv`