/**
 * Stores UI-related state for the application using Svelte 5 Runes.
 */

let searchTerm = $state('');
let categories = $state(new Set<string>());

export const sidebarStore = {
  get searchTerm() {
    return searchTerm;
  },
  setSearchTerm: (value: string) => {
    searchTerm = value;
  },

  get expandedCategories() {
    return categories;
  },
  toggleCategory: (category: string) => {
    if (categories.has(category)) {
      categories.delete(category);
    } else {
      categories.add(category);
    }
  }
}; 