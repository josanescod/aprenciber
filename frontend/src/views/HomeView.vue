<template>
  <main class="min-h-screen bg-white flex items-center justify-center px-4 py-8 font-sans">
    <section class="w-full max-w-3xl text-center space-y-6">

      <div class="bg-black text-white text-left p-4 sm:p-6 rounded font-mono max-w-full overflow-x-auto font-mono">
        <pre class="block sm:hidden text-xs leading-tight whitespace-pre"><code>Benvinguts a AprenCiber

user@aprenciber:~$</code></pre>

        <pre class="hidden sm:block text-sm leading-tight whitespace-pre"><code>Benvinguts a

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

      <nav class="text-sm flex items-center justify-center gap-3 flex-wrap">
        <RouterLink
          to="/login"
          class="text-gray-700 hover:text-black hover:underline"
        >
          Iniciar sessió
        </RouterLink>

        <span class="text-gray-400">|</span>

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