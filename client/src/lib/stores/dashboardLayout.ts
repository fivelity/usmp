import { writable } from "svelte/store";
import type { DashboardLayout } from "$lib/types/dashboard";

export const dashboardLayout = writable<DashboardLayout>({
  canvas_width: 1920,
  canvas_height: 1080,
  background_type: "solid",
  background_settings: {
    color: "#f8fafc",
  },
  grid_settings: {
    visible: true,
    snap: true,
    color: "#e0e0e0",
    size: 20,
  },
});
