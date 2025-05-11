from algorithms import SC, lru, C_SCAN, SSTF, optimal, FIFO, SCAN, LOOK, C_LOOK, ARB
from utils.utils import display_results, parse_reference_string

algorithms = {
    "lru": lru.run,
    "arb": ARB.run,
    "sstf": SSTF.run,
    "c_scan": C_SCAN.run,
    "optimal": optimal.run,
    "second chance": SC.run,
    "fifo": FIFO.run,
    "scan": SCAN.run,
    "look": LOOK.run,
    "c-look": C_LOOK.run,
}


def get_user_input():
    print("\nAvailable Algorithms:")
    for name in algorithms:
        print(f"- {name}")

    while True:
        algorithm_choice = input("Choose an algorithm: ").lower()
        if algorithm_choice in algorithms:
            break
        else:
            print("Invalid choice. Please select from the available options.")

    is_disk_algorithm = algorithm_choice in ["sstf", "c_scan", "look", "c-look", "scan"]

    if is_disk_algorithm:
        requests = list(
            map(
                int,
                input("Enter the disk cylinder requests (space-separated): ")
                .strip()
                .split(),
            )
        )
        initial_head = int(input("Enter the initial head position: "))
        max_cylinder = int(input("Enter the maximum cylinder number: "))
        return algorithm_choice, requests, initial_head, max_cylinder, True
    else:
        reference_string = list(
            map(
                int,
                input("Enter the reference string (space-separated): ").strip().split(),
            )
        )
        num_frames = int(input("Enter the number of available frames: "))
        return algorithm_choice, reference_string, num_frames, None, False


def main():
    algorithm, data, param1, param2, is_disk = get_user_input()
    run_algorithm = algorithms[algorithm]

    results_dict = (
        run_algorithm(data, param1, param2) if is_disk else run_algorithm(data, param1)
    )

    frame_states = results_dict.pop("frame_states", [])
    logs = results_dict.pop("logs", [])
    faults = results_dict.pop("faults", 0)
    others = results_dict

    display_results(frame_states, logs, faults, others, is_disk)


if __name__ == "__main__":
    main()
