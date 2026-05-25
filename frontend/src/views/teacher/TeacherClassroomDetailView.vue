<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'
import ConfirmModal from '../../components/ConfirmModal.vue'

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

const showConfirm = ref(false)
const confirmMessage = ref('')
const confirmAction = ref(null)

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
  openConfirm(
    'Treure aquest alumne de l\'aula?',
    async () => {
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
  )
}

function openConfirm(message, action) {
  confirmMessage.value = message
  confirmAction.value = action
  showConfirm.value = true
}

function handleConfirm() {
  confirmAction.value?.()
  showConfirm.value = false
}

onMounted(fetchData)
</script>

<template>
  <div class="font-sans">
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>

    <p
      v-else-if="error"
      class="font-mono text-sm text-red-600 bg-red-50 border border-red-100 px-4 py-3 rounded whitespace-pre-wrap"
    >
      {{ error }}
    </p>

    <div v-else>
      <div class="flex justify-end mb-4">
        <button
          class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 transition"
          @click="openAddModal"
        >
          Afegir alumne
        </button>
      </div>

      <p v-if="members.length === 0" class="text-gray-400 text-sm">
        No hi ha alumnes en aquesta aula.
      </p>

      <div v-else class="flex flex-col gap-4">
        <div
          v-for="member in members"
          :key="member.id"
          class="border border-gray-200 rounded-xl bg-white p-4"
        >
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-3">
            <div class="min-w-0">
              <p class="font-medium text-gray-900">
                {{ member.full_name ?? '—' }}
              </p>

              <p class="font-mono text-xs text-gray-500 mt-1 break-all">
                {{ member.email }}
              </p>
            </div>

            <button
              class="text-xs border border-red-200 rounded-lg px-2 py-1 text-red-600 hover:bg-red-50 transition w-full sm:w-auto"
              @click="removeMember(member.id)"
            >
              Treure
            </button>
          </div>

          <div v-if="getProgress(member.id).length === 0" class="text-xs text-gray-400">
            Sense activitat encara
          </div>

          <div v-else class="flex flex-col gap-1.5">
            <div
              v-for="p in getProgress(member.id)"
              :key="p.scenario_id"
              class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2 text-xs"
            >
              <span class="font-mono text-gray-700">
                Escenari {{ p.scenario_id }}
              </span>

              <span
                class="w-fit px-2 py-0.5 rounded-full font-medium"
                :class="p.success ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'"
              >
                {{ p.success ? 'Completat' : 'En progrés' }}
              </span>

              <span class="font-mono text-gray-400">
                {{ p.attempts }} intent{{ p.attempts !== 1 ? 's' : '' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal afegir alumne -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4 font-sans"
    >
      <div class="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Afegir alumne</h2>

        <select
          v-model="selectedStudentId"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
        >
          <option value="" disabled>Selecciona un alumne...</option>

          <option
            v-for="student in allStudents"
            :key="student.id"
            :value="student.id"
          >
            {{ student.full_name ?? student.email }} — {{ student.email }}
          </option>
        </select>

        <div class="flex justify-end gap-2 mt-6">
          <button
            class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition disabled:opacity-50"
            :disabled="adding || !selectedStudentId"
            @click="addMember"
          >
            {{ adding ? 'Afegint...' : 'Afegir' }}
          </button>

          <button
            class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
            @click="showAddModal = false"
          >
            Cancel·lar
          </button>
        </div>
      </div>
    </div>

    <ConfirmModal
      v-if="showConfirm"
      :message="confirmMessage"
      @confirm="handleConfirm"
      @cancel="showConfirm = false"
    />
  </div>
</template>