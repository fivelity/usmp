/**
 * History Management Store (Undo/Redo)
 * Implements the command pattern for undo/redo functionality.
 */

export abstract class Command {
  abstract execute(): void;
  abstract undo(): void;
}

export class MoveWidgetCommand extends Command {
  override execute() {
    /* Implementation needed */
  }
  override undo() {
    /* Implementation needed */
  }
}
export class ResizeWidgetCommand extends Command {
  override execute() {
    /* Implementation needed */
  }
  override undo() {
    /* Implementation needed */
  }
}
export class AddWidgetCommand extends Command {
  constructor(
    private widget: any,
    private addWidget: (widget: any) => void,
    private removeWidget: (id: string) => void
  ) {
    super();
  }
  
  override execute() {
    this.addWidget(this.widget);
  }
  
  override undo() {
    this.removeWidget(this.widget.id);
  }
}

export class RemoveWidgetCommand extends Command {
  constructor(
    private widget: any,
    private addWidget: (widget: any) => void,
    private removeWidget: (id: string) => void
  ) {
    super();
  }
  
  override execute() {
    this.removeWidget(this.widget.id);
  }
  
  override undo() {
    this.addWidget(this.widget);
  }
}

export class UpdateWidgetCommand extends Command {
  constructor(
    private widgetId: string,
    private oldValues: any,
    private newValues: any,
    private updateWidget: (id: string, updates: any) => void
  ) {
    super();
  }
  
  override execute() {
    this.updateWidget(this.widgetId, this.newValues);
  }
  
  override undo() {
    this.updateWidget(this.widgetId, this.oldValues);
  }
}
export class GroupWidgetsCommand extends Command {
  override execute() {
    /* Implementation needed */
  }
  override undo() {
    /* Implementation needed */
  }
}

export class BatchCommand extends Command {
  constructor(private commands: Command[], private description?: string) {
    super();
  }
  override execute() {
    this.commands.forEach((cmd) => cmd.execute());
  }
  override undo() {
    this.commands
      .slice()
      .reverse()
      .forEach((cmd) => cmd.undo());
  }
}

function createHistoryStore() {
  const undoStack = $state<Command[]>([]);
  const redoStack = $state<Command[]>([]);

  const execute = (command: Command) => {
    command.execute();
    undoStack.push(command);
    redoStack.length = 0;
  };

  const undo = () => {
    const command = undoStack.pop();
    if (command) {
      command.undo();
      redoStack.push(command);
    }
  };

  const redo = () => {
    const command = redoStack.pop();
    if (command) {
      command.execute();
      undoStack.push(command);
    }
  };

  return {
    execute,
    undo,
    redo,
    get canUndo() {
      return undoStack.length > 0;
    },
    get canRedo() {
      return redoStack.length > 0;
    },
  };
}

export const historyStore = createHistoryStore();
