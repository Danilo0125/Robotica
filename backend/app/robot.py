"""Robot state & queue endpoints (sequential & parallel)."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends
import asyncio
import time
from pydantic import BaseModel, Field
from typing import List
from .auth import get_current_admin
from app.websocket.manager import manager
from app.core.config import Settings
import json

settings = Settings()
router = APIRouter(prefix="/robot", tags=["robot"])

# In-memory storage (replace with Firebase persistence as needed)
robot_state = {"base": 0, "hombro": 0, "codo": 0}
sequential_queue: List[dict] = []  # each item: {joint: str, angle: int, duration_ms: int}
parallel_queue: List[dict] = []    # each item: {base: int, hombro: int, codo: int, duration_ms: int}
_simulation_lock = asyncio.Lock()
_simulation_running = False
_simulation_mode: str | None = None

class State(BaseModel):
    base: int = Field(ge=0, le=180)
    hombro: int = Field(ge=0, le=180)
    codo: int = Field(ge=0, le=180)

class SequentialItem(BaseModel):
    joint: str
    angle: int = Field(ge=0, le=180)
    duration_ms: int = Field(default=1000, ge=50, le=60000)

class ParallelItem(State):
    duration_ms: int = Field(default=1000, ge=50, le=60000)

class TokenHeader(BaseModel):
    token: str

AdminDep = Depends(get_current_admin)

@router.get("/state", response_model=State)
async def get_state():
    return State(**robot_state)

@router.post("/state", response_model=State)
async def set_state(new_state: State, _admin: str = AdminDep):
    robot_state.update(new_state.dict())
    await _broadcast_event("STATE_UPDATE", robot_state)
    return new_state

# Sequential
@router.post("/sequential/enqueue")
async def enqueue_seq(item: SequentialItem, _admin: str = AdminDep):
    if item.joint not in robot_state:
        raise HTTPException(400, detail="Joint inválido")
    sequential_queue.append(item.dict())
    return {"queued": item}

@router.get("/sequential/list")
async def list_seq():
    return sequential_queue

@router.post("/sequential/reset")
async def reset_seq(_admin: str = AdminDep):
    sequential_queue.clear()
    return {"detail": "cola secuencial vacía"}

@router.post("/sequential/start")
async def start_seq(_admin: str = AdminDep):
    global _simulation_running, _simulation_mode
    if _simulation_running:
        raise HTTPException(409, detail="Simulación en curso")
    if not sequential_queue:
        return {"executed": [], "state": robot_state}
    _simulation_running = True
    _simulation_mode = "sequential"
    async def runner():
        ran = []
        try:
            while sequential_queue:
                step = sequential_queue.pop(0)
                await _animate_sequential_step(step)
                ran.append(step)
            await _broadcast_event("STATE_UPDATE", robot_state)
        finally:
            nonlocal_ran[:] = ran  # store result
            _end_simulation()
    nonlocal_ran: List[dict] = []
    asyncio.create_task(runner())
    return {"detail": "Simulación secuencial iniciada"}

# Parallel
@router.post("/parallel/enqueue")
async def enqueue_parallel(item: ParallelItem, _admin: str = AdminDep):
    parallel_queue.append(item.dict())
    return {"queued": item}

@router.get("/parallel/list")
async def list_parallel():
    return parallel_queue

@router.post("/parallel/reset")
async def reset_parallel(_admin: str = AdminDep):
    parallel_queue.clear()
    return {"detail": "cola paralela vacía"}

@router.post("/parallel/start")
async def start_parallel(_admin: str = AdminDep):
    global _simulation_running, _simulation_mode
    if _simulation_running:
        raise HTTPException(409, detail="Simulación en curso")
    if not parallel_queue:
        return {"executed": [], "state": robot_state}
    _simulation_running = True
    _simulation_mode = "parallel"
    async def runner():
        ran = []
        try:
            while parallel_queue:
                block = parallel_queue.pop(0)
                await _animate_parallel_block(block)
                ran.append(block)
            await _broadcast_event("STATE_UPDATE", robot_state)
        finally:
            _end_simulation()
    asyncio.create_task(runner())
    return {"detail": "Simulación paralela iniciada"}

# ----- Simulation helpers -----

def _end_simulation():
    global _simulation_running, _simulation_mode
    _simulation_running = False
    _simulation_mode = None

async def _animate_sequential_step(step: dict):
    joint = step['joint']
    target = step['angle']
    duration = step.get('duration_ms', 1000)
    start_angle = robot_state[joint]
    await _broadcast_event("MOVE_SEQ_START", step)
    if duration <= 0 or target == start_angle:
        robot_state[joint] = target
        await _broadcast_event("STATE_UPDATE", robot_state)
        await _broadcast_event("MOVE_SEQ_END", step)
        return
    interval = 0.05  # 50 ms
    steps = max(1, int(duration / (interval * 1000)))
    for i in range(1, steps + 1):
        factor = i / steps
        robot_state[joint] = round(start_angle + (target - start_angle) * factor)
        await _broadcast_event("STATE_UPDATE", robot_state)
        await asyncio.sleep(interval)
    await _broadcast_event("MOVE_SEQ_END", step)

async def _animate_parallel_block(block: dict):
    duration = block.get('duration_ms', 1000)
    start_state = robot_state.copy()
    targets = {k: block[k] for k in ['base','hombro','codo'] if k in block}
    await _broadcast_event("MOVE_PAR_START", block)
    if duration <= 0:
        robot_state.update(targets)
        await _broadcast_event("STATE_UPDATE", robot_state)
        await _broadcast_event("MOVE_PAR_END", block)
        return
    interval = 0.05
    steps = max(1, int(duration / (interval * 1000)))
    for i in range(1, steps + 1):
        factor = i / steps
        for joint, target in targets.items():
            s = start_state[joint]
            robot_state[joint] = round(s + (target - s) * factor)
        await _broadcast_event("STATE_UPDATE", robot_state)
        await asyncio.sleep(interval)
    await _broadcast_event("MOVE_PAR_END", block)

@router.get("/status")
async def simulation_status():
    return {
        "running": _simulation_running,
        "mode": _simulation_mode,
        "sequential_queue_len": len(sequential_queue),
        "parallel_queue_len": len(parallel_queue),
        "state": robot_state,
    }

async def _broadcast_event(event_type: str, payload: dict):
    message = json.dumps({"type": event_type, "payload": payload})
    await manager.broadcast(message)

