/**
 * This is a legacy Svelte 3/4 store. It should be refactored to use Svelte 5 runes.
 * The store manages the state of the sidebar, including the search term and selected categories.
 */

let searchTerm = $state("");
let categories = $state(new Set<string>());

export const sidebarStore = {
  get searchTerm() {
    return searchTerm;
  },
  setSearchTerm: (value: string) => {
    searchTerm = value;
  },

  get categories() {
    return categories;
  },

  isSelected: (category: string) => {
    return categories.has(category);
  },

  toggleCategory: (category: string) => {
    if (categories.has(category)) {
      categories.delete(category);
    } else {
      categories.add(category);
    }
  },

  clearFilters: () => {
    searchTerm = "";
    categories = new Set<string>();
  },
};
