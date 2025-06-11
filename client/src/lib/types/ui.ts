export type EditMode = "view" | "edit";

export interface DragState {
  isDragging: boolean;
  startX: number;
  startY: number;
  currentX: number;
  currentY: number;
  widgetId?: string;
  initialWidth?: number;
  initialHeight?: number;
}

interface BaseContextMenuItem {
  id?: string;
  disabled?: boolean;
  icon?: string;
  shortcut?: string;
}

interface ActionContextMenuItem extends BaseContextMenuItem {
  type: "item";
  label: string;
  action: string;
}

interface SeparatorContextMenuItem extends BaseContextMenuItem {
  id?: never;
  type: "separator";
  label?: never;
  action?: never;
}

export type ContextMenuItem = ActionContextMenuItem | SeparatorContextMenuItem;

export interface ContextMenuState {
  show: boolean;
  x: number;
  y: number;
  items: ContextMenuItem[];
  targetId?: string;
  targetType?: string;
}
