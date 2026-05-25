<script setup>
defineProps({
  message: String,
})

defineEmits(['confirm', 'cancel'])
</script>

<template>
  <div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4 font-sans">
    <div class="bg-white rounded-lg p-6 w-full max-w-sm shadow-xl">
      <p class="text-sm text-gray-700 mb-6 leading-relaxed">
        {{ message }}
      </p>

      <div class="flex justify-end gap-2">
        <button
          class="text-sm px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 transition-colors"
          @click="$emit('confirm')"
        >
          Confirmar
        </button>

        <button
          class="text-sm px-4 py-2 rounded border hover:bg-gray-100 transition-colors"
          @click="$emit('cancel')"
        >
          Cancel·lar
        </button>
      </div>
    </div>
  </div>
</template>