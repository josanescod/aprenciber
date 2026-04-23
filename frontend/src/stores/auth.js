import { reactive } from 'vue'
import { apiFetch } from '../services/api'
import {
  getSession,
  getUser,
  signInWithPassword,
  signOut,
} from '../services/auth.service'

export const authStore = reactive({
  session: null,
  user: null,
  profile: null,
  loading: false,
  error: null,
  initialized: false,

  async initialize() {
    this.loading = true
    this.error = null

    try {
      this.session = await getSession()

      if (this.session?.access_token) {
        this.user = await getUser()
        this.profile = await apiFetch('/api/users/me', this.session.access_token)
      }
    } catch (error) {
      this.error = error.message
    } finally {
      this.loading = false
      this.initialized = true
    }
  },

  async login(email, password) {
    this.loading = true
    this.error = null

    try {
      const data = await signInWithPassword(email, password)
      this.session = data.session
      this.user = data.user
      this.profile = await apiFetch('/api/users/me', data.session.access_token)
    } catch (error) {
      this.error = error.message
      throw error
    } finally {
      this.loading = false
    }
  },

  async logout() {
    await signOut()
    this.session = null
    this.user = null
    this.profile = null
    this.error = null
  },
})