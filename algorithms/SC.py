def run(reference_string: list, frames_num: int) -> dict:
    frames = [None] * frames_num
    reference_bits = [0] * frames_num
    pointer = 0  
    page_faults = 0
    steps = []
    frame_states = []
    ref_bits_history = []
    hand_logs = []

    for step, page in enumerate(reference_string):
        if page in frames:
            idx = frames.index(page)
            reference_bits[idx] = 1
            steps.append(f"Step {step}: Page {page} hit.")
        else:
            page_faults += 1
            steps.append(f"Step {step}: Page {page} fault.")

            while True:
                if reference_bits[pointer] == 0:
                    replaced = frames[pointer]
                    frames[pointer] = page
                    reference_bits[pointer] = 1
                    if replaced is not None:
                        steps.append(f"Step {step}: Replaced page {replaced} with {page} at frame {pointer}.")
                    else:
                        steps.append(f"Step {step}: Inserted page {page} at frame {pointer}.")

                    pointer_message = (
                        f"🔄 The pointer went back to 0" if pointer + 1 == frames_num else
                        f"🕘 The pointer moved to frame {(pointer + 1) % frames_num}"
                    )
                    hand_logs.append(pointer_message)
                    pointer = (pointer + 1) % frames_num

                    break
                else:
                    reference_bits[pointer] = 0
                    pointer = (pointer + 1) % frames_num

        frame_states.append(frames.copy())
        ref_bits_history.append(reference_bits.copy())

    return {
        "frame_states": frame_states,
        "logs": steps,
        "faults": page_faults,
        "ref_bits": ref_bits_history,
        "clock_hand": hand_logs

    }
