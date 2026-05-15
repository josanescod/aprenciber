<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const route = useRoute()
const classroomId = route.params.id

const members = ref([])
const progress = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchData() {
  try {
    const token = authStore.session?.access_token
      ;[members.value, progress.value] = await Promise.all([
        apiFetch(`/api/classrooms/${classroomId}/members`, token),
        apiFetch(`/api/classrooms/${classroomId}/progress`, token),
      ])
  } catch (err) {
    error.value = 'Error carregant les dades'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function getProgress(studentId) {
  return progress.value.filter(p => p.student_id === studentId)
}

onMounted(fetchData)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
    <div v-else>
      <p v-if="members.length === 0" class="text-gray-400 text-sm">No hi ha alumnes en aquesta aula.</p>
      <div v-else class="flex flex-col gap-4">
        <div v-for="member in members" :key="member.id" class="border rounded p-4">
          <p class="font-medium">{{ member.full_name ?? '—' }}</p>
          <p class="text-sm text-gray-500 mb-3">{{ member.email }}</p>
          <div v-if="getProgress(member.id).length === 0" class="text-xs text-gray-400">
            Sense activitat encara
          </div>
          <div v-else class="flex flex-col gap-1">
            <div v-for="p in getProgress(member.id)" :key="p.scenario_id" class="flex items-center gap-2 text-xs">
              <span>Escenari {{ p.scenario_id }}</span>
              <span class="px-2 py-0.5 rounded font-medium"
                :class="p.success ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">
                {{ p.success ? 'Completat' : 'En progrés' }}
              </span>
              <span class="text-gray-400"> {{ p.attempts }} intent{{ p.attempts !== 1 ? 's' : '' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>