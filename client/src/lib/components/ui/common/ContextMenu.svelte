<script lang="ts">
	import { ui } from '$lib/stores/core/ui.svelte';
	import { actions } from '$lib/services/actions.svelte';
	import type { ContextMenuItem } from '$lib/types/ui';

	let { x, y, items, dispatch } = $props<{
		x: number;
		y: number;
		items: ContextMenuItem[];
		dispatch: (event: 'context-action', detail: { action: string }) => void;
	}>();

	let menu: HTMLDivElement | undefined;
	let adjustedX = $state(x);
	let adjustedY = $state(y);

	$effect(() => {
		if (menu) {
			const rect = menu.getBoundingClientRect();
			if (x + rect.width > window.innerWidth) {
				adjustedX = window.innerWidth - rect.width - 10;
			}
			if (y + rect.height > window.innerHeight) {
				adjustedY = window.innerHeight - rect.height - 10;
			}
		}

		const handleClickOutside = (event: MouseEvent) => {
			if (menu && !menu.contains(event.target as Node)) {
				ui.hideContextMenu();
			}
		};

		document.addEventListener('mousedown', handleClickOutside);
		return () => document.removeEventListener('mousedown', handleClickOutside);
	});

	function handleAction(item: ContextMenuItem) {
		if (item.disabled) return;

		switch (item.action) {
			case 'add-widget':
				actions.addNewWidget();
				break;
			case 'cut-widget':
				actions.cutSelectedWidgets();
				break;
			case 'copy-widget':
				actions.copySelectedWidgets();
				break;
			case 'paste-widget':
				actions.pasteWidgets();
				break;
			case 'delete-widget':
				actions.deleteSelectedWidgets();
				break;
			case 'bring-front':
				actions.bringToFront();
				break;
			case 'send-back':
				actions.sendToBack();
				break;
		}

		dispatch('context-action', { action: item.action });
		ui.hideContextMenu();
	}
</script>

<div
	bind:this={menu}
	class="context-menu"
	style:left="{adjustedX}px"
	style:top="{adjustedY}px"
>
	{#each items as item}
		{#if item.type === 'separator'}
			<div class="separator"></div>
		{:else}
			<button
				class="menu-item"
				class:disabled={item.disabled}
				onclick={() => handleAction(item)}
				disabled={item.disabled}
			>
				{item.label}
			</button>
		{/if}
	{/each}
</div>

<style>
	.context-menu {
		position: fixed;
		z-index: 1000;
		background-color: var(--theme-surface-overlay);
		border: 1px solid var(--theme-border);
		border-radius: 0.5rem;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		padding: 0.5rem;
		min-width: 150px;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.menu-item {
		display: flex;
		align-items: center;
		padding: 0.5rem;
		border-radius: 0.25rem;
		background-color: transparent;
		color: var(--theme-text);
		border: none;
		cursor: pointer;
		width: 100%;
		text-align: left;
		font-size: 0.875rem;
		transition: background-color 0.1s ease-in-out;
	}

	.menu-item:not(.disabled):hover {
		background-color: var(--theme-surface-hover);
	}

	.menu-item.disabled {
		color: var(--theme-text-muted);
		cursor: not-allowed;
	}

	.separator {
		height: 1px;
		background-color: var(--theme-border);
		margin: 0.5rem 0;
	}
</style>
