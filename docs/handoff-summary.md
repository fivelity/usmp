# Ultimate Sensor Monitor – Handoff Summary

## 1. Repository Structure
```
root/
├─ server/   # FastAPI backend
└─ client/   # SvelteKit 5 frontend
```
(See `docs/01-project-structure.md` for full details.)

---

## 2. Front-End Progress
* **Tech Stack**: Svelte 5 (Runes), Tailwind CSS v4, pnpm, ESLint/Prettier, Vitest, Playwright.
* **Theming**
  * `visual.svelte.ts` store – central theme/typography/grid prefs.
  * `ThemeManager.svelte` – applies Tailwind `dark` class + CSS vars.
  * `TopBar.svelte` – Sun/Moon toggle wired to `visualUtils.toggleTheme()`.
* **State Stores**
  * `widgets.svelte.ts` – `$state<Record<string, WidgetConfig>>`; added `widgetMap` and `setWidgets()` util (preset import/export).
  * `dashboard.svelte.ts` – layout getter / setter.
  * `history.svelte.ts` – undo/redo via Command pattern.
* **Preset Workflow** – Import/Export to file & Firebase cloud in `TopBar.svelte`.
* **Tailwind Config** – `tailwind.config.js` extended with custom palettes, fonts and dark-mode class.

---

## 3. Back-End Status / TODO
* **Scaffolding exists** but missing production features:
  * Structured JSON logging, security headers, global exception handlers.
  * `SensorManager`, async sensor drivers (Mock, LibreHardwareMonitor (via HardwareMonitor Python package), HWiNFO).
  * WebSocketManager: heart-beats, client tracking, structured error model.
  * REST routers for presets & widgets.
  * Full Pydantic V2 migration.

---

## 4. Outstanding Front-End Tasks
1. Grid drag/resize + snap (see `GridSystem.svelte`, `DashboardCanvas.svelte`).
2. Widget palette modal for adding gauges.
3. `realtime.ts` WebSocket client → update `sensorData` & widgets.
4. Finalise accessibility / CLS fixes + theme JSON import/export.
5. Unit tests (Vitest) & E2E tests (Playwright) – theme toggle, dashboard load, WS connectivity.
6. CI workflow (GitHub Actions) for lint → test → build.

---

## 5. Dev Workflow
```bash
# Front-end
pnpm i
pnpm dev        # runs on :5173

# Back-end
cd server
uvicorn app.main:app --host 0.0.0.0 --port 8100
```
*Make sure ports 5173 & 8100 are free; previous “app initialisation failed” was a port conflict.*

---

## 6. Conventions & Standards
* **Type-Safety**: strict TypeScript, avoid `any`; JSDoc for legacy `.js` files.
* **Naming**: PascalCase classes, camelCase funcs, kebab-case filenames, one export per file.
* **Stores**: Svelte 5 Runes (`$state`, `$derived`, `$effect`).
* **Styling**: Tailwind only; custom CSS lives in `src/app.css`.
* **Docs**: keep `docs/*` updated (API, Developer Guide, Theme System, Widget Guide, etc.).

---

## 7. Next-Sprint Checklist (TL;DR)
- [ ] Finish widget grid drag/resize & selection.
- [ ] Build `realtime.ts` WebSocket client, wire into `sensorData`.
- [ ] Convert one widget (e.g. `RadialGauge`) to live updates.
- [ ] Write Vitest tests for visual & widget stores.
- [ ] Add GitHub Actions CI.

> **Tip for new devs**: Start by running both dev servers, toggle themes via `TopBar`, then focus on integrating live sensor data into an existing gauge to verify end-to-end flow.