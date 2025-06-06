import { writable } from 'svelte/store';

export type AlertType = 'info' | 'success' | 'warning' | 'error';

export interface Alert {
  id: string;
  type: AlertType;
  message: string;
  title?: string;
  dismissible?: boolean;
  autoDismiss?: boolean;
  dismissTimeout?: number;
}

function createAlertsStore() {
  const { subscribe, update } = writable<Alert[]>([]);

  return {
    subscribe,
    add: (alert: Omit<Alert, 'id'>) => {
      const id = crypto.randomUUID();
      update(alerts => [...alerts, { ...alert, id }]);
      return id;
    },
    remove: (id: string) => {
      update(alerts => alerts.filter(alert => alert.id !== id));
    },
    clear: () => {
      update(() => []);
    }
  };
}

export const alerts = createAlertsStore();

// Helper functions for common alert types
export const showAlert = {
  info: (message: string, options?: Partial<Alert>) => {
    return alerts.add({ type: 'info', message, ...options });
  },
  success: (message: string, options?: Partial<Alert>) => {
    return alerts.add({ type: 'success', message, ...options });
  },
  warning: (message: string, options?: Partial<Alert>) => {
    return alerts.add({ type: 'warning', message, ...options });
  },
  error: (message: string, options?: Partial<Alert>) => {
    return alerts.add({ type: 'error', message, ...options });
  }
}; 