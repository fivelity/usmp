/**
 * Stores UI-related state for the application.
 */

// Store for the search term entered in the sidebar
export let sidebarSearchTerm = $state('');

// Store for the currently expanded categories in the sidebar
export let expandedCategories = $state<Set<string>>(new Set()); 