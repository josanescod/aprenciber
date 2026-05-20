<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const scenarios = ref([])
const loading = ref(true)
const error = ref(null)

const showUploadModal = ref(false)
const uploading = ref(false)
const uploadError = ref(null)

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

async function uploadScenario(event) {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  uploadError.value = null

  try {
    const token = authStore.session?.access_token
    const formData = new FormData()
    formData.append('file', file)

    await fetch('/api/scenarios/admin/upload', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    })

    await fetchScenarios()
    showUploadModal.value = false
  } catch (err) {
    uploadError.value = 'Error pujant l\'escenari'
    console.error(err)
  } finally {
    uploading.value = false
  }
}


onMounted(fetchScenarios)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
    <div v-else class="overflow-x-auto rounded border border-black">
      <div class="flex justify-end mb-4">
        <button class="border rounded px-3 py-1 hover:bg-gray-100" @click="showUploadModal = true">
          Importar escenari
        </button>
      </div>
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
              <span class="text-xs px-2 py-0.5 rounded font-medium" :class="{
                'bg-green-100 text-green-700': scenario.difficulty === 'easy',
                'bg-yellow-100 text-yellow-700': scenario.difficulty === 'medium',
                'bg-red-100 text-red-700': scenario.difficulty === 'hard',
              }">
                {{ scenario.difficulty }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-500">{{ scenario.tags }}</td>
            <td class="px-4 py-3">
              <button class="text-xs px-2 py-1 rounded font-medium"
                :class="scenario.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                @click="toggleActive(scenario)">
                {{ scenario.is_active ? 'Actiu' : 'Inactiu' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Modal upload -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
        <h2 class="text-lg font-bold mb-4">Importar escenari</h2>
        <p class="text-sm text-gray-500 mb-4">
          Puja un fitxer .zip amb l'estructura:<br>
          <code class="text-xs bg-gray-100 px-1">nom_escenari/scenario.yaml + attacker/ + target/</code>
        </p>
        <input type="file" accept=".zip" class="text-sm w-full" @change="uploadScenario" />
        <p v-if="uploadError" class="text-red-500 text-xs mt-2">{{ uploadError }}</p>
        <div class="flex justify-end gap-2 mt-6">
          <button class="text-sm px-4 py-2 rounded border hover:bg-gray-100" @click="showUploadModal = false">
            Cancel·lar
          </button>
          <span v-if="uploading" class="text-sm text-gray-500 self-center">Pujant...</span>
        </div>
      </div>
    </div>
  </div>
</template>