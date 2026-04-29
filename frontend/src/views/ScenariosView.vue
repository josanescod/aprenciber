<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { getScenarios, getMyProgress } from '../services/api.js'
import { authStore } from '../stores/auth.js'

const router = useRouter()

const scenarios = ref([])
const progressByScenarioId = ref({})
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

const isCompleted = (scenarioId) => {
  return progressByScenarioId.value[scenarioId]?.success === true
}

onMounted(async () => {
  try {
    const [scenariosData, progressData] = await Promise.all([
      getScenarios(authStore.session?.access_token),
      getMyProgress(authStore.session?.access_token),
    ])

    scenarios.value = scenariosData

    progressByScenarioId.value = Object.fromEntries(
      progressData.map((item) => [item.scenario_id, item])
    )
  } catch (err) {
    error.value = 'Error carregant els escenaris.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AppLayout>
    <div>
      <h1 class="text-2xl font-bold mb-6">Escenaris</h1>

      <div v-if="loading" class="text-gray-500">Carregant...</div>

      <div v-else-if="error" class="text-red-500">{{ error }}</div>

      <div v-else-if="scenarios.length === 0" class="text-gray-500">
        No hi ha escenaris disponibles.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="scenario in scenarios"
          :key="scenario.id"
          class="border rounded-lg p-4 cursor-pointer hover:shadow-md transition-shadow bg-white"
          :class="{ 'bg-green-50': isCompleted(scenario.id) }"
          @click="router.push(`/scenarios/${scenario.id}`)"
        >
          <div class="flex items-start justify-between mb-2 gap-2">
            <h2 class="font-semibold text-gray-900">{{ scenario.title }}</h2>

            <div class="flex gap-2 shrink-0">
              <span
                v-if="isCompleted(scenario.id)"
                class="text-xs font-medium px-2 py-1 rounded bg-green-100 text-green-800"
              >
                Completat
              </span>

              <span
                class="text-xs font-medium px-2 py-1 rounded"
                :class="difficultyColor(scenario.difficulty)"
              >
                {{ scenario.difficulty }}
              </span>
            </div>
          </div>

          <p class="text-sm text-gray-600 line-clamp-3">
            {{ scenario.description }}
          </p>

          <div v-if="scenario.tags" class="mt-3 flex flex-wrap gap-1">
            <span
              v-for="tag in scenario.tags.split(',')"
              :key="tag"
              class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>