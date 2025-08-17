import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { enqueueSequential, enqueueParallel } from '../services/api'

interface ControlsProps {
  mode: 'sequential' | 'parallel'
}

export function Controls({ mode }: ControlsProps) {
  const { token } = useAuth()
  const disabled = !token
  const [base, setBase] = useState(0)
  const [hombro, setHombro] = useState(0)
  const [codo, setCodo] = useState(0)
  const [joint, setJoint] = useState<'base' | 'hombro' | 'codo'>('base')
  const [angle, setAngle] = useState(0)
  const [message, setMessage] = useState<string | null>(null)

  const enqueue = async () => {
    if (!token) return
    try {
      if (mode === 'sequential') {
        await enqueueSequential({ joint, angle })
        setMessage(`Encolado ${joint}:${angle}`)
      } else {
        await enqueueParallel({ base, hombro, codo })
        setMessage(`Encolado paralelo (${base},${hombro},${codo})`)
      }
    } catch {
      setMessage('Error al encolar')
    }
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Controles <span className="text-xs text-slate-400">({mode === 'sequential' ? 'Secuencial' : 'Paralelo'})</span></h3>
      {mode === 'sequential' ? (
        <div className="space-y-2">
          <select className="input" value={joint} onChange={e => setJoint(e.target.value as any)} disabled={disabled}>
            <option value='base'>Base</option>
            <option value='hombro'>Hombro</option>
            <option value='codo'>Codo</option>
          </select>
          <div className="flex items-center gap-3">
            <input className="flex-1" type='range' min={0} max={180} value={angle} onChange={e => setAngle(Number(e.target.value))} disabled={disabled} />
            <span className="w-10 text-right text-xs text-slate-300">{angle}°</span>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-xs mb-1"><span>Base</span><span>{base}°</span></div>
            <input className="w-full" type='range' min={0} max={180} value={base} onChange={e => setBase(Number(e.target.value))} disabled={disabled} />
          </div>
          <div>
            <div className="flex justify-between text-xs mb-1"><span>Hombro</span><span>{hombro}°</span></div>
            <input className="w-full" type='range' min={0} max={180} value={hombro} onChange={e => setHombro(Number(e.target.value))} disabled={disabled} />
          </div>
          <div>
            <div className="flex justify-between text-xs mb-1"><span>Codo</span><span>{codo}°</span></div>
            <input className="w-full" type='range' min={0} max={180} value={codo} onChange={e => setCodo(Number(e.target.value))} disabled={disabled} />
          </div>
        </div>
      )}
      <div className="flex items-center gap-3">
        <button className="btn" onClick={enqueue} disabled={disabled}>Encolar</button>
        {message && <div className="text-xs text-slate-400">{message}</div>}
      </div>
    </div>
  )
}
