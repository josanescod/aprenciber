<template>
  <main class="max-w-md mx-auto p-6 mt-20">
    <div class="border rounded p-8 text-center space-y-6">

      <h1 class="text-2xl font-bold">Benvingut a AprenCiber</h1>

      <div class="space-y-3">
        <RouterLink
          to="/login"
          class="block border px-4 py-2 rounded hover:bg-gray-50"
        >
          Iniciar sessió
        </RouterLink>
        <RouterLink
          to="/register"
          class="block border px-4 py-2 rounded hover:bg-gray-50"
        >
          Crear compte
        </RouterLink>
      </div>

    </div>
  </main>
</template>