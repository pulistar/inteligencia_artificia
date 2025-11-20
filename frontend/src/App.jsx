import React from 'react'
import ImageClassifier from './components/ImageClassifier'
import NutritionChatbot from './components/NutritionChatbot'
import GeminiChat from './components/GeminiChat'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Clasificación de Alimentos para Asistentes de Nutrición</h1>
      </header>
      <main className="App-main">
        <div className="sections-container">
          <ImageClassifier />
          <NutritionChatbot />
        </div>
      </main>
      
      {/* Botón flotante de Gemini */}
      <GeminiChat />
    </div>
  )
}

export default App
