/**
 * Environment configuration for production deployment.
 * Centralized configuration management with type safety.
 */

export interface Environment {
  // Application metadata
  readonly APP_NAME: string;
  readonly APP_VERSION: string;
  readonly APP_DESCRIPTION: string;

  // API configuration
  readonly API_BASE_URL: string;
  readonly WEBSOCKET_URL: string;
  readonly API_TIMEOUT: number;

  // Feature flags
  readonly ENABLE_DEBUG: boolean;
  readonly ENABLE_MOCK_DATA: boolean;
  readonly ENABLE_ANALYTICS: boolean;
  readonly ENABLE_ERROR_REPORTING: boolean;

  // Performance settings
  readonly MAX_WIDGETS_PER_DASHBOARD: number;
  readonly SENSOR_UPDATE_INTERVAL: number;
  readonly WEBSOCKET_RECONNECT_INTERVAL: number;
  readonly MAX_RECONNECT_ATTEMPTS: number;

  // UI settings
  readonly DEFAULT_THEME: string;
  readonly ANIMATION_DURATION: number;
  readonly DEBOUNCE_DELAY: number;

  // Security settings
  readonly ENABLE_CSP: boolean;
  readonly ALLOWED_ORIGINS: string[];
}

// Load Vite env vars (available in browser and dev server)
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8100";
const WS_BASE = import.meta.env.VITE_WEBSOCKET_URL || "ws://localhost:8100/ws";

// Development environment
const development: Environment = {
  APP_NAME: "Ultimate Sensor Monitor",
  APP_VERSION: "2.0.0",
  APP_DESCRIPTION: "Professional hardware sensor monitoring system",

  API_BASE_URL: API_BASE,
  WEBSOCKET_URL: WS_BASE,
  API_TIMEOUT: 10000,

  ENABLE_DEBUG: true,
  ENABLE_MOCK_DATA: true,
  ENABLE_ANALYTICS: false,
  ENABLE_ERROR_REPORTING: false,

  MAX_WIDGETS_PER_DASHBOARD: 100,
  SENSOR_UPDATE_INTERVAL: 2000,
  WEBSOCKET_RECONNECT_INTERVAL: 3000,
  MAX_RECONNECT_ATTEMPTS: 5,

  DEFAULT_THEME: "dark",
  ANIMATION_DURATION: 300,
  DEBOUNCE_DELAY: 300,

  ENABLE_CSP: false,
  ALLOWED_ORIGINS: ["http://localhost:5501", "http://localhost:4173"],
};

// Production environment (same vars)
const production: Environment = {
  APP_NAME: "Ultimate Sensor Monitor",
  APP_VERSION: "2.0.0",
  APP_DESCRIPTION: "Professional hardware sensor monitoring system",

  API_BASE_URL: API_BASE,
  WEBSOCKET_URL: WS_BASE,
  API_TIMEOUT: 15000,

  ENABLE_DEBUG: false,
  ENABLE_MOCK_DATA: false,
  ENABLE_ANALYTICS: true,
  ENABLE_ERROR_REPORTING: true,

  MAX_WIDGETS_PER_DASHBOARD: 200,
  SENSOR_UPDATE_INTERVAL: 2000,
  WEBSOCKET_RECONNECT_INTERVAL: 5000,
  MAX_RECONNECT_ATTEMPTS: 10,

  DEFAULT_THEME: "dark",
  ANIMATION_DURATION: 200,
  DEBOUNCE_DELAY: 500,

  ENABLE_CSP: true,
  ALLOWED_ORIGINS: [],
};

// Test environment
const test: Environment = {
  ...development,
  ENABLE_DEBUG: false,
  ENABLE_MOCK_DATA: true,
  API_TIMEOUT: 5000,
  SENSOR_UPDATE_INTERVAL: 1000,
  ANIMATION_DURATION: 0,
};

// Environment detection based on Vite mode
function getEnvironment(): "development" | "production" | "test" {
  return (
    (import.meta.env.MODE as "development" | "production" | "test") ??
    "development"
  );
}

// Export current environment configuration
const currentEnv = getEnvironment();

export const env: Environment = (() => {
  switch (currentEnv) {
    case "production":
      return production;
    case "test":
      return test;
    case "development":
    default:
      return development;
  }
})();

// Environment utilities
export const isDevelopment = currentEnv === "development";
export const isProduction = currentEnv === "production";
export const isTest = currentEnv === "test";

// Logging utility
export function log(...args: any[]): void {
  if (env.ENABLE_DEBUG) {
    console.log(`[${env.APP_NAME}]`, ...args);
  }
}

export function warn(...args: any[]): void {
  if (env.ENABLE_DEBUG) {
    console.warn(`[${env.APP_NAME}]`, ...args);
  }
}

export function error(...args: any[]): void {
  console.error(`[${env.APP_NAME}]`, ...args);

  if (env.ENABLE_ERROR_REPORTING && isProduction) {
    // Implement error reporting service integration here
    // Example: Sentry, LogRocket, etc.
  }
}

// Configuration validation
export function validateEnvironment(): boolean {
  const required = [
    "API_BASE_URL",
    "WEBSOCKET_URL",
    "APP_NAME",
    "APP_VERSION",
  ] as const;

  for (const key of required) {
    if (!env[key]) {
      error(`Missing required environment variable: ${key}`);
      return false;
    }
  }

  return true;
}

// Export environment name for debugging
export const environmentName = currentEnv;
