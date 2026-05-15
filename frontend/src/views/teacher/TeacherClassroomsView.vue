<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const classrooms = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchClassrooms() {
  try {
    const token = authStore.session?.access_token
    classrooms.value = await apiFetch('/api/classrooms/', token)
  } catch (err) {
    error.value = 'Error carregant les aules'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchClassrooms)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
    <div v-else>
      <p v-if="classrooms.length === 0" class="text-gray-400 text-sm">No tens cap aula creada.</p>
      <div v-else class="flex flex-col gap-3">
        <RouterLink
          v-for="classroom in classrooms"
          :key="classroom.id"
          :to="{ name: 'teacher-classroom-detail', params: { id: classroom.id } }"
          class="border rounded p-4 hover:bg-gray-50 transition-colors"
        >
          <p class="font-medium">{{ classroom.name }}</p>
          <p class="text-sm text-gray-500 mt-1">{{ classroom.description ?? '—' }}</p>
        </RouterLink>
      </div>
    </div>
  </div>
</template>