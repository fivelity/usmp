declare module "$lib/components/TopBar.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class TopBar extends SvelteComponent<{
    showLeftSidebar: boolean;
    showRightSidebar: boolean;
    onfoo: () => void;
    onbar: () => void;
  }> {}
}

declare module "$lib/components/LeftSidebar.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class LeftSidebar extends SvelteComponent<{
    onclose: () => void;
  }> {}
}

declare module "$lib/components/RightSidebar.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class RightSidebar extends SvelteComponent<{
    onclose: () => void;
  }> {}
}

declare module "$lib/components/DashboardCanvas.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class DashboardCanvas extends SvelteComponent {}
}

declare module "$lib/components/ContextMenu.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class ContextMenu extends SvelteComponent {}
}

declare module "$lib/components/ConnectionStatus.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class ConnectionStatus extends SvelteComponent {}
}

declare module "$lib/components/SnapGuides.svelte" {
  import type { SvelteComponent } from "svelte";
  export default class SnapGuides extends SvelteComponent {}
}
