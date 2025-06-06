import { writable } from "svelte/store";
import type { SystemEvent } from "$lib/types";

// Create a store for system events
const createSystemStatusStore = () => {
  const events = $state<SystemEvent[]>([]);
  let maxEvents = $state(50); // Maximum number of events to keep in history

  function addEvent(event: Omit<SystemEvent, "id" | "timestamp">) {
    const newEvent: SystemEvent = {
      ...event,
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
    };

    events.unshift(newEvent);

    // Trim events if we exceed maxEvents
    if (events.length > maxEvents) {
      events.length = maxEvents;
    }
  }

  function clearEvents() {
    events.length = 0;
  }

  function removeEvent(id: string) {
    const index = events.findIndex((event) => event.id === id);
    if (index !== -1) {
      events.splice(index, 1);
    }
  }

  function setMaxEvents(max: number) {
    maxEvents = max;
    if (events.length > maxEvents) {
      events.length = maxEvents;
    }
  }

  return {
    get events() {
      return events;
    },
    get maxEvents() {
      return maxEvents;
    },
    addEvent,
    clearEvents,
    removeEvent,
    setMaxEvents,
  };
};

export const systemStatus = createSystemStatusStore();
