<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import { apiFetch } from '../services/api'
import { authStore } from '../stores/auth'

const router = useRouter()
const isStudent = computed(() => authStore.profile?.role === 'student')

// Eliminar compte
const showConfirm = ref(false)
const deleting = ref(false)

async function deleteAccount() {
  deleting.value = true
  try {
    const token = authStore.session?.access_token
    await apiFetch('/api/users/me', token, { method: 'DELETE' })
    await authStore.logout()
    router.push({ name: 'home' })
  } catch (err) {
    console.error('Error eliminant compte:', err)
  } finally {
    deleting.value = false
  }
}

// Editar perfil
const showEditModal = ref(false)
const saving = ref(false)
const saveError = ref(null)
const saveSuccess = ref(false)
const editForm = ref({ full_name: '', password: '', password_confirm: '' })

function openEditModal() {
  editForm.value = { full_name: authStore.profile?.full_name ?? '', password: '', password_confirm: '' }
  saveError.value = null
  saveSuccess.value = false
  showEditModal.value = true
}

async function saveProfile() {
  saving.value = true
  saveError.value = null
  saveSuccess.value = false
  try {
    if (editForm.value.password && editForm.value.password !== editForm.value.password_confirm) {
      saveError.value = 'Les contrasenyes no coincideixen'
      return
    }
    const token = authStore.session?.access_token
    const body = { full_name: editForm.value.full_name }
    if (editForm.value.password) {
      body.password = editForm.value.password
    }
    const updated = await apiFetch('/api/users/me', token, {
      method: 'PATCH',
      body: JSON.stringify(body),
    })
    authStore.profile = { ...authStore.profile, ...updated }
    saveSuccess.value = true
    setTimeout(() => { showEditModal.value = false }, 1000)
  } catch (err) {
    saveError.value = 'Error actualitzant el perfil'
    console.error(err)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <AppLayout>
    <div class="font-sans">
      <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

      <div class="border rounded p-4 max-w-md bg-white">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold text-gray-900">El teu perfil</h2>
          <button
            class="text-xs border border-gray-300 rounded-lg px-3 py-1.5 text-gray-700 hover:bg-gray-100 transition"
            @click="openEditModal">
            Editar
          </button>
        </div>

        <div class="space-y-2 text-sm">
          <p>
            <span class="text-gray-500">Email:</span>
            <span class="font-mono text-xs text-gray-700 break-all">
              {{ authStore.profile?.email }}
            </span>
          </p>
          <p>
            <span class="text-gray-500">Rol:</span>
            <span class="font-mono text-xs font-semibold uppercase tracking-wide text-gray-900">
              {{ authStore.profile?.role }}
            </span>
          </p>
          <p>
            <span class="text-gray-500">Nom:</span>
            <span class="text-gray-900">
              {{ authStore.profile?.full_name ?? '—' }}
            </span>
          </p>
        </div>

        <!-- Botó eliminar compte — només students -->
        <div v-if="isStudent" class="mt-6 pt-4 border-t border-gray-100">
          <button
            class="text-sm text-red-600 border border-red-200 rounded-lg px-3 py-1.5 hover:bg-red-50 transition disabled:opacity-50"
            :disabled="deleting"
            @click="showConfirm = true">
            {{ deleting ? 'Eliminant...' : 'Eliminar el meu compte' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal editar perfil -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Editar perfil</h2>

        <div class="flex flex-col gap-3">
          <div>
            <label class="text-xs text-gray-500 mb-1 block">Nom complet</label>
            <input v-model="editForm.full_name" type="text" placeholder="Nom complet"
              class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none focus:border-gray-500" />
          </div>

          <div>
            <label class="text-xs text-gray-500 mb-1 block">Nova contrasenya (opcional)</label>
            <input v-model="editForm.password" type="password" placeholder="Deixa buit per no canviar"
              class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none focus:border-gray-500" />
            <p v-if="editForm.password && editForm.password.length < 8" class="text-red-500 text-xs mt-1">
              Mínim 8 caràcters
            </p>
          </div>

          <div>
            <label class="text-xs text-gray-500 mb-1 block">Confirmar contrasenya</label>
            <input v-model="editForm.password_confirm" type="password" placeholder="Repeteix la contrasenya"
              class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-full focus:outline-none focus:border-gray-500" />
            <p v-if="editForm.password && editForm.password_confirm && editForm.password !== editForm.password_confirm"
              class="text-red-500 text-xs mt-1">
              Les contrasenyes no coincideixen
            </p>
          </div>
        </div>

        <p v-if="saveError" class="text-red-600 text-xs mt-3">{{ saveError }}</p>
        <p v-if="saveSuccess" class="text-green-600 text-xs mt-3">Perfil actualitzat correctament ✓</p>

        <div class="flex justify-end gap-2 mt-6">
          <button
            class="text-sm px-4 py-2 rounded border border-gray-300 hover:bg-gray-100 transition"
            @click="showEditModal = false">
            Cancel·lar
          </button>
          <button
            class="text-sm px-4 py-2 rounded bg-black text-white hover:bg-gray-800 disabled:opacity-50 transition"
            :disabled="saving || (!!editForm.password && editForm.password.length < 8) || (!!editForm.password && editForm.password !== editForm.password_confirm)"
            @click="saveProfile">
            {{ saving ? 'Guardant...' : 'Guardar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal confirmar eliminar compte -->
    <ConfirmModal
      v-if="showConfirm"
      message="Estàs segur que vols eliminar el teu compte? Aquesta acció és irreversible i s'esborraran totes les teves dades."
      @confirm="deleteAccount"
      @cancel="showConfirm = false"
    />
  </AppLayout>
</template>