import { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!query.trim()) {
      setError('Please enter a question')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      if (!res.ok) {
        throw new Error('Failed to get response')
      }

      const data = await res.json()
      setResponse(data)
      setQuery('')
    } catch (err) {
      setError(err.message || 'Error fetching response')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="chat-box">
        <h1>Shopping Mall Assistant</h1>
        <p>Ask me about stores, hours, and promotions</p>

        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What would you like to know?"
            disabled={loading}
            className="input"
          />
          <button type="submit" disabled={loading} className="button">
            {loading ? 'Loading...' : 'Send'}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {response && (
          <div className="response">
            <h3>Answer:</h3>
            <p>{response.answer}</p>

            {response.sources && response.sources.length > 0 && (
              <div className="sources">
                <h4>Sources:</h4>
                {response.sources.map((source, idx) => (
                  <div key={idx} className="source-item">
                    {source.text}
                  </div>
                ))}
              </div>
            )}

            <p className="latency">
              Response time: {response.latency_ms?.toFixed(0) || 'N/A'}ms
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App