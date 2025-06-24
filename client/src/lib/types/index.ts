/**
 * ==================================================================
 * Type Definitions for Ultimate Sensor Monitor
 *
 * This file centralizes all core type definitions used across the
 * application, ensuring consistency and type safety.
 * ==================================================================
 */

// Re-exporting from more specific files
export * from "./sensors";
export * from "./widgets";
export * from "./ui";
export * from "./dashboard";
export * from "./api";
export * from "./stores";
export * from "./common";
export * from "./gauges";
// Note: SystemState is already exported via stores.d.ts re-exports.
// To avoid duplicate identifier errors, only export SystemEvent directly.
export type { SystemEvent } from "./system";

// Add aliases for commonly used types
export type { SensorReading as SensorData } from "./sensors";
export type { ExtendedGaugeType as GaugeType } from "./widgets";
