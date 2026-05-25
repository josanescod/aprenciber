<script setup>
import AppLayout from '../components/AppLayout.vue'
import { authStore } from '../stores/auth'
</script>

<template>
  <AppLayout>
    <div class="font-sans">
      <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

      <div class="border rounded p-4 max-w-md bg-white">
        <h2 class="font-semibold mb-3 text-gray-900">El teu perfil</h2>

        <div class="space-y-2 text-sm">
          <p>
            <span class="text-gray-500">Email:</span>
            <span class="font-mono text-xs text-gray-700 break-all">
              {{ authStore.profile?.email }}
            </span>
          </p>

          <p>
            <span class="text-gray-500">Rol:</span>
            <span class="font-mono text-xs font-semibold uppercase tracking-wide text-gray-900">
              {{ authStore.profile?.role }}
            </span>
          </p>

          <p>
            <span class="text-gray-500">Nom:</span>
            <span class="text-gray-900">
              {{ authStore.profile?.full_name ?? '—' }}
            </span>
          </p>
        </div>
      </div>
    </div>
  </AppLayout>
</template>