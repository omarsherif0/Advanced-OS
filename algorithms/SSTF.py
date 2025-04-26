def run(requests: list, initial: int, max_cylinder: int) -> tuple: 
    current = initial
    total_movements = 0
    head_movements = []
    requests = [r for r in requests if r <= max_cylinder]
    index = 1

    while requests:
        closest_cylinder_index = min(
            range(len(requests)),
            key=lambda index: (abs(requests[index] - current), -requests[index])
        )
        total_movements += abs(current - requests[closest_cylinder_index])
        closest = requests.pop(closest_cylinder_index)
        current = closest
        head_movements.append(f"Step {index}: Head moved to {closest}")
        index += 1

    return (head_movements,[], total_movements)
