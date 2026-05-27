<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import { apiFetch } from '../services/api'
import { authStore } from '../stores/auth'

const router = useRouter()
const isStudent = computed(() => authStore.profile?.role === 'student')

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
</script>

<template>
  <AppLayout>
    <div class="font-sans">
      <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

      <div class="border rounded p-4 max-w-md bg-white">
        <h2 class="font-semibold mb-3 text-gray-900">El teu perfil</h2>
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
            @click="showConfirm = true"
          >
            {{ deleting ? 'Eliminant...' : 'Eliminar el meu compte' }}
          </button>
        </div>
      </div>
    </div>

    <ConfirmModal
      v-if="showConfirm"
      message="Estàs segur que vols eliminar el teu compte? Aquesta acció és irreversible i s'esborraran totes les teves dades."
      @confirm="deleteAccount"
      @cancel="showConfirm = false"
    />
  </AppLayout>
</template>