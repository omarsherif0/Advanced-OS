from algorithms import SC, lru, ARB, C_SCAN, SSTF, optimal, FIFO, SCAN, LOOK, C_LOOK
from utils.utils import display_results

algorithms = {
    "lru": lru.run,
    "arb": ARB.run,  # Additional Reference Bit
    "sstf": SSTF.run,
    "c-scan": C_SCAN.run,
    "optimal": optimal.run,
    "second chance": SC.run,
    "fifo": FIFO.run,
    "scan": SCAN.run,
    "look": LOOK.run,
    "c-look": C_LOOK.run,
}


def run_simulation(algorithm: str, data: list, param1: int, param2: int = None):
    algorithm = algorithm.lower()
    print("Selected Algorithm:", algorithm)
    if algorithm not in algorithms:
        raise ValueError(f"Unsupported algorithm '{algorithm}'")

    is_disk = algorithm in ["sstf", "c-scan", "look", "c-look", "scan"]
    print("Is Disk Algorithm:", is_disk)
    run_algorithm = algorithms[algorithm]

    results_dict = (
        run_algorithm(data, param1, param2)
        if is_disk
        else run_algorithm(data, param1)
    )

    # Extract values
    frame_states = results_dict.pop("frame_states", results_dict.pop("cylinders", []))
    logs = results_dict.pop("logs", [])
    faults = results_dict.pop("faults", results_dict.pop("seek_time", 0))
    others = results_dict

    display_results(frame_states, logs, faults, others, is_disk)

    # Return unified, explicitly structured output
    if is_disk:
        return {
            "seek_time": faults,
            "cylinders": frame_states
        }
    else:
        return {
            "frame_states": frame_states,
            "logs": logs,
            "faults": faults,
            "is_disk": False
        }