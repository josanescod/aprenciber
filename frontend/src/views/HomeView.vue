<template>
  <main class="min-h-screen bg-white flex items-center justify-center px-6">
    <section class="w-full max-w-3xl text-center space-y-6">

      <div class="bg-black text-white text-left p-6 rounded font-mono text-sm overflow-x-auto">
        <pre><code>Benvinguts a

  ___                       _____ _ _
 / _ \                     /  __ (_) |
/ /_\ \_ __  _ __ ___ _ __ | /  \/_| |__   ___ _ __
|  _  | '_ \| '__/ _ \ '_ \| |   | | '_ \ / _ \ '__|
| | | | |_) | | |  __/ | | | \__/\ | |_) |  __/ |
\_| |_/ .__/|_|  \___|_| |_|\____/_|_.__/ \___|_|
      | |
      |_|

user@aprenciber:~$</code></pre>
      </div>

      <nav class="text-sm">
        <RouterLink
          to="/login"
          class="text-gray-700 hover:text-black hover:underline"
        >
          Iniciar sessió
        </RouterLink>

        <span class="mx-3 text-gray-400">|</span>

        <RouterLink
          to="/register"
          class="text-gray-700 hover:text-black hover:underline"
        >
          Crear compte
        </RouterLink>
      </nav>

    </section>
  </main>
</template>