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
    const errorBody = await response.json().catch(() => null)

    const error = new Error(
      errorBody?.detail?.message ||
      errorBody?.detail ||
      'API request failed'
    )

    error.status = response.status
    error.detail = errorBody?.detail

    throw error
  }
  
  const contentType = response.headers.get('content-type')

  if (response.status === 204 || !contentType?.includes('application/json')) {
    return null
  }
  return response.json()
}

export async function getScenarios(accessToken) {
  return apiFetch('/api/scenarios', accessToken)
}

export async function getScenario(id, accessToken) {
  return apiFetch(`/api/scenarios/${id}`, accessToken)
}

export async function startLab(scenarioSlug, accessToken) {
  return apiFetch('/api/labs/start', accessToken, {
    method: 'POST',
    body: JSON.stringify({
      scenario_slug: scenarioSlug,
    }),
  })
}

export async function getLab(labId, accessToken) {
  return apiFetch(`/api/labs/${labId}`, accessToken)
}

export async function deleteLab(labId, accessToken) {
  return apiFetch(`/api/labs/${labId}`, accessToken, {
    method: 'DELETE',
  })
}

// mostrar laboratoris actius
export async function getActiveLabs(accessToken) {
  return apiFetch('/api/labs/me/active', accessToken)
}

// validar la flag
export async function submitFlag(labId, flag, accessToken) {
  return apiFetch(`/api/labs/${labId}/submit`, accessToken, {
    method: 'POST',
    body: JSON.stringify({ flag }),
  })
}