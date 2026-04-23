<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { getScenario } from '../services/api.js'
import { authStore } from '../stores/auth.js'

const route = useRoute()
const router = useRouter()

const scenario = ref(null)
const loading = ref(true)

const difficultyColor = (difficulty) => {
    switch (difficulty) {
        case 'easy': return 'bg-green-100 text-green-800'
        case 'medium': return 'bg-yellow-100 text-yellow-800'
        case 'hard': return 'bg-red-100 text-red-800'
        default: return 'bg-gray-100 text-gray-800'
    }
}

onMounted(async () => {
  try {
    scenario.value = await getScenario(route.params.id, authStore.session.access_token)
  } catch (error) {
    console.error(`[ScenarioDetail] error status: ${error.status} — ${error.message}`)
    if (error.status === 404) {
      router.replace({ name: 'not-found' })
    } else if (error.status === 401) {
      authStore.error = 'Your session has expired. Please log in again.'
      authStore.session = null
      authStore.user = null
      authStore.profile = null
      router.replace({ name: 'login' })
    } else {
      router.replace({ name: 'not-found' })
    }
  } finally {
    loading.value = false
  }
})

function startLab() {
    console.log('Iniciar laboratori per escenari:', scenario.value.id)
    alert('Funcionalitat disponible aviat')
}
</script>

<template>
    <AppLayout>
        <div>

            <button class="text-sm text-gray-500 hover:text-gray-700 mb-6 flex items-center gap-1"
                @click="router.push('/scenarios')">
                ← Tornar als escenaris
            </button>

            <div v-if="loading" class="text-gray-500">Carregant...</div>

            <div v-else-if="scenario">
                <div class="flex items-start justify-between mb-4">
                    <h1 class="text-2xl font-bold text-gray-900">{{ scenario.title }}</h1>
                    <span class="text-sm font-medium px-3 py-1 rounded-full ml-4 shrink-0"
                        :class="difficultyColor(scenario.difficulty)">
                        {{ scenario.difficulty }}
                    </span>
                </div>

                <p class="text-gray-600 mb-6">{{ scenario.description }}</p>

                <div v-if="scenario.tags" class="flex flex-wrap gap-2 mb-8">
                    <span v-for="tag in scenario.tags.split(',')" :key="tag"
                        class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {{ tag }}
                    </span>
                </div>

                <button
                    class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-lg transition-colors"
                    @click="startLab">
                    Iniciar laboratori
                </button>
            </div>

        </div>
    </AppLayout>
</template>