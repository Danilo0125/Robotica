import { useEffect, useState } from 'react'
import { listSequential, listParallel, startSequential, startParallel, resetSequential, resetParallel } from '../services/api'
import { useAuth } from '../context/AuthContext'

interface MovementListProps { mode: 'sequential' | 'parallel' }

export function MovementList({ mode }: MovementListProps) {
  const [items, setItems] = useState<any[]>([])
  const { token } = useAuth()
  const disabled = !token

  const refresh = async () => {
    const data = mode === 'sequential' ? await listSequential() : await listParallel()
    setItems(data)
  }

  useEffect(() => { refresh() }, [mode])

  const start = async () => {
  if (!token) return
  mode === 'sequential' ? await startSequential() : await startParallel()
    refresh()
  }

  const reset = async () => {
  if (!token) return
  mode === 'sequential' ? await resetSequential() : await resetParallel()
    refresh()
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-lg font-semibold">Cola <span className="text-xs text-slate-400">({mode === 'sequential' ? 'Secuencial' : 'Paralelo'})</span></h4>
        <div className="flex gap-2">
          <button className="btn" onClick={refresh}>Actualizar</button>
          <button className="btn" onClick={start} disabled={disabled}>Iniciar</button>
          <button className="btn" onClick={reset} disabled={disabled}>Reset</button>
        </div>
      </div>
      <ul className="flex-1 overflow-auto space-y-1 text-xs font-mono">
        {items.map((it, i) => (
          <li key={i} className="px-2 py-1 rounded bg-slate-800/70 border border-slate-700/60">
            {JSON.stringify(it)}
          </li>
        ))}
        {items.length === 0 && <li className="text-slate-500">(vacío)</li>}
      </ul>
    </div>
  )
}
