<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const router = useRouter()

async function handleLogin() {
  await authStore.login(email.value, password.value)
  if (authStore.profile) {
    router.push({ name: 'dashboard' })
  }
}
</script>


<template>
  <main class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-md border border-gray-200 rounded-xl bg-white p-8">
      <h1 class="text-2xl font-semibold mb-6 text-center text-gray-900">Login</h1>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
          <input
            v-model="email"
            type="email"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
            required
          />
        </div>

        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700">Password</label>
          <input
            v-model="password"
            type="password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-black text-white py-2.5 rounded-lg hover:bg-gray-800 transition"
          :disabled="authStore.loading"
        >
          {{ authStore.loading ? 'Loading...' : 'Sign in' }}
        </button>
      </form>

      <p v-if="authStore.error" class="text-red-600 mt-4 text-sm text-center">
        {{ authStore.error }}
      </p>

      <p class="mt-6 text-sm text-center text-gray-600">
        No estàs registrat?
        <RouterLink to="/register" class="text-gray-900 hover:underline">
          Registrarse
        </RouterLink>
      </p>
    </div>
  </main>
</template>
