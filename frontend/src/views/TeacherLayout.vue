<script setup>
import AppLayout from '../components/AppLayout.vue'
import { authStore } from '../stores/auth'
</script>

<template>
  <AppLayout>
    <h1 class="text-2xl font-bold mb-4">Àrea del professor</h1>
    <p class="text-gray-600 mb-4">Benvingut, {{ authStore.profile?.full_name }}</p>
    <div class="border rounded p-4 max-w-md">
      <p class="text-sm">Rol: <span class="font-bold">{{ authStore.profile?.role }}</span></p>
    </div>

    <nav class="flex gap-2 border-b mb-6">
      <RouterLink :to="{ name: 'teacher-classrooms' }"
        class="px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors" :class="$route.name === 'teacher-classrooms'
          ? 'border-black text-black'
          : 'border-transparent text-gray-500 hover:text-black'">
        Les meves aules
      </RouterLink>
    </nav>

    <RouterView />

  </AppLayout>
</template>