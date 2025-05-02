
def run(requests: list, initial: int, max_cylinder: int) -> dict:
    head_movements = [initial]
    current = initial
    total_movements = 0
    index = 1
    pending = requests.copy()

    while pending:
        greater_values = [x for x in pending if x > current]

        if not greater_values:
            total_movements += abs(max_cylinder - current) 
            head_movements.append(max_cylinder)
            index += 1
            total_movements += max_cylinder
            head_movements.append(0)
            index += 1
            current = 0
            continue

        closest = min(greater_values, key=lambda x: x - current)
        pending.remove(closest)
        total_movements += abs(closest - current)
        head_movements.append(closest)
        current = closest
        index += 1
    return {
        "frame_states": head_movements,
        "logs": [],
        "faults": total_movements,
    }
