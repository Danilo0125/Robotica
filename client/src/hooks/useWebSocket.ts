import { useEffect, useRef, useState, useCallback } from 'react'

export interface UseWebSocketOptions {
  url?: string
  reconnectDelayMs?: number
}

export interface WebSocketState {
  status: string
  messages: string[]
  send: (msg: string) => void
}

export function useWebSocket(options: UseWebSocketOptions = {}): WebSocketState {
  const { url = 'ws://localhost:8000/ws', reconnectDelayMs = 2000 } = options
  const wsRef = useRef<WebSocket | null>(null)
  const [status, setStatus] = useState('desconectado')
  const [messages, setMessages] = useState<string[]>([])
  const retryRef = useRef<number | null>(null)

  const connect = useCallback(() => {
    setStatus('conectando')
    const socket = new WebSocket(url)
    wsRef.current = socket

    socket.onopen = () => setStatus('conectado')
    socket.onmessage = ev => setMessages(prev => [...prev, ev.data])
    socket.onerror = () => setStatus('error')
    socket.onclose = () => {
      setStatus('desconectado')
      if (retryRef.current === null) {
        retryRef.current = window.setTimeout(() => {
          retryRef.current = null
          connect()
        }, reconnectDelayMs)
      }
    }
  }, [url, reconnectDelayMs])

  useEffect(() => {
    connect()
    return () => {
      if (retryRef.current) window.clearTimeout(retryRef.current)
      wsRef.current?.close()
    }
  }, [connect])

  const send = useCallback((msg: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(msg)
    }
  }, [])

  return { status, messages, send }
}
