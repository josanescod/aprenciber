import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '../stores/auth'

import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import ScenariosView from '../views/ScenariosView.vue'
import LabView from '../views/LabView.vue'
import ProgressView from '../views/ProgressView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import ScenarioDetailView from '../views/ScenarioDetailView.vue'
import RegisterView from '../views/RegisterView.vue'
import AuthCallbackView from '../views/AuthCallbackView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresGuest: true },

  },
  {
    path: '/auth/callback',
    name: 'auth-callback',
    component: AuthCallbackView
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
    path: '/labs/:id',
    name: 'lab-detail',
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
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminView.vue'), // lazy load perquè no carregui aquesta vista per a tots els usuaris
    meta: { requiresAuth: true, requiresRole: 'admin' }
  },
  {
    path: '/teacher',
    name: 'teacher',
    component: () => import('../views/TeacherView.vue'),
    meta: { requiresAuth: true, requiresRole: 'teacher' }, // lazy load perquè no carregui aquesta vista per a tots els usuaris
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

  // Guardar el rol si la ruta requereix un rol específic
  if (to.meta.requiresRole) {
    const role = authStore.profile?.role
    if (to.meta.requiresRole === 'admin' && role !== 'admin') {
      return { name: 'dashboard' }
    }
    if (to.meta.requiresRole === 'teacher' && !['teacher', 'admin'].includes(role)) {
      return { name: 'dashboard' }
    }
  }
})

export default router