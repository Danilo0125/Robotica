import axios from 'axios'

const API_BASE = 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
})

export function setAuthToken(token?: string) {
  if (token) api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  else delete api.defaults.headers.common['Authorization']
}

export interface LoginResponse { access_token: string }

export async function login(username: string, password: string) {
  const { data } = await api.post<LoginResponse>('/auth/login', { username, password })
  return data
}

export async function logout(token: string) {
  await api.post('/auth/logout', { token })
}

export async function getRobotState() {
  const { data } = await api.get('/robot/state')
  return data
}

export async function setRobotState(state: { base: number; hombro: number; codo: number }) {
  const { data } = await api.post(`/robot/state`, state)
  return data
}

// Sequential
export async function enqueueSequential(item: { joint: string; angle: number }) {
  const { data } = await api.post(`/robot/sequential/enqueue`, item)
  return data
}
export async function startSequential() {
  const { data } = await api.post(`/robot/sequential/start`)
  return data
}
export async function resetSequential() {
  const { data } = await api.post(`/robot/sequential/reset`)
  return data
}
export async function listSequential() {
  const { data } = await api.get(`/robot/sequential/list`)
  return data
}

// Parallel
export async function enqueueParallel(item: { base: number; hombro: number; codo: number }) {
  const { data } = await api.post(`/robot/parallel/enqueue`, item)
  return data
}
export async function startParallel() {
  const { data } = await api.post(`/robot/parallel/start`)
  return data
}
export async function resetParallel() {
  const { data } = await api.post(`/robot/parallel/reset`)
  return data
}
export async function listParallel() {
  const { data } = await api.get(`/robot/parallel/list`)
  return data
}
