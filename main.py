from algorithms import lru
from utils.utils import display_results, parse_reference_string

algorithms = {
    "LRU": lru.run,
    "FIFO": "fifo.run",
    "OPTIMAL": "optimal.run",
    "ARB": "additional_bit.run" 
}

def get_user_input():
    reference_string = input("Enter the reference string (space-separated): ")
    reference_list = list(map(int, reference_string.strip().split()))
    
    while True:
        try:
            num_frames = int(input("Enter the number of available frames: "))
            if num_frames <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer for frames.")
    
    print("\nAvailable Algorithms:")
    for name in algorithms:
        print(f"- {name}")
    
    while True:
        algorithm_choice = input("Choose an algorithm: ").strip().upper()
        if algorithm_choice in algorithms:
            break
        else:
            print("Invalid choice. Please select from the available options.")
    
    return reference_list, num_frames, algorithm_choice

def main():
    reference_string, num_frames, algorithm = get_user_input()
    run_algorithm = algorithms[algorithm]
    frame_states, logs, faults = run_algorithm(reference_string, num_frames)
    display_results(frame_states, logs, faults)

if __name__ == "__main__":
    main()
