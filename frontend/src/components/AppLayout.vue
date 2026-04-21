<template>
  <div class="min-h-screen flex flex-col">

    <header class="border-b px-6 py-3 flex items-center justify-between">
      <span class="font-bold text-lg">AprenCiber</span>

      <nav class="flex items-center gap-6 text-sm">
        <RouterLink
          to="/dashboard"
          class="hover:underline"
          active-class="font-semibold"
        >
          Dashboard
        </RouterLink>
        <RouterLink
          to="/scenarios"
          class="hover:underline"
          active-class="font-semibold"
        >
          Escenaris
        </RouterLink>
        <RouterLink
          to="/progress"
          class="hover:underline"
          active-class="font-semibold"
        >
          Progrés
        </RouterLink>
      </nav>

      <div class="flex items-center gap-4 text-sm">
        <span class="text-gray-500">{{ authStore.profile?.email }}</span>
        <button
          class="border rounded px-3 py-1 hover:bg-gray-100"
          @click="handleLogout"
        >
          Sortir
        </button>
      </div>
    </header>

    <main class="flex-1 p-6">
      <slot />
    </main>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'

const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>