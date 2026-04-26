<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { getScenario, startLab as startLabApi, getActiveLabs } from '../services/api.js'
import { authStore } from '../stores/auth.js'


const route = useRoute()
const router = useRouter()

const scenario = ref(null)
const loading = ref(true)
const startingLab = ref(false)
const startLabError = ref(null)
const activeLab = ref(null)

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
        const labs = await getActiveLabs(authStore.session.access_token)

        // buscar si l'usuari té un lab actiu per aquest escenari
        activeLab.value = labs.find(
            (lab) => lab.scenario_id === scenario.value.id
        ) || null
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

async function startLab() {
    startLabError.value = null
    startingLab.value = true

    try {
        const data = await startLabApi(
            scenario.value.slug,
            authStore.session.access_token
        )

        router.push(`/labs/${data.id}`)
    } catch (error) {
        console.error(error)

        if (error.status === 409 && error.detail?.lab_id) {
            router.push(`/labs/${error.detail.lab_id}`)
        } else if (error.status === 409) {
            startLabError.value = 'Ja tens un laboratori actiu.'
        } else {
            startLabError.value = 'Error iniciant el laboratori.'
        }
    } finally {
        startingLab.value = false
    }
}
</script>

<template>
    <AppLayout>
        <div>

            <button class="text-sm text-gray-500 hover:text-gray-700 mb-6 flex items-center gap-1"
                @click="router.push('/scenarios')">
                ← Tornar als escenaris
            </button>

            <div v-if="loading" class="text-gray-500">
                Carregant...
            </div>

            <div v-else-if="scenario">
                <div class="flex items-start justify-between mb-4">
                    <h1 class="text-2xl font-bold text-gray-900">
                        {{ scenario.title }}
                    </h1>

                    <span class="text-sm font-medium px-3 py-1 rounded-full ml-4 shrink-0"
                        :class="difficultyColor(scenario.difficulty)">
                        {{ scenario.difficulty }}
                    </span>
                </div>

                <p class="text-gray-600 mb-6">
                    {{ scenario.description }}
                </p>

                <div v-if="scenario.tags" class="flex flex-wrap gap-2 mb-8">
                    <span v-for="tag in scenario.tags.split(',')" :key="tag"
                        class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {{ tag }}
                    </span>
                </div>
  
                <div class="flex items-center gap-3">
                    <button
                        class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium px-6 py-3 rounded-lg transition-colors"
                        :disabled="startingLab || !!activeLab" @click="startLab">
                        {{ startingLab ? 'Creant laboratori...' : 'Iniciar laboratori' }}
                    </button>

                    <button v-if="activeLab"
                        class="bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-3 rounded-lg"
                        @click="router.push(`/labs/${activeLab.id}`)">
                        Continuar laboratori
                    </button>
                </div>

                <p v-if="activeLab" class="text-sm text-gray-500 mt-3">
                    Ja tens un laboratori actiu. Pots continuar-lo o eliminar-lo des de la vista del laboratori.
                </p>

                <p v-if="startLabError" class="text-red-500 text-sm mt-3">
                    {{ startLabError }}
                </p>
            </div>

        </div>
    </AppLayout>
</template>