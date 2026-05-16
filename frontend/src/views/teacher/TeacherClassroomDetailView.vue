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

const showAddModal = ref(false)
const allStudents = ref([])
const selectedStudentId = ref('')
const adding = ref(false)


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

async function fetchStudents() {
  const token = authStore.session?.access_token
  allStudents.value = await apiFetch('/api/users/by-role/student', token)
}

async function addMember() {
  if (!selectedStudentId.value) return
  adding.value = true
  try {
    const token = authStore.session?.access_token
    await apiFetch(`/api/classrooms/${classroomId}/members`, token, {
      method: 'POST',
      body: JSON.stringify({ student_id: selectedStudentId.value }),
    })
    await fetchData()
    showAddModal.value = false
    selectedStudentId.value = ''
  } catch (err) {
    console.error('Error afegint alumne:', err)
  } finally {
    adding.value = false
  }
}

async function openAddModal() {
  await fetchStudents()
  showAddModal.value = true
}

async function removeMember(studentId) {
  if (!confirm('Treure aquest alumne de l\'aula?')) return
  try {
    const token = authStore.session?.access_token
    await apiFetch(`/api/classrooms/${classroomId}/members/${studentId}`, token, {
      method: 'DELETE',
    })
    members.value = members.value.filter(m => m.id !== studentId)
  } catch (err) {
    console.error('Error traient alumne:', err)
  }
}


onMounted(fetchData)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
    <div v-else>
      <div class="flex justify-end mb-4">
        <button class="border rounded px-3 py-1 hover:bg-gray-100" @click="openAddModal">
          Afegir alumne
        </button>
      </div>

      <p v-if="members.length === 0" class="text-gray-400 text-sm">No hi ha alumnes en aquesta aula.</p>
      <div v-else class="flex flex-col gap-4">
        <div v-for="member in members" :key="member.id" class="border rounded p-4">
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="font-medium">{{ member.full_name ?? '—' }}</p>
              <p class="text-sm text-gray-500">{{ member.email }}</p>
            </div>
            <button class="text-xs border rounded px-2 py-1 text-red-600 hover:bg-red-50"
              @click="removeMember(member.id)">
              Treure
            </button>
          </div>
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
              <span class="text-gray-400">{{ p.attempts }} intent{{ p.attempts !== 1 ? 's' : '' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal afegir alumne -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
        <h2 class="text-lg font-bold mb-4">Afegir alumne</h2>
        <select v-model="selectedStudentId" class="w-full border rounded px-3 py-2 text-sm">
          <option value="" disabled>Selecciona un alumne...</option>
          <option v-for="student in allStudents" :key="student.id" :value="student.id">
            {{ student.full_name ?? student.email }} — {{ student.email }}
          </option>
        </select>
        <div class="flex justify-end gap-2 mt-6">
          <button class="text-sm px-4 py-2 rounded border hover:bg-gray-100" @click="showAddModal = false">
            Cancel·lar
          </button>
          <button class="text-sm px-4 py-2 rounded bg-black text-white hover:bg-gray-800 disabled:opacity-50"
            :disabled="adding || !selectedStudentId" @click="addMember">
            {{ adding ? 'Afegint...' : 'Afegir' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>