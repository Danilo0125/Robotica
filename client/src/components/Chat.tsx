import { useState } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'

export function Chat() {
  const { status, messages, send } = useWebSocket()
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim()) {
      send(input.trim())
      setInput('')
    }
  }

  return (
    <div>
      <h2>Chat ({status})</h2>
      <div style={{border: '1px solid #ccc', padding: 8, height: 150, overflowY: 'auto', marginBottom: 8}}>
        {messages.map((m, i) => <div key={i}>{m}</div>)}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder='Mensaje' />
      <button onClick={handleSend}>Enviar</button>
    </div>
  )
}
