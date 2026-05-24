<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const users = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const newUser = ref({ email: '', full_name: '', password: '', role: 'student' })
const creating = ref(false)

const filterRole = ref('')
const filterActive = ref('')

const filteredUsers = computed(() => {
    return users.value.filter(u => {
        const roleMatch = filterRole.value === '' || u.role === filterRole.value
        const activeMatch = filterActive.value === '' ||
            (filterActive.value === 'active' && u.is_active) ||
            (filterActive.value === 'inactive' && !u.is_active)
        return roleMatch && activeMatch
    })
})

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

async function createUser() {
    if (!newUser.value.email || !newUser.value.password) return
    creating.value = true
    try {
        const token = authStore.session?.access_token
        const created = await apiFetch('/api/users/', token, {
            method: 'POST',
            body: JSON.stringify(newUser.value),
        })
        users.value.unshift(created)
        showModal.value = false
        newUser.value = { email: '', full_name: '', password: '', role: 'student' }
    } catch (err) {
        console.error('Error creant usuari:', err)
    } finally {
        creating.value = false
    }
}

onMounted(fetchUsers)
</script>

<template>
    <!-- Modal -->
    <div
        v-if="showModal"
        class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4"
    >
        <div class="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">
                Nou usuari
            </h2>

            <div class="flex flex-col gap-3">
                <input
                    v-model="newUser.full_name"
                    type="text"
                    placeholder="Nom complet"
                    class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
                />

                <input
                    v-model="newUser.email"
                    type="email"
                    placeholder="Email"
                    class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
                />

                <input
                    v-model="newUser.password"
                    type="password"
                    placeholder="Contrasenya"
                    class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
                />

                <p
                    v-if="newUser.password && newUser.password.length < 8"
                    class="text-red-600 text-xs -mt-2"
                >
                    Mínim 8 caràcters
                </p>

                <select
                    v-model="newUser.role"
                    class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
                >
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                    <option value="admin">Admin</option>
                </select>
            </div>

            <div class="flex justify-end gap-2 mt-6">
                <button
                    class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition disabled:opacity-50"
                    :disabled="creating || !newUser.email || !newUser.password || newUser.password.length < 8"
                    @click="createUser"
                >
                    {{ creating ? 'Creant...' : 'Crear' }}
                </button>

                <button
                    class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
                    @click="showModal = false"
                >
                    Cancel·lar
                </button>
            </div>
        </div>
    </div>

    <div>
        <p v-if="loading" class="text-gray-500 text-sm">
            Carregant...
        </p>

        <p v-else-if="error" class="text-red-600 text-sm">
            {{ error }}
        </p>

        <div
            v-else
            class="overflow-x-auto rounded-xl border border-gray-200 bg-white"
        >
            <div class="flex items-center justify-between p-4">
                <div class="flex gap-2">
                    <select
                        v-model="filterRole"
                        class="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
                    >
                        <option value="">Tots els rols</option>
                        <option value="student">Student</option>
                        <option value="teacher">Teacher</option>
                        <option value="admin">Admin</option>
                    </select>

                    <select
                        v-model="filterActive"
                        class="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-gray-500"
                    >
                        <option value="">Tots els estats</option>
                        <option value="active">Actiu</option>
                        <option value="inactive">Inactiu</option>
                    </select>
                </div>

                <button
                    class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 transition"
                    @click="showModal = true"
                >
                    Nou usuari
                </button>
            </div>

            <table class="w-full text-sm">
                <thead
                    class="bg-gray-50 border-b border-gray-200 text-gray-500 text-left"
                >
                    <tr>
                        <th class="px-4 py-3 font-medium">Nom</th>
                        <th class="px-4 py-3 font-medium">Email</th>
                        <th class="px-4 py-3 font-medium">Rol</th>
                        <th class="px-4 py-3 font-medium">Estat</th>
                    </tr>
                </thead>

                <tbody class="divide-y divide-gray-200">
                    <tr
                        v-for="user in filteredUsers"
                        :key="user.id"
                        class="hover:bg-gray-50 transition-colors duration-200"
                    >
                        <td class="px-4 py-3 text-gray-900">
                            {{ user.full_name ?? '—' }}
                        </td>

                        <td class="px-4 py-3 text-gray-600">
                            {{ user.email }}
                        </td>

                        <td class="px-4 py-3">
                            <select
                                v-if="user.role !== 'admin'"
                                :value="user.role"
                                class="text-sm border border-gray-300 rounded-lg px-3 py-1.5 focus:outline-none focus:border-gray-500"
                                @change="updateRole(user.id, $event.target.value)"
                            >
                                <option value="student">Student</option>
                                <option value="teacher">Teacher</option>
                            </select>

                            <span v-else class="text-sm font-medium text-gray-900">
                                Admin
                            </span>
                        </td>

                        <td class="px-4 py-3">
                            <button
                                v-if="user.role !== 'admin'"
                                class="text-xs px-3 py-1 rounded-full font-medium transition"
                                :class="user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                                @click="toggleActive(user.id, user.is_active)"
                            >
                                {{ user.is_active ? 'Actiu' : 'Inactiu' }}
                            </button>

                            <span v-else class="text-xs px-2 py-1 text-gray-400">
                                —
                            </span>
                        </td>
                    </tr>

                    <tr v-if="filteredUsers.length === 0">
                        <td colspan="4" class="px-4 py-6 text-center text-gray-400">
                            No hi ha usuaris amb aquests filtres
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>