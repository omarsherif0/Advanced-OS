def run(requests: list, initial: int, maxCylinder: int) -> dict:
    headMovement = []
    totalMovement = 0
    pending = requests.copy()
    pending.sort()
    currentPointer = initial

    start = 0
    if initial in pending:
        start = pending.index(initial)
    else:
        start = next((i for i, val in enumerate(pending) if val > initial))

    i = start
    headMovement.append(initial)
    while i < len(pending):
        val = pending.pop(i)
        headMovement.append(val)
        movement = abs(currentPointer - val)
        totalMovement += movement
        currentPointer = val

    headMovement.append(maxCylinder)
    movement = abs(currentPointer - maxCylinder)
    totalMovement += movement
    currentPointer = maxCylinder

    while len(pending):
        val = pending.pop(-1)
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
