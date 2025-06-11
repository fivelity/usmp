/**
 * Common API response typings used throughout the frontend.
 * Keeping this isolated prevents circular dependencies and keeps payload-related
 * types in one place.
 */

export interface ApiResponse<T = unknown> {
  /** Indicates whether the request was successful */
  success: boolean;
  /** Payload returned from the backend (undefined when success is false) */
  data?: T;
  /** Human-readable error message (present when success is false) */
  error?: string;
}

// ---------------------------------------------------------------------------
// Helpful aliases for domain models that travel over the wire.
// ---------------------------------------------------------------------------

import type { Preset } from "./presets";

/** Alias to keep historical naming consistency in services */
export type DashboardPreset = Preset;
