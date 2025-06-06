import { writable, get } from "svelte/store";

export type NotificationType = "info" | "success" | "warning" | "error";
export type NotificationCategory = "system" | "sensor" | "alert" | "user";

export interface Notification {
  id: string;
  type: NotificationType;
  category: NotificationCategory;
  title: string;
  message: string;
  timestamp: number;
  read: boolean;
  priority: "low" | "medium" | "high";
  data?: Record<string, any>;
  actions?: Array<{
    label: string;
    handler: () => void;
  }>;
  sound?: boolean;
  desktop?: boolean;
}

interface NotificationPreferences {
  desktopEnabled: boolean;
  soundEnabled: boolean;
  soundVolume: number;
  categories: {
    [K in NotificationCategory]: {
      desktop: boolean;
      sound: boolean;
    };
  };
}

const defaultPreferences: NotificationPreferences = {
  desktopEnabled: true,
  soundEnabled: true,
  soundVolume: 0.5,
  categories: {
    system: { desktop: true, sound: true },
    sensor: { desktop: true, sound: true },
    alert: { desktop: true, sound: true },
    user: { desktop: true, sound: true },
  },
};

// Load preferences from localStorage
const storedPreferences = localStorage.getItem("notificationPreferences");
const preferences = writable<NotificationPreferences>(
  storedPreferences ? JSON.parse(storedPreferences) : defaultPreferences,
);

// Save preferences to localStorage when they change
preferences.subscribe((value) => {
  localStorage.setItem("notificationPreferences", JSON.stringify(value));
});

// Sound effects for different notification types
const notificationSounds = {
  info: "/sounds/notification-info.mp3",
  success: "/sounds/notification-success.mp3",
  warning: "/sounds/notification-warning.mp3",
  error: "/sounds/notification-error.mp3",
};

// Audio context for playing sounds
let audioContext: AudioContext | null = null;

function createNotificationsStore() {
  const { subscribe, set, update } = writable<Notification[]>([]);

  // Initialize audio context on user interaction
  function initAudio() {
    if (!audioContext) {
      audioContext = new AudioContext();
    }
  }

  // Play notification sound
  async function playSound(type: NotificationType) {
    const $preferences = get(preferences);
    if (!$preferences.soundEnabled) return;

    initAudio();
    if (!audioContext) return;

    try {
      const response = await fetch(notificationSounds[type]);
      const arrayBuffer = await response.arrayBuffer();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

      const source = audioContext.createBufferSource();
      source.buffer = audioBuffer;

      const gainNode = audioContext.createGain();
      gainNode.gain.value = $preferences.soundVolume;

      source.connect(gainNode);
      gainNode.connect(audioContext.destination);
      source.start();
    } catch (error) {
      console.error("Error playing notification sound:", error);
    }
  }

  // Show desktop notification
  async function showDesktopNotification(notification: Notification) {
    const $preferences = get(preferences);
    if (!$preferences.desktopEnabled) return;
    if (!$preferences.categories[notification.category].desktop) return;

    try {
      const permission = await Notification.requestPermission();
      if (permission === "granted") {
        new Notification(notification.title, {
          body: notification.message,
          icon: "/icons/notification-icon.png",
          badge: "/icons/notification-badge.png",
          tag: notification.id,
          requireInteraction: notification.priority === "high",
        });
      }
    } catch (error) {
      console.error("Error showing desktop notification:", error);
    }
  }

  return {
    subscribe,
    add: (notification: Omit<Notification, "id" | "timestamp" | "read">) => {
      const id = crypto.randomUUID();
      const newNotification: Notification = {
        ...notification,
        id,
        timestamp: Date.now(),
        read: false,
      };

      update((notifications) => [newNotification, ...notifications]);

      // Handle desktop notification and sound
      if (newNotification.desktop !== false) {
        showDesktopNotification(newNotification);
      }
      if (newNotification.sound !== false) {
        playSound(newNotification.type);
      }
    },
    markAsRead: (id: string) => {
      update((notifications) =>
        notifications.map((n) => (n.id === id ? { ...n, read: true } : n)),
      );
    },
    markAllAsRead: () => {
      update((notifications) =>
        notifications.map((n) => ({ ...n, read: true })),
      );
    },
    remove: (id: string) => {
      update((notifications) => notifications.filter((n) => n.id !== id));
    },
    clear: () => {
      set([]);
    },
    clearByCategory: (category: NotificationCategory) => {
      update((notifications) =>
        notifications.filter((n) => n.category !== category),
      );
    },
    updatePreferences: (newPreferences: Partial<NotificationPreferences>) => {
      preferences.update((current) => ({
        ...current,
        ...newPreferences,
      }));
    },
  };
}

export const notifications = createNotificationsStore();

// Helper functions for common notification types
export const notify = {
  system: {
    info: (message: string, title = "System Information") =>
      notifications.add({
        type: "info",
        category: "system",
        title,
        message,
        priority: "low",
      }),
    warning: (message: string, title = "System Warning") =>
      notifications.add({
        type: "warning",
        category: "system",
        title,
        message,
        priority: "medium",
      }),
    error: (message: string, title = "System Error") =>
      notifications.add({
        type: "error",
        category: "system",
        title,
        message,
        priority: "high",
      }),
  },
  sensor: {
    update: (sensorId: string, value: number, unit: string) =>
      notifications.add({
        type: "info",
        category: "sensor",
        title: `Sensor Update: ${sensorId}`,
        message: `Current value: ${value} ${unit}`,
        priority: "low",
        data: { sensorId, value, unit },
      }),
    alert: (sensorId: string, message: string) =>
      notifications.add({
        type: "warning",
        category: "sensor",
        title: `Sensor Alert: ${sensorId}`,
        message,
        priority: "high",
        data: { sensorId },
      }),
  },
  user: {
    action: (message: string, title = "User Action") =>
      notifications.add({
        type: "info",
        category: "user",
        title,
        message,
        priority: "low",
      }),
    error: (message: string, title = "Action Failed") =>
      notifications.add({
        type: "error",
        category: "user",
        title,
        message,
        priority: "medium",
      }),
  },
};
