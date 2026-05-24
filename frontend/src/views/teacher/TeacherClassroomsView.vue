<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'
import ConfirmModal from '../../components/ConfirmModal.vue'

const classrooms = ref([])
const loading = ref(true)
const error = ref(null)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingClassroom = ref(null)
const newClassroom = ref({ name: '', description: '' })
const saving = ref(false)

const showConfirm = ref(false)
const confirmMessage = ref('')
const confirmAction = ref(null)


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

async function createClassroom() {
  if (!newClassroom.value.name) return
  saving.value = true
  try {
    const token = authStore.session?.access_token
    const created = await apiFetch('/api/classrooms/', token, {
      method: 'POST',
      body: JSON.stringify(newClassroom.value),
    })
    classrooms.value.unshift(created)
    showCreateModal.value = false
    newClassroom.value = { name: '', description: '' }
  } catch (err) {
    console.error('Error creant aula:', err)
  } finally {
    saving.value = false
  }
}

async function updateClassroom() {
  if (!editingClassroom.value?.name) return
  saving.value = true
  try {
    const token = authStore.session?.access_token
    const updated = await apiFetch(`/api/classrooms/${editingClassroom.value.id}`, token, {
      method: 'PATCH',
      body: JSON.stringify({
        name: editingClassroom.value.name,
        description: editingClassroom.value.description,
      }),
    })
    const index = classrooms.value.findIndex(c => c.id === updated.id)
    if (index !== -1) classrooms.value.splice(index, 1, updated)
    showEditModal.value = false
    editingClassroom.value = null
  } catch (err) {
    console.error('Error actualitzant aula:', err)
  } finally {
    saving.value = false
  }
}

async function deleteClassroom(classroom) {
  openConfirm(
    `Eliminar l'aula "${classroom.name}"?`,
    async () => {
      try {
        const token = authStore.session?.access_token
        await apiFetch(`/api/classrooms/${classroom.id}`, token, { method: 'DELETE' })
        classrooms.value = classrooms.value.filter(c => c.id !== classroom.id)
      } catch (err) {
        console.error('Error eliminant aula:', err)
      }
    }
  )
}

function openEditModal(classroom) {
  editingClassroom.value = { ...classroom }
  showEditModal.value = true
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

onMounted(fetchClassrooms)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>

    <div v-else>
      <div class="flex justify-end mb-4">
        <button class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 transition"
          @click="showCreateModal = true">
          Nova aula
        </button>
      </div>

      <p v-if="classrooms.length === 0" class="text-gray-400 text-sm">
        No tens cap aula creada.
      </p>

      <div v-else class="flex flex-col gap-3">
        <div v-for="classroom in classrooms" :key="classroom.id"
          class="border border-gray-200 rounded-xl bg-white p-4 flex items-center justify-between hover:bg-gray-50 transition">
          <RouterLink :to="{ name: 'teacher-classroom-detail', params: { id: classroom.id } }" class="flex-1">
            <p class="font-medium text-gray-900">{{ classroom.name }}</p>
            <p class="text-sm text-gray-500 mt-1">{{ classroom.description ?? '—' }}</p>
            <p class="text-xs text-gray-400 mt-1">
              {{ classroom.member_count }} alumne{{ classroom.member_count !== 1 ? 's' : '' }}
            </p>
          </RouterLink>

          <div class="flex gap-2 ml-4">
            <button
              class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 transition"
              @click.prevent="openEditModal(classroom)">
              Editar
            </button>

            <button class="border border-red-200 rounded-lg px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 transition"
              @click.prevent="deleteClassroom(classroom)">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal crear -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Nova aula</h2>

        <div class="flex flex-col gap-3">
          <input v-model="newClassroom.name" type="text" placeholder="Nom de l'aula"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500" />

          <input v-model="newClassroom.description" type="text" placeholder="Descripció (opcional)"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500" />
        </div>

        <div class="flex justify-end gap-2 mt-6">
          <button
            class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition disabled:opacity-50"
            :disabled="saving || !newClassroom.name" @click="createClassroom">
            {{ saving ? 'Creant...' : 'Crear' }}
          </button>

          <button class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
            @click="showCreateModal = false">
            Cancel·lar
          </button>
        </div>
      </div>
    </div>

    <!-- Modal editar -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Editar aula</h2>

        <div class="flex flex-col gap-3">
          <input v-model="editingClassroom.name" type="text" placeholder="Nom de l'aula"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500" />

          <input v-model="editingClassroom.description" type="text" placeholder="Descripció (opcional)"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-gray-500" />
        </div>

        <div class="flex justify-end gap-2 mt-6">
          <button
            class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition disabled:opacity-50"
            :disabled="saving || !editingClassroom.name" @click="updateClassroom">
            {{ saving ? 'Guardant...' : 'Guardar' }}
          </button>

          <button class="border border-gray-300 rounded-lg px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition"
            @click="showEditModal = false">
            Cancel·lar
          </button>
        </div>
      </div>
    </div>
    <ConfirmModal v-if="showConfirm" :message="confirmMessage" @confirm="handleConfirm" @cancel="showConfirm = false" />
  </div>
</template>