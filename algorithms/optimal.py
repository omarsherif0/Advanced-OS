def run(reference_string: str, frames_num: int) -> list:
    frames = []
    page_faults = 0
    steps = []
    frame_states = []

    for i, page in enumerate(reference_string):
        if page in frames:
            steps.append(f"Step {i}: Page {page} hit.")
        else:
            page_faults += 1
            if len(frames) < frames_num:
                frames.append(page)
                steps.append(f"Step {i}: Page {page} added (no replacement).")
            else:
                future_uses = []
                for f in frames:
                    try:
                        next_use = reference_string[i+1:].index(f)
                    except ValueError:
                        next_use = float('inf')  # Never used again
                    future_uses.append(next_use)

                index_to_replace = future_uses.index(max(future_uses))
                removed = frames[index_to_replace]
                frames[index_to_replace] = page
                steps.append(f"Step {i}: Page {removed} replaced with {page}.")

        frame_states.append(frames.copy())

    return [frame_states, steps, page_faults]
