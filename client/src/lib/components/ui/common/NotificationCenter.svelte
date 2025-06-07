<!-- NotificationCenter.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition';
  import { notifications, type NotificationCategoryType } from '$lib/stores/notifications';
  import Badge from './Badge.svelte';

  type Props = {
    position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
    maxNotifications?: number;
    className?: string;
  };
  let { position = 'top-right', maxNotifications = 50, className = '' }: Props = $props();

  let isOpen = $state(false);
  let activeCategory = $state<NotificationCategoryType | 'all'>('all');
  let showRead = $state(true);

  const filteredNotifications = $derived(() => {
    return $notifications
      .filter(n => (activeCategory === 'all' || n.category === activeCategory) && (showRead || !n.read))
      .slice(0, maxNotifications);
  });

  const unreadCount = $derived($notifications.filter(n => !n.read).length);

  const positionClasses = $derived(({
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4'
  })[position]);

  function handleCategoryChange(category: NotificationCategoryType | 'all') {
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
      notifications.clearByCategory(activeCategory as NotificationCategoryType);
    }
  }

  function formatTimestamp(timestamp: number) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  }
</script>

<div class="fixed z-50 {positionClasses} {className}">
  <button
    class="relative p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
    onclick={() => (isOpen = !isOpen)}
    aria-label="Toggle notifications"
  >
    <i class="fas fa-bell"></i>
    {#if unreadCount > 0}
      <Badge variant="error" size="sm" className="absolute -top-1 -right-1">
        {unreadCount}
      </Badge>
    {/if}
  </button>

  {#if isOpen}
    <div
      class="absolute mt-2 w-96 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700"
      transition:fly={{ y: 10, duration: 200 }}
    >
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Notifications</h3>
          <div class="flex space-x-2">
            <button
              class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              onclick={handleToggleRead}
              aria-label={showRead ? 'Hide read notifications' : 'Show read notifications'}
            >
              <i class="fas {showRead ? 'fa-eye-slash' : 'fa-eye'}"></i>
            </button>
            <button
              class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              onclick={handleMarkAllAsRead}
              aria-label="Mark all as read"
            >
              <i class="fas fa-check-double"></i>
            </button>
            <button
              class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              onclick={handleClearAll}
              aria-label="Clear all notifications"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <div class="flex space-x-2 p-2 border-b border-gray-200 dark:border-gray-700">
        <button
          class="px-3 py-1 text-sm rounded-full {activeCategory === 'all' ? 'bg-primary-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}"
          onclick={() => handleCategoryChange('all')}
        >
          All
        </button>
        <button
          class="px-3 py-1 text-sm rounded-full {activeCategory === 'system' ? 'bg-primary-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}"
          onclick={() => handleCategoryChange('system')}
        >
          System
        </button>
        <button
          class="px-3 py-1 text-sm rounded-full {activeCategory === 'sensor' ? 'bg-primary-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}"
          onclick={() => handleCategoryChange('sensor')}
        >
          Sensors
        </button>
        <button
          class="px-3 py-1 text-sm rounded-full {activeCategory === 'alert' ? 'bg-primary-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}"
          onclick={() => handleCategoryChange('alert')}
        >
          Alerts
        </button>
        <button
          class="px-3 py-1 text-sm rounded-full {activeCategory === 'user' ? 'bg-primary-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}"
          onclick={() => handleCategoryChange('user')}
        >
          User
        </button>
      </div>

      <div class="max-h-96 overflow-y-auto">
        {#if filteredNotifications().length === 0}
          <div class="flex flex-col items-center justify-center p-8 text-gray-500 dark:text-gray-400">
            <i class="fas fa-bell-slash text-4xl mb-2"></i>
            <p>No notifications</p>
          </div>
        {:else}
          {#each filteredNotifications() as notification (notification.id)}
            <div
              class="p-4 border-b border-gray-200 dark:border-gray-700 {notification.read ? 'bg-gray-50 dark:bg-gray-800/50' : 'bg-white dark:bg-gray-800'}"
              transition:fade
            >
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <i class="fas {notification.type === 'info' ? 'fa-info-circle text-info-500' :
                    notification.type === 'success' ? 'fa-check-circle text-success-500' :
                    notification.type === 'warning' ? 'fa-exclamation-triangle text-warning-500' :
                    'fa-times-circle text-error-500'}"></i>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">{notification.title}</h4>
                    <span class="text-xs text-gray-500 dark:text-gray-400">
                      {formatTimestamp(notification.timestamp)}
                    </span>
                  </div>
                  <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{notification.message}</p>
                  {#if notification.actions}
                    <div class="mt-2 flex space-x-2">
                      {#each notification.actions as action}
                        <button
                          class="px-3 py-1 text-xs font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                          onclick={action.handler}
                        >
                          {action.label}
                        </button>
                      {/each}
                    </div>
                  {/if}
                </div>
                {#if !notification.read}
                  <button
                    class="flex-shrink-0 p-1 text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
                    onclick={() => notifications.markAsRead(notification.id)}
                    aria-label="Mark as read"
                  >
                    <i class="fas fa-check"></i>
                  </button>
                {/if}
              </div>
            </div>
          {/each}
        {/if}
      </div>
    </div>
  {/if}
</div> 