def parse_reference_string(input_str: str) -> list:
    """
    Parses a space-separated string of integers into a list.
    """
    try:
        return list(map(int, input_str.strip().split()))
    except ValueError:
        raise ValueError("Input must contain only space-separated integers.")

def display_results(frame_states: list, steps: list, page_faults: int,  others: dict, flag: int) -> None:
    if flag:  # Disk scheduling
        print("\n📊 Order of reserved request:")
        for i, state in enumerate(frame_states):
            print(f"{state}")
        
        print(f"\n📏 Total Head Movements: {page_faults}")

    else:  # Memory (page replacement)
        print("\n📊 Frame states after each step:")
        for i, state in enumerate(frame_states):
            print(f"Step {i+1}: {state}")

        print("\n🔁 Replacement log:")
        for step in steps:
            print(step)

        print(f"\n❌ Total Page Faults: {page_faults}")

        # Optionally show reference bits or aging counters
        if "ref_bits" in others:
            print("\n🧠 Reference Bits History:")
            for i, bits in enumerate(others["ref_bits"]):
                print(f"Step {i+1}: {bits}")

        if "clock_hand" in others:
            print("\n🧭 Pointer Movements:")
            for i, log in enumerate(others["clock_hand"]):
                print(f"Step {i+1}: {log}")