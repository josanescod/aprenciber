<script setup>
import AppLayout from '../components/AppLayout.vue'
import { authStore } from '../stores/auth'
</script>

<template>
  <AppLayout>
    <div class="font-sans">
      <div class="mb-6">
        <h1 class="text-2xl font-bold mb-1">Àrea del professor</h1>

        <p class="text-gray-600">
          Benvingut,
          <span class="font-medium text-gray-800">
            {{ authStore.profile?.full_name }}
          </span>
        </p>
      </div>

      <div class="border rounded p-4 max-w-md mb-6 bg-white">
        <p class="text-sm text-gray-700">
          Rol:
          <span class="font-mono text-xs font-semibold uppercase tracking-wide text-gray-900">
            {{ authStore.profile?.role }}
          </span>
        </p>
      </div>

      <nav class="flex gap-2 border-b mb-6 overflow-x-auto">
        <RouterLink
          :to="{ name: 'teacher-classrooms' }"
          class="px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap"
          :class="$route.name === 'teacher-classrooms'
            ? 'border-black text-black'
            : 'border-transparent text-gray-500 hover:text-black'"
        >
          Les meves aules
        </RouterLink>
      </nav>

      <RouterView />
    </div>
  </AppLayout>
</template>