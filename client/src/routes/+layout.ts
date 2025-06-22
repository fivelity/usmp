// Configure for static site generation
// Sensor data will be fetched client-side via WebSocket and API calls
export const prerender = true;
export const ssr = false;
export const csr = true;

// No server-side data loading needed
// All dynamic data (sensors, hardware) will be loaded client-side
