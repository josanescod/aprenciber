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
async function updateRole(userId, newRole) {
    try {
        const token = authStore.session?.access_token
        const updated = await apiFetch(`/api/users/${userId}/role`, token, {
            method: 'PATCH',
            body: JSON.stringify({ role: newRole }),
        })
        console.log('updated:', updated)
        const index = users.value.findIndex(u => u.id === userId)
        if (index !== -1) users.value.splice(index, 1, updated)
    } catch (err) {
        console.error('Error actualitzant rol:', err)
    }
}

async function toggleActive(userId, currentValue) {
    try {
        const token = authStore.session?.access_token
        const updated = await apiFetch(`/api/users/${userId}/active`, token, {
            method: 'PATCH',
            body: JSON.stringify({ is_active: !currentValue }),
        })
        const index = users.value.findIndex(u => u.id === userId)
        if (index !== -1) users.value.splice(index, 1, updated)
    } catch (err) {
        console.error('Error canviant estat:', err)
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
                        <td class="px-4 py-3">
                            <select v-if="user.role !== 'admin'" :value="user.role"
                                class="text-sm border rounded px-2 py-1"
                                @change="updateRole(user.id, $event.target.value)">
                                <option value="student">Student</option>
                                <option value="teacher">Teacher</option>
                            </select>
                            <span v-else class="text-sm font-medium">Admin</span>
                        </td>
                        <td class="px-4 py-3">
                            <button v-if="user.role !== 'admin'" class="text-xs px-2 py-1 rounded font-medium"
                                :class="user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                                @click="toggleActive(user.id, user.is_active)">
                                {{ user.is_active ? 'Actiu' : 'Inactiu' }}
                            </button>
                            <span v-else class="text-xs px-2 py-1">—</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>