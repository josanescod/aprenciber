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

    const response = await fetch('http://127.0.0.1:8000/api/scenarios/admin/upload', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    })

    if (!response.ok) {
      const data = await response.json()
      uploadError.value = data.detail || 'Error pujant l\'escenari'
      return
    }

    await fetchScenarios()
    showUploadModal.value = false
  } catch (err) {
    uploadError.value = 'Error de connexió'
    console.error(err)
  } finally {
    uploading.value = false
  }
}


onMounted(fetchScenarios)
</script>

<template>
  <div class="font-sans">
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>

    <p
      v-else-if="error"
      class="font-mono text-sm text-red-600 bg-red-50 border border-red-100 px-4 py-3 rounded whitespace-pre-wrap"
    >
      {{ error }}
    </p>

    <div v-else class="overflow-x-auto rounded-xl border border-gray-200 bg-white">
      <div class="flex justify-end p-4">
        <button
          class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 transition"
          @click="showUploadModal = true"
        >
          Importar escenari
        </button>
      </div>

      <table class="w-full min-w-max text-sm">
        <thead class="bg-gray-50 border-b border-gray-200 text-gray-500 text-left">
          <tr>
            <th class="px-4 py-3 font-medium">Títol</th>
            <th class="px-4 py-3 font-medium">Dificultat</th>
            <th class="px-4 py-3 font-medium">Tags</th>
            <th class="px-4 py-3 font-medium">Estat</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-200">
          <tr
            v-for="scenario in scenarios"
            :key="scenario.id"
            class="hover:bg-gray-50 transition-colors duration-200"
          >
            <td class="px-4 py-3">
              <div class="font-medium text-gray-900">
                {{ scenario.title }}
              </div>

              <div
                v-if="scenario.slug"
                class="font-mono text-xs text-gray-400 mt-1 break-all"
              >
                {{ scenario.slug }}
              </div>
            </td>

            <td class="px-4 py-3">
              <span
                class="font-mono text-xs px-2 py-0.5 rounded-full font-semibold uppercase tracking-wide"
                :class="{
                  'bg-green-100 text-green-700': scenario.difficulty === 'easy',
                  'bg-yellow-100 text-yellow-700': scenario.difficulty === 'medium',
                  'bg-red-100 text-red-700': scenario.difficulty === 'hard',
                }"
              >
                {{ scenario.difficulty }}
              </span>
            </td>

            <td class="px-4 py-3">
              <div
                v-if="scenario.tags"
                class="flex flex-wrap gap-1.5"
              >
                <span
                  v-for="tag in scenario.tags.split(',')"
                  :key="tag"
                  class="font-mono text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded"
                >
                  {{ tag.trim() }}
                </span>
              </div>

              <span v-else class="text-gray-400">—</span>
            </td>

            <td class="px-4 py-3">
              <button
                class="text-xs px-3 py-1 rounded-full font-medium transition"
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

    <!-- Modal upload -->
    <div
      v-if="showUploadModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4 font-sans"
    >
      <div class="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">
          Importar escenari
        </h2>

        <p class="text-sm text-gray-500 mb-4 leading-relaxed">
          Puja un fitxer .zip amb l'estructura:<br>
          <code class="font-mono text-xs bg-gray-100 text-gray-700 px-1.5 py-0.5 rounded break-all">
            nom_escenari/scenario.yaml + attacker/ + target/
          </code>
        </p>

        <input
          type="file"
          accept=".zip"
          class="text-sm w-full text-gray-700 file:mr-3 file:border file:border-gray-300 file:rounded-lg file:bg-white file:px-3 file:py-1.5 file:text-sm file:text-gray-700 hover:file:bg-gray-100"
          @change="uploadScenario"
        />

        <p
          v-if="uploadError"
          class="font-mono text-xs text-red-600 bg-red-50 border border-red-100 px-3 py-2 rounded mt-3 whitespace-pre-wrap"
        >
          {{ uploadError }}
        </p>

        <div class="flex justify-end gap-2 mt-6">
          <button
            class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
            @click="showUploadModal = false"
          >
            Cancel·lar
          </button>

          <span
            v-if="uploading"
            class="font-mono text-xs text-gray-500 self-center"
          >
            Pujant...
          </span>
        </div>
      </div>
    </div>
  </div>
</template>