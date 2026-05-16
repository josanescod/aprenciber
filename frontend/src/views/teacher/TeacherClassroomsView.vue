<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../../services/api'
import { authStore } from '../../stores/auth'

const classrooms = ref([])
const loading = ref(true)
const error = ref(null)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingClassroom = ref(null)
const newClassroom = ref({ name: '', description: '' })
const saving = ref(false)

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
  if (!confirm(`Eliminar "${classroom.name}"?`)) return
  try {
    const token = authStore.session?.access_token
    await apiFetch(`/api/classrooms/${classroom.id}`, token, { method: 'DELETE' })
    classrooms.value = classrooms.value.filter(c => c.id !== classroom.id)
  } catch (err) {
    console.error('Error eliminant aula:', err)
  }
}

function openEditModal(classroom) {
  editingClassroom.value = { ...classroom }
  showEditModal.value = true
}


onMounted(fetchClassrooms)
</script>

<template>
  <div>
    <p v-if="loading" class="text-gray-500 text-sm">Carregant...</p>
    <p v-else-if="error" class="text-red-600 text-sm">{{ error }}</p>
    <div v-else>
      <div class="flex justify-end mb-4">
        <button class="text-sm border rounded px-3 py-1 hover:bg-gray-100" @click="showCreateModal = true">
          Nova aula
        </button>
      </div>

      <p v-if="classrooms.length === 0" class="text-gray-400 text-sm">No tens cap aula creada.</p>
      <div v-else class="flex flex-col gap-3">
        <div v-for="classroom in classrooms" :key="classroom.id"
          class="border rounded p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
          <RouterLink :to="{ name: 'teacher-classroom-detail', params: { id: classroom.id } }" class="flex-1">
            <p class="font-medium">{{ classroom.name }}</p>
            <p class="text-sm text-gray-500 mt-1">{{ classroom.description ?? '—' }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ classroom.member_count }} alumne{{ classroom.member_count !== 1 ?
              's' : '' }}</p>
          </RouterLink>
          <div class="flex gap-2 ml-4">
            <button class="text-sm border rounded px-3 py-1 hover:bg-gray-100"
              @click.prevent="openEditModal(classroom)">
              Editar
            </button>
            <button class="text-sm border rounded px-3 py-1 text-red-600 hover:bg-red-50"
              @click.prevent="deleteClassroom(classroom)">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal crear -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
        <h2 class="text-lg font-bold mb-4">Nova aula</h2>
        <div class="flex flex-col gap-3">
          <input v-model="newClassroom.name" type="text" placeholder="Nom de l'aula"
            class="border rounded px-3 py-2 text-sm" />
          <input v-model="newClassroom.description" type="text" placeholder="Descripció (opcional)"
            class="border rounded px-3 py-2 text-sm" />
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button class="text-sm px-4 py-2 rounded border hover:bg-gray-100" @click="showCreateModal = false">
            Cancel·lar
          </button>
          <button class="text-sm px-4 py-2 rounded bg-black text-white hover:bg-gray-800 disabled:opacity-50"
            :disabled="saving || !newClassroom.name" @click="createClassroom">
            {{ saving ? 'Creant...' : 'Crear' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal editar -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
        <h2 class="text-lg font-bold mb-4">Editar aula</h2>
        <div class="flex flex-col gap-3">
          <input v-model="editingClassroom.name" type="text" placeholder="Nom de l'aula"
            class="border rounded px-3 py-2 text-sm" />
          <input v-model="editingClassroom.description" type="text" placeholder="Descripció (opcional)"
            class="border rounded px-3 py-2 text-sm" />
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button class="text-sm px-4 py-2 rounded border hover:bg-gray-100" @click="showEditModal = false">
            Cancel·lar
          </button>
          <button class="text-sm border rounded px-3 py-1 hover:bg-gray-100"
            :disabled="saving || !editingClassroom.name" @click="updateClassroom">
            {{ saving ? 'Guardant...' : 'Guardar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>