function createUIState() {
  let leftSidebarVisible = $state(true);
  let rightSidebarVisible = $state(false);
  let editMode = $state<'view' | 'edit'>('view');

  return {
    get leftSidebarVisible() { return leftSidebarVisible; },
    get rightSidebarVisible() { return rightSidebarVisible; },
    get editMode() { return editMode; },

    toggleLeftSidebar: () => {
      leftSidebarVisible = !leftSidebarVisible;
    },
    toggleRightSidebar: () => {
      rightSidebarVisible = !rightSidebarVisible;
    },
    setEditMode: (mode: 'view' | 'edit') => {
      editMode = mode;
    },
    toggleEditMode: () => {
      editMode = editMode === 'view' ? 'edit' : 'view';
    }
  };
}

export const uiState = createUIState(); 