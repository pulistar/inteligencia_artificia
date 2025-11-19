const API_BASE_URL = 'http://localhost:8000'

export const predictImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Error en la predicción')
  }

  return response.json()
}

export const sendChatMessage = async (message) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error('Error en el chat')
  }

  return response.json()
}
