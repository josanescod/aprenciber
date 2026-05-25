<script setup>
import AppLayout from '../components/AppLayout.vue'
import { authStore } from '../stores/auth'
</script>

<template>
  <AppLayout>
    <div class="font-sans">
      <div class="mb-6">
        <h1 class="text-2xl font-bold">Panell d'administració</h1>

        <p class="text-gray-600 mt-1">
          Benvingut,
          <span class="font-medium text-gray-800">
            {{ authStore.profile?.full_name }}
          </span>
        </p>
      </div>

      <nav class="flex gap-2 border-b mb-6 overflow-x-auto">
        <RouterLink
          :to="{ name: 'admin-users' }"
          class="px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap"
          :class="$route.name === 'admin-users'
            ? 'border-black text-black'
            : 'border-transparent text-gray-500 hover:text-black'"
        >
          Usuaris
        </RouterLink>

        <RouterLink
          :to="{ name: 'admin-scenarios' }"
          class="px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap"
          :class="$route.name === 'admin-scenarios'
            ? 'border-black text-black'
            : 'border-transparent text-gray-500 hover:text-black'"
        >
          Escenaris
        </RouterLink>
      </nav>

      <RouterView />
    </div>
  </AppLayout>
</template>