import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { authStore } from './stores/auth'
import router from './router'

authStore.initialize()

createApp(App).use(router).mount('#app')
