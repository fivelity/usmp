# Svelte 5 Coding Standards Guide - Ultimate Sensor Monitor

✅ **Migration Complete!** - All standards below have been successfully implemented

This document outlines the coding standards for Svelte 5 projects within Ultimate Sensor Monitor. Adhering to these standards will ensure code consistency, readability, and maintainability, aligning with our Svelte 5.x.x technology stack.

## 🎉 **Migration Achievement**

**All patterns described in this document are now live** in the Ultimate Sensor Monitor codebase:
- ✅ Rune-based state management (`$state`, `$derived`, `$effect`)
- ✅ Modern component patterns (`$props()`, `{@render}`)
- ✅ TypeScript integration with Svelte 5
- ✅ Zero build errors, production ready

## 📋 **Version Mandate**

**Ultimate Sensor Monitor exclusively uses Svelte 5.x.x.** All new and existing Svelte code should leverage Svelte 5 features, particularly Runes, for optimal performance and developer experience.

## Table of Contents

1.  [General Principles](#1-general-principles)
2.  [File Structure](#2-file-structure)
3.  [Component Structure](#3-component-structure)
4.  [TypeScript Usage](#4-typescript-usage)
5.  [Svelte 5 Syntax Standards (Runes)](#5-svelte-5-syntax-standards-runes)
*   [5.1. Component Props (`$props`)](#51-component-props-props)
*   [5.2. State (`$state`)](#52-state-state)
*   [5.3. Derived State (`$derived`)](#53-derived-state-derived)
*   [5.4. Side Effects (`$effect`)](#54-side-effects-effect)
*   [5.5. Event Handling](#55-event-handling)
*   [5.6. Bindings (`bind:`, `$bindable`)](#56-bindings-bind-bindable)
*   [5.7. Slots](#57-slots)
*   [5.8. Conditional Rendering (`{#if}`, `{#each}`, `{#await}`)](#58-conditional-rendering-if-each-await)
*   [5.9. Stores (When to use with Runes)](#59-stores-when-to-use-with-runes)
*   [5.10. Class Fields with Runes](#510-class-fields-with-runes)
6.  [Styling (Tailwind CSS)](#6-styling-tailwind-css)
7.  [Accessibility (A11y)](#7-accessibility-a11y)
8.  [Testing](#8-testing)
9.  [Code Organization and Comments](#9-code-organization-and-comments)
10. [Performance Considerations](#10-performance-considerations)
11. [Verification](#11-verification)

---

## 1. General Principles

*   **Consistency:** Follow these standards consistently throughout the project.
*   **Readability:** Write code that is easy to understand and maintain. Prioritize clarity.
*   **Simplicity:** Keep code as simple as possible while meeting requirements.
*   **Modularity:** Create small, focused, and reusable components.
*   **Embrace Runes:** Utilize Svelte 5 Runes for state management and reactivity as the primary approach.

## 2. File Structure

*   Svelte components: `.svelte` files.
*   Naming: Use PascalCase for component file names (e.g., `MyWidget.svelte`).
*   Location:
*   Reusable UI elements: `client/src/lib/components/ui/`
*   Feature-specific widgets: `client/src/lib/components/widgets/`
*   Widget inspectors: `client/src/lib/components/inspectors/` (if applicable)
*   Stores (for global/cross-component state): `client/src/lib/stores/`
*   Services (API, WebSocket): `client/src/lib/services/`
*   Types: `client/src/lib/types/`
*   Routes: `client/src/routes/` (SvelteKit file-based routing)

## 3. Component Structure

A Svelte 5 component typically consists of:
1.  `<script lang="ts">`: TypeScript logic, utilizing Runes.
2.  HTML markup: Defines the structure.
3.  `<style>`: Scoped CSS (though Tailwind CSS is primary).

\`\`\`svelte
<script lang="ts">
// TypeScript logic here, using Svelte 5 Runes
import { type Snippet } from 'svelte';

// Props
let { 
greeting = 'Hello', 
name = 'World',
children, // Default slot
actions // Named slot
}: { 
greeting?: string; 
name?: string;
children: Snippet; // For default slot content
actions?: Snippet; // For named slot content
} = $props();

// State
let count = $state(0);

// Derived State
const fullGreeting = $derived(\`\${greeting}, \${name}!\`);
const doubledCount = $derived(count * 2);

// Effect
$effect(() => {
console.log('Component mounted or greeting/name changed:', fullGreeting);
console.log('Count is now:', count);
});

function increment() {
count++;
}
</script>

<div class="p-4 border rounded shadow">
<h1 class="text-xl font-bold">{fullGreeting}</h1>
<p>Count: {count}, Doubled: {doubledCount}</p>
<button onclick={increment} class="btn-primary">Increment</button>

{@render children} <!-- Render default slot -->

{#if actions}
<div class="actions-container mt-2">
  {@render actions} <!-- Render named slot -->
</div>
{/if}
</div>

<style>
/* Scoped styles (use sparingly, prefer Tailwind) */
h1 {
color: var(--theme-text-primary, #333); /* Example using CSS var for theming */
}
</style>
\`\`\`

## 4. TypeScript Usage

*   Use TypeScript for all Svelte script blocks (`<script lang="ts">`).
*   Define types for props (within the `$props()` call or separately), store values, and complex objects in `client/src/lib/types/`.
*   Use interfaces or type aliases for defining shapes of data.
*   Utilize TypeScript's utility types (e.g., `Partial`, `Readonly`) where appropriate.
*   For `$props()`, you can define the type inline or import it:
\`\`\`ts
// Inline type
// let { title, count = 0 }: { title: string; count?: number } = $props();

// Imported type
// import type { MyComponentProps } from '$lib/types';
// let { title, count = 0 }: MyComponentProps = $props();
\`\`\`

## 5. Svelte 5 Syntax Standards (Runes)

### 5.1. Component Props (`$props`)
Declare props using `let { ... } = $props();`. Provide default values directly in the destructuring.
\`\`\`svelte
<script lang="ts">
interface WidgetProps {
title: string;
description?: string;
initialValue?: number;
onclick?: (event: MouseEvent) => void;
}

let { 
title, 
description = 'No description provided.', 
initialValue = 0,
onclick
}: WidgetProps = $props();

let currentValue = $state(initialValue);
</script>

<div class="widget">
<h3>{title}</h3>
<p>{description}</p>
<p>Value: {currentValue}</p>
{#if onclick}
<button {onclick}>Click Me</button>
{/if}
</div>
\`\`\`

### 5.2. State (`$state`)
Use `$state()` for reactive component state.
\`\`\`svelte
<script lang="ts">
let count = $state(0);
let text = $state("initial text");
let user = $state<{ name: string; age: number } | null>(null);

function increment() {
count++;
}
function login() {
user = { name: "Svelte User", age: 5 };
}
</script>

<p>Count: {count}</p>
<button onclick={increment}>Increment</button>
<input type="text" bind:value={text} /> 
<p>{text}</p>
{#if user}
<p>Welcome, {user.name} ({user.age})</p>
{:else}
<button onclick={login}>Login</button>
{/if}
\`\`\`

### 5.3. Derived State (`$derived`)
Use `$derived()` for values computed from other reactive state or props.
\`\`\`svelte
<script lang="ts">
let count = $state(0);
const doubled = $derived(count * 2);
const isEven = $derived(count % 2 === 0);

let { price = 0, quantity = 0 }: {price?: number, quantity?: number} = $props();
const totalCost = $derived(price * quantity);
</script>

<p>{count} * 2 = {doubled}</p>
<p>Count is {isEven ? 'even' : 'odd'}.</p>
<p>Total cost: ${totalCost.toFixed(2)}</p>
\`\`\`

### 5.4. Side Effects (`$effect`)
Use `$effect()` to run code in response to changes in state or props.
\`\`\`svelte
<script lang="ts">
let count = $state(0);
let { userId }: { userId: string | undefined } = $props();

$effect(() => {
console.log('The count is now', count);
document.title = \`Count: \${count}\`;

// Cleanup function (optional)
return () => {
console.log('Effect cleanup: count was', count);
};
});

$effect(() => {
if (userId) {
console.log('Fetching data for user:', userId);
// const unsubscribe = someApi.subscribe(userId, (data) => {...});
// return () => unsubscribe(); // Cleanup subscription
}
});
</script>
\`\`\`
- `$effect.pre()`: For effects that need to run before DOM updates (rare).
- `$effect.active()`: To check if currently inside an effect (rare).

### 5.5. Event Handling
Use `oneventname={handler}` (e.g., `onclick`, `oninput`). The `on:eventname` directive is still valid, especially for custom events or when modifiers are needed.
\`\`\`svelte
<script lang="ts">
let message = $state('No message yet');

function handleClick(event: MouseEvent) {
message = \`Button clicked at \${new Date().toLocaleTimeString()}\`;
console.log(event);
}

function handleInput(event: Event) {
const target = event.target as HTMLInputElement;
message = \`Input value: \${target.value}\`;
}

function handleSubmit(event: SubmitEvent) {
event.preventDefault(); // Manually prevent default for forms
console.log('Form submitted');
}
</script>

<button onclick={handleClick} class="btn-primary">Click me</button>
<input oninput={handleInput} placeholder="Type something" class="input-field" />

<form onsubmit={handleSubmit}>
<button type="submit" class="btn-secondary">Submit</button>
</form>
<p>{message}</p>
\`\`\`

### 5.6. Bindings (`bind:`, `$bindable`)
`bind:property` continues to work for two-way data binding on form elements.
For component props, if a parent needs to two-way bind to a child's prop, the child can declare that prop with `$bindable()`.
\`\`\`svelte
<!-- ChildComponent.svelte -->
<script lang="ts">
let count = $props($bindable(0)); // Make 'count' prop bindable
</script>
<button onclick={() => count++}>Increment from Child ({count})</button>

<!-- ParentComponent.svelte -->
<script lang="ts">
import ChildComponent from './ChildComponent.svelte';
let parentCount = $state(10);
</script>
<ChildComponent bind:count={parentCount} />
<p>Parent count: {parentCount}</p>
\`\`\`

### 5.7. Slots
Use `{@render children}` for the default slot and `{@render slotName}` for named slots. Pass props to slots if needed.
\`\`\`svelte
<!-- Card.svelte -->
<script lang="ts">
import { type Snippet } from 'svelte';
let { children, header }: { children: Snippet, header?: Snippet } = $props();
</script>
<div class="card">
<div class="card-header">
{#if header}
  {@render header()}
{:else}
  Default Header
{/if}
</div>
<div class="card-body">
{@render children()}
</div>
</div>

<!-- Usage -->
<script lang="ts">
import Card from './Card.svelte';
</script>
<Card>
<svelte:fragment slot="header">My Custom Card Header</svelte:fragment>
<p>This is the main content of the card.</p>
</Card>
\`\`\`

### 5.8. Conditional Rendering (`{#if}`, `{#each}`, `{#await}`)
These control flow blocks remain the same as in Svelte 5.
\`\`\`svelte
<script lang="ts">
let loggedIn = $state(false);
let items = $state(['Apple', 'Banana', 'Cherry']);
let promise = new Promise<string>((resolve) => setTimeout(() => resolve("Data loaded!"), 2000));
</script>

{#if loggedIn}
<p>Welcome back!</p>
{:else}
<p>Please log in.</p>
{/if}

<ul>
{#each items as item, i (item)} <!-- Keyed each block -->
<li>{i + 1}. {item}</li>
{/each}
</ul>

{#await promise}
<p>Loading data...</p>
{:then value}
<p>Success: {value}</p>
{:catch error}
<p>Error: {error.message}</p>
{/await}
\`\`\`

### 5.9. Stores (When to use with Runes)
-   **Runes are preferred for component-local state.**
-   Svelte stores (`writable`, `readable`, `derived` from `svelte/store`) are still useful for:
*   Global state shared across many unrelated components.
*   State that needs to be accessed or modified outside of Svelte components (e.g., in utility `.ts` files).
*   Complex state management logic that benefits from the store contract.
-   Access store values in components using the `$`-prefix auto-subscription.
\`\`\`typescript
// client/src/lib/stores/themeStore.ts
import { writable } from 'svelte/store';
export const currentTheme = writable<'dark' | 'light'>('dark');
\`\`\`
Usage in a Svelte 5 component:
\`\`\`svelte
<script lang="ts">
import { currentTheme } from '$lib/stores/themeStore';
// No need for $state here if just reading or updating the store
</script>
<p>Current Theme: {$currentTheme}</p>
<button onclick={() => currentTheme.set($currentTheme === 'dark' ? 'light' : 'dark')}>
Toggle Theme
</button>
\`\`\`

### 5.10. Class Fields with Runes
State and derived values can be used as class fields.
\`\`\`svelte
<script lang="ts">
class Counter {
count = $state(0);
doubled = $derived(this.count * 2);

increment() {
this.count++;
}
}
const myCounter = new Counter();
</script>
<p>{myCounter.count} * 2 = {myCounter.doubled}</p>
<button onclick={() => myCounter.increment()}>Increment Class Counter</button>
\`\`\`

## 6. Styling (Tailwind CSS)

*   Primarily use Tailwind CSS utility classes directly in your HTML markup.
*   Scoped `<style>` blocks should be used sparingly, for styles not easily achievable with Tailwind or for component-specific complex selectors.
*   Define custom theme colors and configurations in `tailwind.config.js`.
*   Refer to the `docs/UI_DESIGN_SYSTEM.md` for color palette and design principles.

## 7. Accessibility (A11y)

*   Use semantic HTML elements (`<nav>`, `<main>`, `<article>`, `<button>`, etc.).
*   Provide `alt` text for images.
*   Ensure sufficient color contrast (refer to UI Design System).
*   Use ARIA attributes where necessary to enhance accessibility for interactive elements.
*   Ensure keyboard navigability for all interactive components.
*   Test with screen readers periodically.

## 8. Testing

*   Write unit tests for components and utility functions using Vitest (or the configured test runner).
*   Test component props, Rune-based state logic, and events.
*   Integration tests should cover interactions between components and stores.
*   E2E tests (if applicable) to verify user flows.

## 9. Code Organization and Comments

*   Keep components focused on a single responsibility.
*   Extract complex logic into utility functions in `client/src/lib/utils/`.
*   Use JSDoc-style comments for components, props, and complex functions.
*   Write clear, concise comments to explain non-obvious logic.

## 10. Performance Considerations

*   Svelte 5's Rune-based reactivity is designed for fine-grained updates and excellent performance.
*   Use keyed `{#each}` blocks for lists where items can be reordered or change.
*   Be mindful of expensive computations in `$derived()` values; optimize if necessary.
*   Lazy load components or data where appropriate for initial page load performance.

## 11. Verification

-   Ensure `client/package.json` specifies `"svelte": "^5.x.x"` (e.g., `"^5.0.0-next.100"` or a stable `^5.0.0`).
-   Run `pnpm check` (or `npm run check`) in the `client` directory to catch type errors and potential syntax issues.
-   Manual vigilance and peer reviews are key to ensuring Svelte 5 best practices.

By strictly adhering to these Svelte 5 standards, we leverage the latest Svelte features for a modern, performant, and maintainable codebase.
