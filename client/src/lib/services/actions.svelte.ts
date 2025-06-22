import { ui } from "$lib/stores/core/ui.svelte";
import { widgets as widgetStore } from "$lib/stores/data/widgets.svelte";
import {
  historyStore as history,
  RemoveWidgetCommand,
  UpdateWidgetCommand,
  AddWidgetCommand,
  BatchCommand,
} from "$lib/stores/history.svelte";
import type { WidgetConfig } from "$lib/types";

const isWidgetConfig = (w: WidgetConfig | undefined): w is WidgetConfig => !!w;

function createActionsService() {
  const { selectedWidgets, clipboard, setClipboard } = ui;
  const { widgets, updateWidget, removeWidget, addWidget } = widgetStore;

  function deleteSelectedWidgets() {
    const widgetsToRemove = [...selectedWidgets]
      .map((id) => widgets.find((w) => w.id === id))
      .filter(isWidgetConfig);
    if (widgetsToRemove.length === 0) return;

    const commands = widgetsToRemove.map(
      (widget) => new RemoveWidgetCommand(widget, addWidget, removeWidget),
    );
    const batchCommand = new BatchCommand(commands, "Delete selected widgets");
    history.execute(batchCommand);

    ui.clearSelection();
  }

  function bringToFront() {
    const maxZ = Math.max(0, ...widgets.map((w) => w.z_index || 0));
    const commands = [...selectedWidgets]
      .map((id) => {
        const widget = widgets.find((w) => w.id === id);
        if (widget) {
          const oldValues = { z_index: widget.z_index };
          const newValues = { z_index: maxZ + 1 };
          return new UpdateWidgetCommand(
            id,
            oldValues,
            newValues,
            updateWidget,
          );
        }
        return null;
      })
      .filter((cmd) => cmd !== null) as UpdateWidgetCommand[];

    if (commands.length > 0) {
      const batchCommand = new BatchCommand(commands, "Bring widgets to front");
      history.execute(batchCommand);
    }
  }

  function sendToBack() {
    const minZ = Math.min(0, ...widgets.map((w) => w.z_index || 0));
    const commands = [...selectedWidgets]
      .map((id) => {
        const widget = widgets.find((w) => w.id === id);
        if (widget) {
          const oldValues = { z_index: widget.z_index };
          const newValues = { z_index: minZ - 1 };
          return new UpdateWidgetCommand(
            id,
            oldValues,
            newValues,
            updateWidget,
          );
        }
        return null;
      })
      .filter((cmd) => cmd !== null) as UpdateWidgetCommand[];

    if (commands.length > 0) {
      const batchCommand = new BatchCommand(commands, "Send widgets to back");
      history.execute(batchCommand);
    }
  }

  function cutSelectedWidgets() {
    copySelectedWidgets();
    deleteSelectedWidgets();
  }

  function copySelectedWidgets() {
    const widgetsToCopy = [...selectedWidgets]
      .map((id) => widgets.find((w) => w.id === id))
      .filter(isWidgetConfig);
    if (widgetsToCopy.length > 0) {
      setClipboard(widgetsToCopy);
    }
  }

  function pasteWidgets() {
    if (!clipboard || clipboard.length === 0) return;

    const commands = clipboard.map((widgetToPaste) => {
      const newWidget = {
        ...widgetToPaste,
        id: `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        pos_x: widgetToPaste.pos_x + 20,
        pos_y: widgetToPaste.pos_y + 20,
      };
      return new AddWidgetCommand(newWidget, addWidget, removeWidget);
    });

    if (commands.length > 0) {
      const batchCommand = new BatchCommand(commands, "Paste widgets");
      history.execute(batchCommand);
    }
  }

  function addNewWidget() {
    // Placeholder for add functionality
    console.log("Add new widget action triggered");
  }

  return {
    deleteSelectedWidgets,
    bringToFront,
    sendToBack,
    cutSelectedWidgets,
    copySelectedWidgets,
    pasteWidgets,
    addNewWidget,
  };
}

export const actions = createActionsService();
