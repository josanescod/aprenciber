import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '../stores/auth'

import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import ScenariosView from '../views/ScenariosView.vue'
import LabView from '../views/LabView.vue'
import ProgressView from '../views/ProgressView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import ScenarioDetailView from '../views/ScenarioDetailView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }, // only access it if user is logged in
  },
  {
    path: '/scenarios',
    name: 'scenarios',
    component: ScenariosView,
    meta: { requiresAuth: true }, // only access it if user is logged in
  },
  {
    path: '/scenarios/:id',
    name: 'scenario-detail',
    component: ScenarioDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/lab',
    name: 'lab',
    component: LabView,
    meta: { requiresAuth: true },
  },
  {
    path: '/progress',
    name: 'progress',
    component: ProgressView,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*', // Qualsevol ruta que no coincideixi amb les anteriors redirigir a NotFoundView
    name: 'not-found',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  if (!authStore.initialized) {
    await authStore.initialize()
  }

  const isAuthenticated = !!authStore.session

  if (to.meta.requiresAuth && !isAuthenticated) {
    return { name: 'login' }
  }

  if (to.meta.requiresGuest && isAuthenticated) {
    return { name: 'dashboard' }
  }
})

export default router