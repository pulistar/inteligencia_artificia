import React, { useState } from 'react'
import { predictImage } from '../services/api'

function ImageClassifier() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      setResult(null)
    }
  }

  const handleClassify = async () => {
    if (!selectedFile) return

    setLoading(true)
    try {
      const prediction = await predictImage(selectedFile)
      setResult(prediction)
    } catch (error) {
      setResult({ error: 'Error al clasificar la imagen' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="classifier-section">
      <h2>Clasificador de Imágenes</h2>
      
      <div className="file-input-container">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="file-input"
        />
      </div>

      {previewUrl && (
        <div className="image-preview">
          <img src={previewUrl} alt="Preview" className="preview-image" />
        </div>
      )}

      <button
        onClick={handleClassify}
        disabled={!selectedFile || loading}
        className="classify-button"
      >
        {loading ? 'Clasificando...' : 'Clasificar'}
      </button>

      {result && (
        <div className="result-container">
          {result.error ? (
            <p className="error">{result.error}</p>
          ) : (
            <div className="result">
              <h3>Resultado:</h3>
              <p><strong>Clase:</strong> {result.clase}</p>
              <p><strong>Probabilidad:</strong> {result.probabilidad}%</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ImageClassifier
