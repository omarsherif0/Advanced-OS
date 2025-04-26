from algorithms import lru, C_SCAN, SSTF
from utils.utils import display_results, parse_reference_string

algorithms = {
    "lru": lru.run,
    "arb": "arb.run", # Additiona Reference Bit
    "sstf": SSTF.run,
    "c_scan": C_SCAN.run 
}

def get_user_input():
    print("\nAvailable Algorithms:")
    for name in algorithms:
        print(f"- {name}")

    while True:
        algorithm_choice = input("Choose an algorithm: ").strip().lower()
        if algorithm_choice in algorithms:
            break
        else:
            print("Invalid choice. Please select from the available options.")

    is_disk_algorithm = algorithm_choice in ["sstf", "c_scan"]

    if is_disk_algorithm:
        requests = list(map(int, input("Enter the disk cylinder requests (space-separated): ").strip().split()))
        initial_head = int(input("Enter the initial head position: "))
        max_cylinder = int(input("Enter the maximum cylinder number: "))
        return algorithm_choice, requests, initial_head, max_cylinder, True
    else:
        reference_string = list(map(int, input("Enter the reference string (space-separated): ").strip().split()))
        num_frames = int(input("Enter the number of available frames: "))
        return algorithm_choice, reference_string, num_frames, None, False

def main():
    algorithm, data, param1, param2, is_disk = get_user_input()
    run_algorithm = algorithms[algorithm]

    if is_disk:
        # SSTF, C-SCAN
        frame_states, logs, faults = run_algorithm(data, param1, param2)
    else:
        # LRU Additional reference bit
        frame_states, logs, faults = run_algorithm(data, param1)

    display_results(frame_states, logs, faults, is_disk)

if __name__ == "__main__":
    main()