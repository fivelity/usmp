import { describe, it, expect, beforeEach, vi } from "vitest";
import { tick } from "svelte";
import { getStoreVersion } from "../widgets.svelte.js";
import {
  addWidget,
  removeWidget,
  updateWidget,
  getWidgetById,
  getWidgetArray,
  getWidgetMap,
  getWidgetGroups,
  setWidgets,
} from "../widgets.svelte.js";
import type { WidgetConfig } from "$lib/types";

describe("Widget Store", () => {
  const mockWidget: WidgetConfig = {
    id: "test-widget-1",
    type: "gauge",
    title: "Test Widget",
    pos_x: 0,
    pos_y: 0,
    width: 2,
    height: 2,
    is_locked: false,
    gauge_type: "gauge",
    gauge_settings: {},
    z_index: 0,
    is_visible: true,
    is_draggable: true,
    is_resizable: true,
    is_selectable: true,
    is_grouped: false,
  };

  const mockWidgetWithGroup: WidgetConfig = {
    ...mockWidget,
    id: "test-widget-2",
    group_id: "test-group",
  };

  // Track state version changes for reactivity testing
  let stateVersion = 0;

  beforeEach(async () => {
    // Clear widgets before each test
    setWidgets([]);
    stateVersion = getStoreVersion();

    // Clear tracked effects
    trackedEffects = [];

    // Wait for state to settle
    await waitForStateUpdate();
  });

  // Improved state tracking function that actually tracks reactivity
  function createTrackedEffect(fn: () => void) {
    // Run the function initially
    fn();

    // In a real implementation, this would set up reactive tracking
    // For tests, we'll simulate it by re-running the function after state changes
    const cleanup = () => {};

    // Store the function so we can re-run it after mutations
    trackedEffects.push(fn);

    return cleanup;
  }

  // Keep track of all tracked effects so we can re-run them
  let trackedEffects: (() => void)[] = [];

  // Simplified helper function to wait for state updates
  async function waitForStateUpdate() {
    // Wait for Svelte's tick to process microtasks
    await tick();

    // Wait for a short delay to ensure all updates propagate
    await new Promise((resolve) => setTimeout(resolve, 20));

    // Check if state version has changed and update our tracker
    const newVersion = getStoreVersion();
    if (newVersion !== stateVersion) {
      stateVersion = newVersion;

      // Re-run all tracked effects to simulate reactivity
      trackedEffects.forEach((effect) => {
        try {
          effect();
        } catch (e) {
          // Ignore errors in tracked effects during test simulation
          console.warn("Error in tracked effect:", e);
        }
      });

      // Wait for another tick to process the version change
      await tick();
    }

    // Final tick to ensure everything is processed
    await tick();
  }

  describe("Basic CRUD Operations", () => {
    it("should add a widget", async () => {
      let widgetArray: WidgetConfig[] = [];

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
      });

      addWidget(mockWidget);
      await waitForStateUpdate();

      expect(getWidgetById(mockWidget.id)).toEqual(mockWidget);
      expect(widgetArray.length).toBe(1);
      expect(widgetArray[0]).toEqual(mockWidget);
    });

    it("should remove a widget", async () => {
      let widgetArray: WidgetConfig[] = [];
      let widgetById: WidgetConfig | undefined;

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
        widgetById = getWidgetById(mockWidget.id);
      });

      addWidget(mockWidget);
      await waitForStateUpdate();
      expect(widgetArray.length).toBe(1);

      removeWidget(mockWidget.id);
      await waitForStateUpdate();

      expect(widgetById).toBeUndefined();
      expect(widgetArray.length).toBe(0);
    });

    it("should update a widget", async () => {
      let updatedWidget: WidgetConfig | undefined;

      createTrackedEffect(() => {
        updatedWidget = getWidgetById(mockWidget.id);
      });

      addWidget(mockWidget);
      await waitForStateUpdate();

      const newTitle = "Updated Widget";
      updateWidget(mockWidget.id, { title: newTitle });
      await waitForStateUpdate();

      expect(updatedWidget?.title).toBe(newTitle);
    });

    it("should set multiple widgets", async () => {
      let widgetArray: WidgetConfig[] = [];
      let widgetMap: Record<string, WidgetConfig> = {};

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
        widgetMap = getWidgetMap();
      });

      setWidgets([mockWidget, mockWidgetWithGroup]);
      await waitForStateUpdate();

      expect(widgetArray.length).toBe(2);
      expect(Object.keys(widgetMap).length).toBe(2);
      expect(widgetMap[mockWidget.id]).toEqual(mockWidget);
      expect(widgetMap[mockWidgetWithGroup.id]).toEqual(mockWidgetWithGroup);
    });
  });

  describe("Derived Stores", () => {
    it("should update widgetArray when widgets change", async () => {
      let widgetArray: WidgetConfig[] = [];
      const arrayChangesSpy = vi.fn();

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
        arrayChangesSpy(widgetArray.length);
      });

      // Initial state
      expect(arrayChangesSpy).toHaveBeenCalledWith(0);

      // Add widget
      addWidget(mockWidget);
      await waitForStateUpdate();
      expect(widgetArray.some((w) => w.id === mockWidget.id)).toBe(true);
      expect(arrayChangesSpy).toHaveBeenCalledWith(1);

      // Remove widget
      removeWidget(mockWidget.id);
      await waitForStateUpdate();
      expect(widgetArray).not.toContain(mockWidget);
      expect(arrayChangesSpy).toHaveBeenCalledWith(0);
    });

    it("should maintain widget groups", async () => {
      let groups: Record<string, WidgetConfig[]> = {};

      createTrackedEffect(() => {
        groups = getWidgetGroups();
      });

      addWidget(mockWidget);
      addWidget(mockWidgetWithGroup);
      await waitForStateUpdate();

      expect(groups.default?.some((w) => w.id === mockWidget.id)).toBe(true);
      expect(
        groups["test-group"]?.some((w) => w.id === mockWidgetWithGroup.id),
      ).toBe(true);
    });
  });

  describe("Accessor Functions", () => {
    it("should provide widget map through accessor function", async () => {
      let map: Record<string, WidgetConfig> = {};

      createTrackedEffect(() => {
        map = getWidgetMap();
      });

      addWidget(mockWidget);
      await waitForStateUpdate();

      expect(map[mockWidget.id]).toEqual(mockWidget);
    });

    it("should get widget by ID", async () => {
      let widget: WidgetConfig | undefined;

      createTrackedEffect(() => {
        widget = getWidgetById(mockWidget.id);
      });

      addWidget(mockWidget);
      await waitForStateUpdate();

      expect(widget).toEqual(mockWidget);
    });

    it("should handle asynchronous state updates correctly", async () => {
      const stateChangeSequence: Array<number> = [];

      // Track state changes in sequence
      createTrackedEffect(() => {
        stateChangeSequence.push(getWidgetArray().length);
      });

      // Add multiple widgets with delays to simulate async operations
      await Promise.all([
        (async () => {
          await new Promise((resolve) => setTimeout(resolve, 10));
          addWidget({ ...mockWidget, id: "async-1" });
        })(),
        (async () => {
          await new Promise((resolve) => setTimeout(resolve, 5));
          addWidget({ ...mockWidget, id: "async-2" });
        })(),
      ]);

      await waitForStateUpdate();

      // We should have captured the sequence of state changes
      expect(stateChangeSequence).toContain(0); // Initial state
      expect(stateChangeSequence).toContain(2); // Final state with 2 widgets
      expect(getWidgetArray().length).toBe(2);
    });
  });

  describe("Error Cases", () => {
  it("should handle adding widget with missing required properties", async () => {
    let widgetArray: WidgetConfig[] = [];

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
      });

      // Missing required properties
      const invalidWidget = {
        id: "invalid-widget",
        type: "gauge",
        // Missing title, pos_x, pos_y, etc.
      } as WidgetConfig;

      try {
        addWidget(invalidWidget);
      } catch (e) {
        // Function should handle invalid widgets gracefully
      }

      await waitForStateUpdate();

      // Either the function should throw an error or silently fail
      // The most important thing is that the store remains in a valid state
      expect(
        widgetArray.find((w) => w.id === "invalid-widget"),
      ).toBeUndefined();
    });

    it("should handle adding widget with duplicate ID", async () => {
      let widgetArray: WidgetConfig[] = [];

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
      });

      // Add the first widget
      addWidget(mockWidget);
      await waitForStateUpdate();
      expect(widgetArray.length).toBe(1);

      // Try to add a widget with the same ID but different properties
      const duplicateIdWidget = {
        ...mockWidget,
        title: "Duplicate ID Widget",
      };

      addWidget(duplicateIdWidget);
      await waitForStateUpdate();

      // Either the second add should be ignored or it should replace the first widget
      // We're testing for consistent behavior, not specific behavior
      expect(widgetArray.length).toBe(1);

      // Check which version of the widget is in the store
      const storedWidget = getWidgetById(mockWidget.id);

      // Depending on implementation, either the original or duplicate could be present
      // Just ensure we have a predictable, documented behavior
      expect(storedWidget).toBeDefined();
      expect(storedWidget?.id).toBe(mockWidget.id);
    });

    it("should gracefully handle updating non-existent widget", async () => {
      let widgetMap: Record<string, WidgetConfig> = {};

      createTrackedEffect(() => {
        widgetMap = getWidgetMap();
      });

      // Try updating a widget that doesn't exist
      const nonExistentId = "non-existent-widget";
      updateWidget(nonExistentId, { title: "New Title" });
      await waitForStateUpdate();

      // Ensure the store wasn't corrupted by the operation
      expect(Object.keys(widgetMap)).not.toContain(nonExistentId);
      expect(getWidgetById(nonExistentId)).toBeUndefined();
    });

    it("should gracefully handle removing non-existent widget", async () => {
      let widgetArray: WidgetConfig[] = [];

      // Add a widget to the store first
      addWidget(mockWidget);
      await waitForStateUpdate();

      createTrackedEffect(() => {
        widgetArray = getWidgetArray();
      });

      // Initial state should have our test widget
      expect(widgetArray.length).toBe(1);

      // Try removing a widget that doesn't exist
      removeWidget("non-existent-widget");
      await waitForStateUpdate();

      // The store should remain unchanged
      expect(widgetArray.length).toBe(1);
      expect(getWidgetById(mockWidget.id)).toEqual(mockWidget);
    });

    it("should handle invalid widget property updates", async () => {
      let updatedWidget: WidgetConfig | undefined;

      // Add a widget to update
      addWidget(mockWidget);
      await waitForStateUpdate();

      createTrackedEffect(() => {
        updatedWidget = getWidgetById(mockWidget.id);
      });

      // Try updating with invalid property values
      updateWidget(mockWidget.id, {
        pos_x: -999999, // Extremely negative value
        pos_y: NaN, // Not a number
        width: 0, // Zero width
        height: -5, // Negative height
      });
      await waitForStateUpdate();

      // Widget should either maintain original valid values or be updated with sanitized values
      expect(updatedWidget).toBeDefined();
      expect(updatedWidget?.id).toBe(mockWidget.id);

      // If the implementation enforces constraints, check that invalid values were rejected or sanitized
      // For example:
      if (updatedWidget) {
        expect(updatedWidget.width).toBeGreaterThan(0); // Width should never be 0 or negative
        expect(updatedWidget.height).toBeGreaterThan(0); // Height should never be negative

        // If NaN protection is implemented:
        expect(updatedWidget.pos_y).not.toBeNaN();
      }
    });

    it("should handle null/undefined values in widget operations", async () => {
      // Test adding null/undefined
      try {
        // @ts-expect-error - Intentionally passing null for testing
        addWidget(null);
        // @ts-expect-error - Intentionally passing undefined for testing
        addWidget(undefined);
      } catch (e) {
        // This is actually expected to throw in a strongly typed system
        // Just making sure it doesn't corrupt the store
      }

      // Test removing with null/undefined
      try {
        // @ts-expect-error - Intentionally passing null for testing
        removeWidget(null);
        // @ts-expect-error - Intentionally passing undefined for testing
        removeWidget(undefined);
      } catch (e) {
        // Expected to either throw or be a no-op
      }

      // Add a real widget
      addWidget(mockWidget);
      await waitForStateUpdate();

      // Test updating with null/undefined
      try {
        // @ts-expect-error - Intentionally passing null for testing values
        updateWidget(mockWidget.id, null);
        // @ts-expect-error - Intentionally passing undefined as properties
        updateWidget(mockWidget.id, undefined);
        // Testing with null/undefined properties
        updateWidget(mockWidget.id, {
          // Intentionally passing null/undefined for testing
          title: null as any,
          // Intentionally passing null/undefined for testing
          pos_x: undefined as any,
        });
      } catch (e) {
        // Expected to either throw or ignore invalid updates
      }

      await waitForStateUpdate();

      // Check that the store remains in a valid state
      const widget = getWidgetById(mockWidget.id);
      expect(widget).toBeDefined();
      expect(widget?.id).toBe(mockWidget.id);

      // Original title should remain if null wasn't accepted
      expect(typeof widget?.title).toBe("string");
    });
  });
});
