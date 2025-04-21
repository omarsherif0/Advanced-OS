def parse_reference_string(input_str: str) -> list:
    """
    Parses a space-separated string of integers into a list.
    """
    try:
        return list(map(int, input_str.strip().split()))
    except ValueError:
        raise ValueError("Input must contain only space-separated integers.")

def display_results(frame_states, steps, page_faults):
    print("\n📊 Frame states after each step:")
    for i, state in enumerate(frame_states):
        print(f"Step {i+1}: {state}")

    print("\n🔁 Replacement log:")
    for step in steps:
        print(step)

    print(f"\n❌ Total Page Faults: {page_faults}")
