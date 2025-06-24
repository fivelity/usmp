import type { DashboardLayout } from "./dashboard";
import type { Widget } from "./widgets";

export interface Preset {
  id: string;
  name: string;
  layout: DashboardLayout;
  widgets: Record<string, Widget>;
  createdAt:
    | {
        seconds: number;
        nanoseconds: number;
      }
    | Date;
  author?: string;
}
