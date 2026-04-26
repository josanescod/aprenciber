<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { getLab, deleteLab } from '../services/api.js'
import { authStore } from '../stores/auth.js'

const route = useRoute()
const router = useRouter()

const lab = ref(null)
const loading = ref(true)
const error = ref(null)

const labId = route.params.id

onMounted(async () => {
  try {
    lab.value = await getLab(
      labId,
      authStore.session.access_token
    )
  } catch (err) {
    console.error(err)
    error.value = 'Error carregant el laboratori'
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

async function removeLab() {
  try {
    await deleteLab(labId, authStore.session.access_token)
    router.push('/scenarios')
  } catch (err) {
    console.error(err)
    alert('Error eliminant el laboratori')
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
        <p class="mb-2"><strong>ID:</strong> {{ lab.id }}</p>
        <p class="mb-2">
          <strong>Status:</strong>
          <span :class="statusColor(lab.status)">
            {{ lab.status }}
          </span>
        </p>
        <p v-if="lab.status === 'expired'" class="text-orange-500 mb-2">
          Aquest laboratori ha expirat.
        </p>
        <button class="mt-4 bg-red-600 hover:bg-red-700 disabled:bg-gray-300 text-white px-4 py-2 rounded"
          :disabled="lab.status !== 'running'" @click="removeLab">
          Eliminar laboratori
        </button>
        <div class="mt-4">
          <h2 class="font-semibold mb-2">Contenidors:</h2>
          <ul class="text-sm text-gray-700">
            <li v-for="(container, key) in lab.containers_info" :key="key">
              {{ key }} → {{ container.name }}
            </li>
          </ul>
        </div>
      </div>

    </div>
  </AppLayout>
</template>