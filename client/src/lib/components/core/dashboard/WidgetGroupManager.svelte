<script lang="ts">
  
  import { widgetsStore } from '$lib/stores/data/widgets.svelte';
  import { selectedWidgets, storeUtils } from '$lib/stores';
  import {
    addWidget,
    updateWidget,
    addWidgetGroup,
    updateWidgetGroup
  } from '$lib/stores/data/widgets.svelte';
  import { Users, Download, Upload, Plus, Trash2, Edit2 } from '@lucide/svelte';
  import type { WidgetGroup, WidgetConfig } from '$lib/types';

  let showCreateDialog = $state(false);
  let editingGroup = $state<WidgetGroup | null>(null);
  let newGroupName = $state('');
  let newGroupDescription = $state('');
  let currentEditDescription = $state('');

  // Create a new group from selected widgets
  function createGroupFromSelection() {
    const selectedIds: string[] = Array.from(selectedWidgets);
    if (selectedIds.length < 2) {
      alert('Please select at least 2 widgets to create a group');
      return;
    }

    if (selectedIds.length === 0) { // Explicit check even if covered by < 2 for clarity
      alert('No widgets selected to form a group.');
      return;
    }
    const firstWidgetId = selectedIds[0];
    if (!firstWidgetId) { // Should be caught by earlier checks, but good for safety
      alert('Cannot identify the first selected widget.');
      return;
    }
    const firstWidget = $widgetsStore[firstWidgetId];
    if (!firstWidget) {
      alert('Selected widget data not found.');
      return;
    }
    // TODO: Re-evaluate if relative_positions are needed and how they should be stored/calculated
    // For now, focusing on core group creation matching the WidgetGroup type.
    // const relativePositions: Record<string, { x: number; y: number }> = {};
    // selectedIds.forEach((id: string) => {
    //   const widget = $widgets[id];
    //   if (widget && firstWidget) {
    //     relativePositions[id] = {
    //       x: widget.x - firstWidget.x,
    //       y: widget.y - firstWidget.y
    //     };
    //   }
    // });

    const group: WidgetGroup = {
      id: crypto.randomUUID(),
      name: newGroupName || `Group 1`,
      widget_ids: selectedIds,
      widgets: selectedIds,
      is_collapsed: false,
      // Initialize with a default layout; this can be adjusted later
      layout: { x: firstWidget.pos_x || firstWidget.x || 0, y: firstWidget.pos_y || firstWidget.y || 0, width: 200, height: 200 },
      metadata: { description: newGroupDescription }
      // metadata: { description: newGroupDescription, relative_positions: relativePositions, created_at: new Date().toISOString() }
    };

    // Update widgets to include group_id
    selectedIds.forEach(id => {
      updateWidget(id, { group_id: group.id });
    });

    addWidgetGroup(group);
    showCreateDialog = false;
    newGroupName = '';
    newGroupDescription = '';
  }

  // Ungroup widgets
  function ungroupWidgets(groupId: string) {
    // TODO: Implement actual widget groups store
    console.warn('Widget groups not yet implemented:', groupId);
    return;
  }

  // Export group as JSON
  function exportGroup(group: WidgetGroup) {
    const groupWidgets: WidgetConfig[] = group.widgets.map(id => $widgetsStore[id]).filter(Boolean) as WidgetConfig[];
    
    const exportData = {
      group,
      widgets: groupWidgets.map(widget => ({
        ...widget,
        x: (widget.x ?? widget.pos_x ?? 0) - (group.layout?.x || 0),
        y: (widget.y ?? widget.pos_y ?? 0) - (group.layout?.y || 0)
      })),
      version: '1.0',
      exported_at: new Date().toISOString()
    };

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${group.name.replace(/\s+/g, '_')}_group.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  // Import group from file
  function importGroup() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = (event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importData = JSON.parse(e.target?.result as string);
          
          if (importData.group && importData.widgets) {
            // Generate new IDs to avoid conflicts
            const oldToNewIds: Record<string, string> = {};
            const newGroup = { 
              ...importData.group, 
              id: crypto.randomUUID(),
              created_at: new Date().toISOString()
            };

            // Create new widgets with new IDs
            const newWidgets: WidgetConfig[] = importData.widgets.map((widget: WidgetConfig) => {
              const newId = crypto.randomUUID();
              oldToNewIds[widget.id] = newId;
              
              return {
                ...widget,
                id: newId,
                group_id: newGroup.id,
                // Position widgets in empty area
                x: (widget.x ?? widget.pos_x ?? 0) + 200,
                y: (widget.y ?? widget.pos_y ?? 0) + 200,
                pos_x: (widget.x ?? widget.pos_x ?? 0) + 200,
                pos_y: (widget.y ?? widget.pos_y ?? 0) + 200
              };
            });

            newGroup.widgets = Object.values(oldToNewIds);

            // Add widgets and group
            newWidgets.forEach((widget: WidgetConfig) => addWidget(widget));
            addWidgetGroup(newGroup);

            console.log('Successfully imported group:', newGroup.name);
          }
        } catch (error) {
          console.error('Failed to import group:', error);
          alert('Failed to import group. Please check the file format.');
        }
      };
      reader.readAsText(file);
    };
    
    input.click();
  }

  // Select all widgets in a group
  function selectGroup(group: WidgetGroup) {
    storeUtils.clearSelection();
    group.widgets.forEach((id: string) => storeUtils.selectWidget(id, true));
  }

  // Edit group
  function editGroup(group: WidgetGroup) {
    editingGroup = group;
    newGroupName = group.name; // newGroupName is for create, editingGroup.name is bound directly
    currentEditDescription = group.metadata?.description || '';
  }

  // Save changes to group
  function saveGroupChanges() {
    if (editingGroup) {
      updateWidgetGroup(editingGroup.id, {
        name: editingGroup.name,
        metadata: { ...editingGroup.metadata, description: currentEditDescription }
      });
      editingGroup = null;
    }
  }
