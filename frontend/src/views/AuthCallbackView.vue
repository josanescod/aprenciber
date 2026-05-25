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
    <main class="min-h-screen flex items-center justify-center px-4 font-sans">
        <div class="max-w-md text-center">
            <p class="font-mono text-sm text-gray-500">
                Verificant sessió...
            </p>
        </div>
    </main>
</template>
