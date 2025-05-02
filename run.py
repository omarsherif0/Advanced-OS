from algorithms import SC, lru, C_SCAN, SSTF, optimal
from utils.utils import display_results

algorithms = {
    "lru": lru.run,
    "arb": "arb.run",  # Additional Reference Bit (you’ll want to implement the actual function)
    "sstf": SSTF.run,
    "c-scan": C_SCAN.run,
    "optimal": optimal.run,
    "second chance": SC.run,
}

def run_simulation(algorithm: str, data: list, param1: int, param2: int = None):
    algorithm = algorithm.lower()
    
    if algorithm not in algorithms:
        raise ValueError(f"Unsupported algorithm '{algorithm}'")

    is_disk = algorithm in ["sstf", "c-scan"]

    run_algorithm = algorithms[algorithm]

    if is_disk:
        results_dict = run_algorithm(data, param1, param2)
    else:
        results_dict = run_algorithm(data, param1)

    frame_states = results_dict.pop("frame_states", [])
    logs = results_dict.pop("logs", [])
    faults = results_dict.pop("faults", 0)
    others = results_dict

    display_results(frame_states, logs, faults, others, is_disk)
    return {
        "cylinders": frame_states,
        #"logs": logs,
        "seek_time": faults,
        # "others": others,
        # "is_disk": is_disk,
    }
