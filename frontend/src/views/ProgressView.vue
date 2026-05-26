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
    <div class="font-sans">
      <h1 class="text-2xl font-bold mb-6">El meu progrés</h1>

      <div v-if="loading" class="text-gray-500">Carregant progrés...</div>

      <div v-else-if="error"
        class="font-mono text-sm text-red-600 bg-red-50 border border-red-100 px-4 py-3 rounded whitespace-pre-wrap">
        {{ error }}
      </div>

      <div v-else-if="progress.length === 0" class="text-gray-500">
        Encara no hi ha progrés registrat.
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl overflow-hidden">

        <!-- Taula — desktop -->
        <table class="hidden sm:table min-w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200 text-gray-500">
            <tr>
              <th class="text-left px-4 py-3 font-medium">Escenari</th>
              <th class="text-left px-4 py-3 font-medium">Dificultat</th>
              <th class="text-left px-4 py-3 font-medium">Estat</th>
              <th class="text-left px-4 py-3 font-medium">Temps</th>
              <th class="text-left px-4 py-3 font-medium">Intents</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="item in progress" :key="item.scenario_id"
              class="hover:bg-gray-50 transition-colors duration-200">
              <td class="px-4 py-3 font-medium text-gray-900">{{ item.scenario_title }}</td>
              <td class="px-4 py-3">
                <span class="font-mono text-xs font-semibold uppercase tracking-wide px-2 py-1 rounded"
                  :class="difficultyColor(item.difficulty)">
                  {{ item.difficulty }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span v-if="item.success"
                  class="text-green-700 bg-green-100 px-2 py-1 rounded text-xs font-medium">
                  Completat
                </span>
                <span v-else class="text-gray-700 bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                  Pendent
                </span>
              </td>
              <td class="px-4 py-3 font-mono text-xs text-gray-700">
                {{ item.success ? formatTime(item.best_time_seconds) : '—' }}
              </td>
              <td class="px-4 py-3 font-mono text-xs text-gray-600">{{ item.attempts }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Targetes — mòbil -->
        <div class="sm:hidden divide-y divide-gray-200">
          <div v-for="item in progress" :key="item.scenario_id" class="p-4 flex flex-col gap-2">
            <div class="flex items-start justify-between gap-2">
              <span class="font-medium text-gray-900">{{ item.scenario_title }}</span>
              <span v-if="item.success"
                class="text-green-700 bg-green-100 px-2 py-1 rounded text-xs font-medium shrink-0">
                Completat
              </span>
              <span v-else
                class="text-gray-700 bg-gray-100 px-2 py-1 rounded text-xs font-medium shrink-0">
                Pendent
              </span>
            </div>
            <div class="flex items-center gap-3 text-xs text-gray-500">
              <span class="font-mono font-semibold uppercase tracking-wide px-2 py-0.5 rounded"
                :class="difficultyColor(item.difficulty)">
                {{ item.difficulty }}
              </span>
              <span class="font-mono">{{ item.attempts }} intent{{ item.attempts !== 1 ? 's' : '' }}</span>
              <span v-if="item.success" class="font-mono text-gray-700">
                {{ formatTime(item.best_time_seconds) }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </AppLayout>
</template>