</script>

<div class="p-4 space-y-4">
  <div class="flex items-center justify-between">
    <h3 class="text-lg font-semibold text-(--theme-text) flex items-center gap-2">
      <Users size={20} />
      Widget Groups
    </h3>
    
    <div class="flex items-center gap-2">
      <button
        onclick={() => showCreateDialog = true}
        disabled={selectedWidgets.size < 2}
        class="px-3 py-1 text-sm bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
        title="Create group from selected widgets"
      >
        <Plus size={14} />
        Create Group
      </button>
      
      <button
        onclick={importGroup}
        class="px-3 py-1 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600 flex items-center gap-1"
        title="Import group from file"
      >
        <Upload size={14} />
        Import
      </button>
    </div>
  </div>

  <!-- Groups List -->
  <div class="space-y-2">
    {#each ([] as WidgetGroup[]) as group (group.id)}
      <div class="border border-(--theme-border) rounded-lg p-3 bg-(--theme-surface)">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="font-medium text-(--theme-text)">
              {group.name}
            </div>
            {#if group.metadata?.description}
              <div class="text-xs text-(--theme-text-muted) mt-1">
                {group.metadata.description}
              </div>
            {/if}
            <div class="text-xs text-(--theme-text-muted) mt-2">
              {group.widgets.length} widget{group.widgets.length === 1 ? '' : 's'}
            </div>
          </div>
          
          <div class="flex items-center gap-1">
            <button
              onclick={() => selectGroup(group)}
              class="p-1 text-(--theme-text-muted) hover:text-(--theme-text) transition-colors"
              title="Select group widgets"
            >
              <Users size={14} />
            </button>
            
            <button
              onclick={() => exportGroup(group)}
              class="p-1 text-(--theme-text-muted) hover:text-(--theme-text) transition-colors"
              title="Export group"
            >
              <Download size={14} />
            </button>
            
            <button
              onclick={() => editGroup(group)}
              class="p-1 text-(--theme-text-muted) hover:text-(--theme-text) transition-colors"
              title="Edit group"
            >
              <Edit2 size={14} />
            </button>
            
            <button
              onclick={() => ungroupWidgets(group.id)}
              class="p-1 text-red-500 hover:text-red-600 transition-colors"
              title="Ungroup widgets"
            >
              <Trash2 size={14} />
            </button>
          </div>
        </div>
      </div>
    {:else}
      <div class="text-center py-8 text-(--theme-text-muted)">
        No groups created yet. Select multiple widgets and create a group.
      </div>
    {/each}
  </div>
</div>

<!-- Create Group Dialog -->
{#if showCreateDialog}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-(--theme-surface) rounded-lg p-6 w-96 border border-(--theme-border)">
      <h3 class="text-lg font-semibold text-(--theme-text) mb-4">Create Widget Group</h3>
      
      <div class="space-y-4">
        <div>
          <label for="newGroupNameInput" class="block text-sm font-medium text-(--theme-text) mb-1">
            Group Name
          </label>
          <input
            id="newGroupNameInput"
            bind:value={newGroupName}
            type="text"
            placeholder="Enter group name"
            class="w-full px-3 py-2 border border-(--theme-border) rounded-md bg-(--theme-background) text-(--theme-text)"
          />
        </div>
        
        <div>
          <label for="newGroupDescriptionInput" class="block text-sm font-medium text-(--theme-text) mb-1">
            Description (Optional)
          </label>
          <textarea
            id="newGroupDescriptionInput"
            bind:value={newGroupDescription}
            placeholder="Enter group description"
            rows="3"
            class="w-full px-3 py-2 border border-(--theme-border) rounded-md bg-(--theme-background) text-(--theme-text)"
          ></textarea>
        </div>
        
        <div class="text-sm text-(--theme-text-muted)">
          {selectedWidgets.size} widgets will be grouped together.
        </div>
      </div>
      
      <div class="flex justify-end gap-2 mt-6">
        <button
          onclick={() => showCreateDialog = false}
          class="px-4 py-2 text-(--theme-text) border border-(--theme-border) rounded-md hover:bg-(--theme-background)"
        >
          Cancel
        </button>
        <button
          onclick={createGroupFromSelection}
          class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
        >
          Create Group
        </button>
      </div>
    </div>
  </div>
{/if}

<!-- Edit Group Dialog -->
{#if editingGroup}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-(--theme-surface) rounded-lg p-6 w-96 border border-(--theme-border)">
      <h3 class="text-lg font-semibold text-(--theme-text) mb-4">Edit Group</h3>
      
      <div class="space-y-4">
        <div>
          <label for="editGroupNameInput" class="block text-sm font-medium text-(--theme-text) mb-1">
            Group Name
          </label>
          <input
            id="editGroupNameInput"
            bind:value={editingGroup.name}
            type="text"
            class="w-full px-3 py-2 border border-(--theme-border) rounded-md bg-(--theme-background) text-(--theme-text)"
          />
        </div>
        
        <div>
          <label for="editGroupDescriptionInput" class="block text-sm font-medium text-(--theme-text) mb-1">
            Description
          </label>
          <textarea
            id="editGroupDescriptionInput"
            bind:value={currentEditDescription}
            placeholder="Enter group description"
            rows="3"
            class="w-full px-3 py-2 border border-(--theme-border) rounded-md bg-(--theme-background) text-(--theme-text)"
          ></textarea>
        </div>
      </div>
      
      <div class="flex justify-end gap-2 mt-6">
        <button
          onclick={() => editingGroup = null}
          class="px-4 py-2 text-(--theme-text) border border-(--theme-border) rounded-md hover:bg-(--theme-background)"
        >
          Cancel
        </button>
        <button
          onclick={saveGroupChanges}
          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Save Changes
        </button>
      </div>
    </div>
  </div>
{/if}
