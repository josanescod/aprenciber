<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../services/supabase'

const router = useRouter()

onMounted(async () => {
    const { data: { session } } = await supabase.auth.getSession()

    if (session) {
        router.push({ name: 'dashboard' })
    } else {
        // Link expirat o ja utilitzat
        router.push({ name: 'login' })
    }
})
</script>

<template>
    <main class="max-w-md mx-auto p-6 text-center">
        <p class="text-gray-500">Verificant sessió...</p>
    </main>
</template>
