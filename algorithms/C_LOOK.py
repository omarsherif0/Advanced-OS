def run(requests: list, initial: int, max_cylinder: int) -> dict:
    headMovement = []
    totalMovement = 0
    pending = requests.copy()
    pending.sort()
    currentPointer = initial

    # Logic
    start = 0
    if initial in pending:
        start = pending.index(initial)
    else:
        start = next((i for i, val in enumerate(pending) if val > initial))

    i = start
    while i < len(pending):
        val = pending.pop(i)
        headMovement.append(val)
        movement = abs(currentPointer - val)
        totalMovement += movement
        currentPointer = val

    while len(pending):
        val = pending.pop(0)
        headMovement.append(val)
        movement = abs(currentPointer - val)
        totalMovement += movement
        currentPointer = val

    # Output
    return {
        "frame_states": headMovement,
        "logs": [],
        "faults": totalMovement,
    }
