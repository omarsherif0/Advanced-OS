
def run(requests: list, initial: int, max_cylinder: int) -> tuple:
    head_movements = []
    current = initial
    total_movements = 0
    index = 1
    pending = requests.copy()

    while pending:
        greater_values = [x for x in pending if x > current]

        if not greater_values:
            total_movements += abs(max_cylinder - current) 
            head_movements.append(f"Step {index}: Head moved to {max_cylinder}")
            index += 1
            total_movements += max_cylinder
            head_movements.append(f"Step {index}: Head jumped to 0")
            index += 1
            current = 0
            continue

        closest = min(greater_values, key=lambda x: x - current)
        pending.remove(closest)
        total_movements += abs(closest - current)
        head_movements.append(f"Step {index}: Head moved to {closest}")
        current = closest
        index += 1

    return [head_movements,[], total_movements]
