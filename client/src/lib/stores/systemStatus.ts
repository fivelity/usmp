import { writable, get } from "svelte/store";
import type { SystemEvent } from "$lib/types";

// Create a store for system events
const createSystemStatusStore = () => {
  const events = writable<SystemEvent[]>([]);
  const maxEvents = writable(50); // Maximum number of events to keep in history

  function addEvent(event: Omit<SystemEvent, "id" | "timestamp">) {
    const newEvent: SystemEvent = {
      ...event,
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
    };

    events.update(currentEvents => {
      const updatedEvents = [newEvent, ...currentEvents];
      // Trim events if we exceed maxEvents
      if (updatedEvents.length > get(maxEvents)) {
        return updatedEvents.slice(0, get(maxEvents));
      }
      return updatedEvents;
    });
  }

  function clearEvents() {
    events.set([]);
  }

  function removeEvent(id: string) {
    events.update(currentEvents => 
      currentEvents.filter(event => event.id !== id)
    );
  }

  function setMaxEvents(max: number) {
    maxEvents.set(max);
    events.update(currentEvents => {
      if (currentEvents.length > max) {
        return currentEvents.slice(0, max);
      }
      return currentEvents;
    });
  }

  return {
    events,
    maxEvents,
    addEvent,
    clearEvents,
    removeEvent,
    setMaxEvents,
  };
};

export const systemStatus = createSystemStatusStore();
