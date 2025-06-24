// Compatibility re-export for legacy imports.
// The new canonical store implementation is in `sensorData.ts`.
// TODO: migrate all imports to use `./sensorData` (or directly from the store itself) and delete this file.
export { sensorDataManager } from "./sensorData";
