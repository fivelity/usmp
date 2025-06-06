<!-- NotificationCenter.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition';
  import { notifications, type Notification, type NotificationCategory } from '$lib/stores/notifications';
  import Badge from './common/Badge.svelte';

  export let position: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' = 'top-right';
  export let maxNotifications = 50;
  export let className = '';

  let isOpen = false;
  let activeCategory: NotificationCategory | 'all' = 'all';
  let showRead = true;

  $: filteredNotifications = $notifications
    .filter(n => (activeCategory === 'all' || n.category === activeCategory) && (showRead || !n.read))
    .slice(0, maxNotifications);

  $: unreadCount = $notifications.filter(n => !n.read).length;

  $: positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4'
  }[position];

  function handleCategoryChange(category: NotificationCategory | 'all') {
    activeCategory = category;
  }

  function handleToggleRead() {
    showRead = !showRead;
  }

  function handleMarkAllAsRead() {
    notifications.markAllAsRead();
  }

  function handleClearAll() {
    if (activeCategory === 'all') {
      notifications.clear();
    } else {
      notifications.clearByCategory(activeCategory as NotificationCategory);
    }
  }

  function formatTimestamp(timestamp: number) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  }
</script>

<div class="notification-center {positionClasses} {className}">
  <button
    class="notification-trigger"
    on:click={() => (isOpen = !isOpen)}
    aria-label="Toggle notifications"
  >
    <i class="fas fa-bell" />
    {#if unreadCount > 0}
      <Badge variant="error" size="sm" class="notification-badge">
        {unreadCount}
      </Badge>
    {/if}
  </button>

  {#if isOpen}
    <div
      class="notification-panel"
      transition:fly={{ y: 10, duration: 200 }}
    >
      <div class="notification-header">
        <h3 class="notification-title">Notifications</h3>
        <div class="notification-actions">
          <button
            class="btn btn-secondary"
            on:click={handleToggleRead}
            aria-label={showRead ? 'Hide read notifications' : 'Show read notifications'}
          >
            <i class="fas {showRead ? 'fa-eye-slash' : 'fa-eye'}" />
          </button>
          <button
            class="btn btn-secondary"
            on:click={handleMarkAllAsRead}
            aria-label="Mark all as read"
          >
            <i class="fas fa-check-double" />
          </button>
          <button
            class="btn btn-secondary"
            on:click={handleClearAll}
            aria-label="Clear all notifications"
          >
            <i class="fas fa-trash" />
          </button>
        </div>
      </div>

      <div class="notification-filters">
        <button
          class="filter-btn {activeCategory === 'all' ? 'active' : ''}"
          on:click={() => handleCategoryChange('all')}
        >
          All
        </button>
        <button
          class="filter-btn {activeCategory === 'system' ? 'active' : ''}"
          on:click={() => handleCategoryChange('system')}
        >
          System
        </button>
        <button
          class="filter-btn {activeCategory === 'sensor' ? 'active' : ''}"
          on:click={() => handleCategoryChange('sensor')}
        >
          Sensors
        </button>
        <button
          class="filter-btn {activeCategory === 'alert' ? 'active' : ''}"
          on:click={() => handleCategoryChange('alert')}
        >
          Alerts
        </button>
        <button
          class="filter-btn {activeCategory === 'user' ? 'active' : ''}"
          on:click={() => handleCategoryChange('user')}
        >
          User
        </button>
      </div>

      <div class="notification-list custom-scrollbar">
        {#if filteredNotifications.length === 0}
          <div class="notification-empty">
            <i class="fas fa-bell-slash" />
            <p>No notifications</p>
          </div>
        {:else}
          {#each filteredNotifications as notification (notification.id)}
            <div
              class="notification-item {notification.read ? 'read' : ''}"
              transition:fade
            >
              <div class="notification-icon">
                <i class="fas {notification.type === 'info' ? 'fa-info-circle' :
                  notification.type === 'success' ? 'fa-check-circle' :
                  notification.type === 'warning' ? 'fa-exclamation-triangle' :
                  'fa-times-circle'}" />
              </div>
              <div class="notification-content">
                <div class="notification-header">
                  <h4 class="notification-title">{notification.title}</h4>
                  <span class="notification-time">
                    {formatTimestamp(notification.timestamp)}
                  </span>
                </div>
                <p class="notification-message">{notification.message}</p>
                {#if notification.actions}
                  <div class="notification-actions">
                    {#each notification.actions as action}
                      <button
                        class="btn btn-secondary"
                        on:click={action.handler}
                      >
                        {action.label}
                      </button>
                    {/each}
                  </div>
                {/if}
              </div>
              {#if !notification.read}
                <button
                  class="notification-mark-read"
                  on:click={() => notifications.markAsRead(notification.id)}
                  aria-label="Mark as read"
                >
                  <i class="fas fa-check" />
                </button>
              {/if}
            </div>
          {/each}
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .notification-center {
    @apply fixed z-50;
  }

  .notification-trigger {
    @apply relative p-2 rounded-full hover:bg-surface-hover transition-colors;
  }

  .notification-badge {
    @apply absolute -top-1 -right-1;
  }

  .notification-panel {
    @apply absolute mt-2 w-96 bg-surface rounded-lg shadow-lg border border-border;
  }

  .notification-header {
    @apply flex items-center justify-between p-4 border-b border-border;
  }

  .notification-title {
    @apply text-lg font-medium;
  }

  .notification-actions {
    @apply flex items-center gap-2;
  }

  .notification-filters {
    @apply flex items-center gap-1 p-2 border-b border-border;
  }

  .filter-btn {
    @apply px-3 py-1 rounded-md text-sm font-medium text-text-muted hover:text-text transition-colors;
  }

  .filter-btn.active {
    @apply bg-primary/20 text-primary;
  }

  .notification-list {
    @apply max-h-[60vh] overflow-y-auto;
  }

  .notification-item {
    @apply flex items-start gap-3 p-4 border-b border-border hover:bg-surface-hover transition-colors;
  }

  .notification-item.read {
    @apply opacity-60;
  }

  .notification-icon {
    @apply text-lg;
  }

  .notification-content {
    @apply flex-1 min-w-0;
  }

  .notification-header {
    @apply flex items-center justify-between mb-1;
  }

  .notification-title {
    @apply text-sm font-medium;
  }

  .notification-time {
    @apply text-xs text-text-muted;
  }

  .notification-message {
    @apply text-sm text-text-muted;
  }

  .notification-mark-read {
    @apply p-1 hover:bg-surface-hover rounded-full transition-colors;
  }

  .notification-empty {
    @apply flex flex-col items-center justify-center p-8 text-text-muted;
  }

  .notification-empty i {
    @apply text-3xl mb-2;
  }

  /* Responsive adjustments */
  @media (max-width: 640px) {
    .notification-panel {
      @apply fixed inset-4 w-auto;
    }

    .notification-list {
      max-height: calc(100vh - 12rem);
    }
  }
</style> 