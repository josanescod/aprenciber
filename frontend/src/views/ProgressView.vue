<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { getMyProgress } from '../services/api.js'
import { authStore } from '../stores/auth.js'

const progress = ref([])
const loading = ref(true)
const error = ref(null)

const difficultyColor = (difficulty) => {
  switch (difficulty) {
    case 'easy': return 'bg-green-100 text-green-800'
    case 'medium': return 'bg-yellow-100 text-yellow-800'
    case 'hard': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

function formatTime(seconds) {
  if (seconds === null || seconds === undefined) return '-'

  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60

  if (minutes === 0) {
    return `${remainingSeconds}s`
  }

  return `${minutes}m ${remainingSeconds}s`
}

onMounted(async () => {
  try {
    progress.value = await getMyProgress(authStore.session?.access_token)
  } catch (err) {
    console.error(err)
    error.value = 'Error carregant el progrés.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AppLayout>
    <div>
      <h1 class="text-2xl font-bold mb-6">El meu progrés</h1>

      <div v-if="loading" class="text-gray-500">
        Carregant progrés...
      </div>

      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>

      <div v-else-if="progress.length === 0" class="text-gray-500">
        Encara no hi ha progrés registrat.
      </div>

      <div v-else class="overflow-x-auto bg-white border rounded-lg">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-50 text-gray-600">
            <tr>
              <th class="text-left px-4 py-3">Escenari</th>
              <th class="text-left px-4 py-3">Dificultat</th>
              <th class="text-left px-4 py-3">Estat</th>
              <th class="text-left px-4 py-3">Temps</th>
              <th class="text-left px-4 py-3">Intents</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in progress" :key="item.scenario_id" class="border-t">
              <td class="px-4 py-3 font-medium text-gray-900">
                {{ item.scenario_title }}
              </td>

              <td class="px-4 py-3">
                <span class="text-xs font-medium px-2 py-1 rounded" :class="difficultyColor(item.difficulty)">
                  {{ item.difficulty }}
                </span>
              </td>

              <td class="px-4 py-3">
                <span v-if="item.success" class="text-green-700 bg-green-100 px-2 py-1 rounded text-xs font-medium">
                  Completat
                </span>
                <span v-else class="text-gray-700 bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                  Pendent
                </span>
              </td>

              <td class="px-4 py-3">
                {{ item.success ? formatTime(item.best_time_seconds) : '-' }}
              </td>

              <td class="px-4 py-3 text-gray-600">{{ item.attempts }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </AppLayout>
</template>