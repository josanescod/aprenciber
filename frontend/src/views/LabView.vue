<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { getLab, deleteLab, submitFlag } from '../services/api.js'
import { authStore } from '../stores/auth.js'

const route = useRoute()
const router = useRouter()

const lab = ref(null)
const loading = ref(true)
const error = ref(null)
const terminalReady = ref(false)
const terminalUrl = ref(null)
//flags
const flagInput = ref('')
const flagSubmitting = ref(false)
const flagResult = ref(null)

const labId = route.params.id

async function prepareTerminal(rawUrl) {
  terminalUrl.value = rawUrl
  terminalReady.value = true
}

onMounted(async () => {
  try {
    lab.value = await getLab(labId, authStore.session?.access_token)
    if (lab.value.status === 'running' && lab.value.terminal_url) {
      await prepareTerminal(lab.value.terminal_url)
    }
  } catch (err) {
    console.error(err)
    if (err.status === 404) {
      router.replace({ name: 'not-found' })
    } else if (err.status === 401) {
      authStore.error = 'La sessió ha expirat. Torna a entrar.'
      authStore.session = null
      authStore.user = null
      authStore.profile = null
      router.replace({ name: 'login' })
    } else {
      error.value = 'Error carregant el laboratori'
    }
  } finally {
    loading.value = false
  }
})

const statusColor = (status) => {
  switch (status) {
    case 'running': return 'text-green-600'
    case 'creating': return 'text-yellow-600'
    case 'failed': return 'text-red-600'
    case 'removed': return 'text-gray-500'
    case 'expired': return 'text-orange-500'
    default: return 'text-gray-700'
  }
}

const statusLabel = (status) => {
  switch (status) {
    case 'running': return 'Actiu'
    case 'creating': return 'Creant...'
    case 'failed': return 'Error'
    case 'removed': return 'Eliminat'
    case 'expired': return 'Expirat'
    default: return status
  }
}

async function removeLab() {
  try {
    // Netejar el iframe abans d'eliminar el lab
    terminalReady.value = false
    terminalUrl.value = null
    await deleteLab(labId, authStore.session?.access_token)
    router.push('/scenarios')
  } catch (err) {
    console.error(err)
    // Si falla, restaurar la terminal
    terminalReady.value = true
    terminalUrl.value = lab.value.terminal_url
    alert('Error eliminant el laboratori')
  }
}

async function sendFlag() {
  if (!flagInput.value.trim()) return

  flagSubmitting.value = true
  flagResult.value = null

  try {
    const result = await submitFlag(labId, flagInput.value.trim(), authStore.session?.access_token)
    flagResult.value = result
    if (result.correct) {
      flagInput.value = ''
    }
  } catch (err) {
    console.error(err)
    flagResult.value = {
      correct: false,
      message: 'Error enviant la flag. Torna-ho a intentar.',
    }
  } finally {
    flagSubmitting.value = false
  }
}

</script>

<template>
  <AppLayout>
    <div>
      <h1 class="text-2xl font-bold mb-6">Laboratori</h1>

      <div v-if="loading" class="text-gray-500">
        Carregant laboratori...
      </div>

      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>

      <div v-else-if="lab">
        <div class="flex items-center justify-between mb-4">
          <div>
            <p class="mb-1 text-sm text-gray-500">Lab #{{ lab.id }}</p>
            <p class="mb-1">
              <strong>Estat:</strong>
              <span :class="statusColor(lab.status)" class="ml-1 font-medium">
                {{ statusLabel(lab.status) }}
              </span>
            </p>
          </div>
          <button
            class="bg-red-600 hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-4 py-2 rounded transition-colors"
            :disabled="lab.status !== 'running'"
            @click="removeLab">
            Eliminar laboratori
          </button>
        </div>

        <p v-if="lab.status === 'expired'" class="text-orange-500 mb-4">
          Aquest laboratori ha expirat.
        </p>
        <p v-if="lab.status === 'removed'" class="text-gray-500 mb-4">
          Aquest laboratori ha estat eliminat.
        </p>

        <!-- Terminal -->
        <div v-if="lab.status === 'running'" class="mb-6">
          <h2 class="font-semibold mb-2">Terminal</h2>
          <div v-if="terminalReady" class="rounded overflow-hidden border border-gray-300" style="height: 500px;">
            <iframe
              :src="terminalUrl"
              class="w-full h-full"
              frameborder="0"
              allow="clipboard-read; clipboard-write"
            />
          </div>
          <div v-else class="text-sm text-gray-500">
            Preparant terminal...
          </div>
        </div>
        <!-- Enviar flag -->
        <div v-if="lab.status === 'running'" class="mb-6">
          <h2 class="font-semibold mb-2">Enviar flag</h2>

          <div v-if="flagResult?.correct" class="mb-3 p-3 bg-green-50 border border-green-200 rounded text-green-800 text-sm">
            {{ flagResult.message }}
          </div>

          <div v-if="flagResult && !flagResult.correct" class="mb-3 p-3 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
            {{ flagResult.message }}
          </div>

          <div v-if="!flagResult?.correct" class="flex gap-2">
            <input
              v-model="flagInput"
              type="text"
              placeholder="FLAG{...}"
              class="flex-1 border rounded px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="flagSubmitting"
              @keyup.enter="sendFlag"
            />
            <button
              class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-4 py-2 rounded text-sm transition-colors"
              :disabled="flagSubmitting || !flagInput.trim()"
              @click="sendFlag">
              {{ flagSubmitting ? 'Enviant...' : 'Enviar' }}
            </button>
          </div>
        </div>
      </div>

    </div>
  </AppLayout>
</template>