<script setup>
import { ref, computed } from 'vue'
import { register } from '../services/auth.service'

const fullName = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

const passwordsMatch = computed(() =>
  !password.value || !passwordConfirm.value || password.value === passwordConfirm.value
)

const formValid = computed(() =>
  fullName.value &&
  email.value &&
  password.value.length >= 8 &&
  password.value === passwordConfirm.value
)

async function handleRegister() {
  loading.value = true
  error.value = ''
  success.value = false
  try {
    await register(email.value, password.value, fullName.value)
    success.value = true
  } catch (err) {
    error.value = err.message || 'Error al crear el compte'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="min-h-screen flex items-center justify-center bg-gray-50 px-4 font-sans">
    <div class="w-full max-w-md border border-gray-200 rounded-xl bg-white p-8">
      <h1 class="text-2xl font-semibold mb-6 text-center text-gray-900">
        Crear compte
      </h1>

      <form class="space-y-4" @submit.prevent="handleRegister">
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700">Nom</label>
          <input v-model="fullName" type="text"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
            required />
        </div>

        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
          <input v-model="email" type="email"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
            required />
        </div>

        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700">Contrasenya</label>
          <input v-model="password" type="password" minlength="8"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
            required />
          <p v-if="password && password.length < 8" class="text-red-500 text-xs mt-1">
            Mínim 8 caràcters
          </p>
        </div>

        <div>
          <label class="block mb-1 text-sm font-medium text-gray-700">Confirmar contrasenya</label>
          <input v-model="passwordConfirm" type="password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
            required />
          <p v-if="!passwordsMatch" class="text-red-500 text-xs mt-1">
            Les contrasenyes no coincideixen
          </p>
        </div>

        <button type="submit"
          class="w-full bg-black text-white py-2.5 rounded-lg hover:bg-gray-800 transition disabled:opacity-50"
          :disabled="loading || !formValid">
          {{ loading ? 'Creant compte...' : 'Registrar-se' }}
        </button>
      </form>

      <div v-if="success" class="mt-5 p-4 border border-green-200 rounded-lg bg-green-50">
        <p class="text-green-800 font-medium text-sm">Important!</p>
        <p class="text-green-700 text-sm mt-1">
          Revisa el teu email <strong>{{ email }}</strong> i fes click a
          l'enllaç per confirmar el registre.
        </p>
      </div>

      <p v-if="error" class="text-red-600 mt-4 text-sm text-center">{{ error }}</p>

      <p class="mt-6 text-sm text-center text-gray-600">
        Ja estàs registrat?
        <RouterLink to="/login" class="text-gray-900 hover:underline">
          Inicia sessió
        </RouterLink>
      </p>
    </div>
  </main>
</template>