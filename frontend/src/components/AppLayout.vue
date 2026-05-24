<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'

const router = useRouter()

const isStudent = computed(() => authStore.profile?.role === 'student')
const isAdmin = computed(() => authStore.profile?.role === 'admin')
const isTeacher = computed(() => authStore.profile?.role === 'teacher')

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="border-b border-gray-200 bg-white px-6 py-3 flex items-center justify-between">
      <span class="font-bold text-lg text-gray-900">AprenCiber</span>
      <nav class="flex items-center gap-6 text-sm">
        <RouterLink
          to="/dashboard"
          class="text-gray-700 hover:text-gray-900 hover:underline"
          active-class="font-semibold text-gray-900"
        >
          Dashboard
        </RouterLink>
        <RouterLink
          to="/scenarios"
          class="text-gray-700 hover:text-gray-900 hover:underline"
          active-class="font-semibold text-gray-900"
        >
          Escenaris
        </RouterLink>
        <RouterLink
          v-if="isStudent"
          to="/progress"
          class="text-gray-700 hover:text-gray-900 hover:underline"
          active-class="font-semibold text-gray-900"
        >
          Progrés
        </RouterLink>
        <RouterLink
          v-if="isAdmin"
          to="/admin"
          class="text-gray-700 hover:text-gray-900 hover:underline"
          active-class="font-semibold text-gray-900"
        >
          Admin
        </RouterLink>
        <RouterLink
          v-if="isTeacher"
          to="/teacher"
          class="text-gray-700 hover:text-gray-900 hover:underline"
          active-class="font-semibold text-gray-900"
        >
          Professor
        </RouterLink>
      </nav>
      <div class="flex items-center gap-4 text-sm">
        <span class="text-gray-500">
          {{ authStore.profile?.full_name || authStore.profile?.email }}
        </span>
        <button
          class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-50 transition"
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