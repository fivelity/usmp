import type { DashboardLayout } from "$lib/types/dashboard";

function createDashboardStore() {
  let layout = $state<DashboardLayout>({
    grid_size: [100, 100],
    background_color: "#1a1a1a",
    show_grid: true,
    grid_color: "#333333",
    background_opacity: 1,
  });

  return {
    get layout() {
      return layout;
    },
    setLayout(newLayout: DashboardLayout) {
      layout = newLayout;
    },
  };
}

export const dashboard = createDashboardStore();
