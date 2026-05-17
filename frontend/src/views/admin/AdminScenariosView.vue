<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const scenarios = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchScenarios() {
  try {
    const token = authStore.session?.access_token
    scenarios.value = await apiFetch('/api/scenarios/admin/all', token)
  } catch (err) {
    error.value = 'Error carregant els escenaris'
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function toggleActive(scenario) {
  try {
    const token = authStore.session?.access_token
    const updated = await apiFetch(`/api/scenarios/admin/${scenario.id}/toggle`, token, {
      method: 'PATCH',
    })
    const index = scenarios.value.findIndex(s => s.id === scenario.id)
    if (index !== -1) scenarios.value.splice(index, 1, updated)
  } catch (err) {
    console.error('Error canviant estat:', err)
  }
}

onMounted(fetchScenarios)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
    <div v-else class="overflow-x-auto rounded border border-black">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-black text-gray-500 text-left">
          <tr>
            <th class="px-4 py-3 font-medium">Títol</th>
            <th class="px-4 py-3 font-medium">Dificultat</th>
            <th class="px-4 py-3 font-medium">Tags</th>
            <th class="px-4 py-3 font-medium">Estat</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-black">
          <tr v-for="scenario in scenarios" :key="scenario.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium">{{ scenario.title }}</td>
            <td class="px-4 py-3">
              <span class="text-xs px-2 py-0.5 rounded font-medium"
                :class="{
                  'bg-green-100 text-green-700': scenario.difficulty === 'easy',
                  'bg-yellow-100 text-yellow-700': scenario.difficulty === 'medium',
                  'bg-red-100 text-red-700': scenario.difficulty === 'hard',
                }">
                {{ scenario.difficulty }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-500">{{ scenario.tags }}</td>
            <td class="px-4 py-3">
              <button
                class="text-xs px-2 py-1 rounded font-medium"
                :class="scenario.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                @click="toggleActive(scenario)"
              >
                {{ scenario.is_active ? 'Actiu' : 'Inactiu' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>