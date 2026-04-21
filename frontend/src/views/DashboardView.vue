<script setup>
import AppLayout from '../components/AppLayout.vue'
import { authStore } from '../stores/auth'
</script>

<template>
  <AppLayout>
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

    <div class="border rounded p-4 max-w-md">
      <h2 class="font-semibold mb-2">El teu perfil</h2>
      <p><span class="text-gray-500">Email:</span> {{ authStore.profile?.email }}</p>
      <p><span class="text-gray-500">Rol:</span> {{ authStore.profile?.role }}</p>
      <p><span class="text-gray-500">Nom:</span> {{ authStore.profile?.full_name ?? '—' }}</p>
    </div>
  </AppLayout>
</template>