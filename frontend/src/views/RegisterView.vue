<script setup>
import { ref } from 'vue'
import { register } from '../services/auth.service'

const fullName = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

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
    <main class="max-w-md mx-auto p-6">
        <h1 class="text-2xl font-bold mb-4">Crear compte</h1>

        <form class="space-y-4" @submit.prevent="handleRegister">
            <div>
                <label class="block mb-1">Nom</label>
                <input v-model="fullName" type="text" class="w-full border rounded px-3 py-2" required />
            </div>
            <div>
                <label class="block mb-1">Email</label>
                <input v-model="email" type="email" class="w-full border rounded px-3 py-2" required />
            </div>
            <div>
                <label class="block mb-1">Contrassenya</label>
                <input v-model="password" type="password" class="w-full border rounded px-3 py-2" minlength="8"
                    required />
            </div>

            <button type="submit" class="bg-black text-white px-4 py-2 rounded" :disabled="loading">
                {{ loading ? 'Creant compte...' : 'Registrar-se' }}
            </button>
        </form>

        <div v-if="success" class="mt-4 p-4 bg-green-50 border border-green-200 rounded">
            <p class="text-green-800 font-medium">Important!</p>
            <p class="text-green-700 text-sm mt-1">
                Revisa el teu email <strong>{{ email }}</strong> i fes click a l'enllaç per confirmar el registre.
            </p>
        </div>

        <p v-if="error" class="text-red-600 mt-4">{{ error }}</p>

        <p class="mt-4 text-sm text-center">
            Ja estàs registrat? <RouterLink to="/login" class="text-blue-600 hover:underline">Inicia sessió</RouterLink>
        </p>
    </main>
</template>
