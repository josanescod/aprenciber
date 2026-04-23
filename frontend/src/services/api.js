const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export async function apiFetch(path, accessToken, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options.headers || {}),
    },
  })

  if (!response.ok) {
    const message = await response.text()
    const error = new Error(message || 'API request failed')
    error.status = response.status
    //console.log('[apiFetch] error.status assigned:', error.status)
    throw error
  }

  return response.json()
}

export async function getScenarios(accessToken) {
  return apiFetch('/api/scenarios', accessToken)
}

export async function getScenario(id, accessToken) {
  return apiFetch(`/api/scenarios/${id}`, accessToken)
}