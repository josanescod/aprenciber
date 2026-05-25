<template>
  <div class="min-h-screen flex flex-col items-center justify-center text-center p-6 font-sans">
    <h1 class="font-mono text-6xl font-bold mb-4 text-gray-900">
      404
    </h1>

    <p class="text-gray-500 mb-6">
      La pàgina que busques no existeix.
    </p>

    <RouterLink
      to="/"
      class="border rounded px-4 py-2 hover:bg-gray-100 text-sm transition-colors"
    >
      Tornar a l'inici
    </RouterLink>
  </div>
</template>