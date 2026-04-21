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
  <main class="max-w-md mx-auto p-6">
    <h1 class="text-2xl font-bold mb-4">Login</h1>

    <form class="space-y-4" @submit.prevent="handleLogin">
      <div>
        <label class="block mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>

      <div>
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>

      <button
        type="submit"
        class="bg-black text-white px-4 py-2 rounded"
        :disabled="authStore.loading"
      >
        {{ authStore.loading ? 'Loading...' : 'Sign in' }}
      </button>
    </form>

    <p v-if="authStore.error" class="text-red-600 mt-4">
      {{ authStore.error }}
    </p>

    <section v-if="authStore.profile" class="mt-6 border rounded p-4">
      <h2 class="font-semibold mb-2">Perfil carregat des del backend</h2>
      <pre class="text-sm">{{ authStore.profile }}</pre>
    </section>
  </main>
</template>

