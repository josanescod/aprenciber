<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const users = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchUsers() {
    try {
        const token = authStore.session?.access_token
        users.value = await apiFetch('/api/users/', token)
    } catch (err) {
        error.value = 'Error carregant els usuaris'
        console.error(err)
    } finally {
        loading.value = false
    }
}

onMounted(fetchUsers)
</script>

<template>
    <div>
        <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
        <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
        <div v-else class="overflow-x-auto rounded border border-black">
            <table class="w-full text-sm">
                <thead class="bg-gray-50 border-b border-black text-gray-500 text-left">
                    <tr>
                        <th class="px-4 py-3 font-medium">Nom</th>
                        <th class="px-4 py-3 font-medium">Email</th>
                        <th class="px-4 py-3 font-medium">Rol</th>
                        <th class="px-4 py-3 font-medium">Estat</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-black">
                    <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                        <td class="px-4 py-3">{{ user.full_name ?? '—' }}</td>
                        <td class="px-4 py-3 text-gray-600">{{ user.email }}</td>
                        <td class="px-4 py-3">{{ user.role }}</td>
                        <td class="px-4 py-3">{{ user.is_active ? 'Actiu' : 'Inactiu' }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>