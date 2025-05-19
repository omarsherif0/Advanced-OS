def run(referenceString: list, framesNum: int) -> dict:
    framesInMemory = [None for _ in range(framesNum)]
    refBits = ["00000000" for _ in range(framesNum)]
    steps = []
    pageFaults = 0
    refBitsHistory = []
    frameState = []

    # Logic
    for step, page in enumerate(referenceString):
        # 1. Shift all reference bits to the right
        for i in range(framesNum):
            refBits[i] = "0" + refBits[i][:-1]  # Shift right, MSB = 0 by default

        # 2. Page Hit
        if page in framesInMemory:
            pos = framesInMemory.index(page)
            refBits[pos] = "1" + refBits[pos][1:]  # Set MSB = 1
            steps.append(f"Step {step}: Page {page} hit.")
        else:
            # 3. Page Fault
            pageFaults += 1
            steps.append(f"Step {step}: Page {page} fault.")

            # 3.a. Insert if empty frame exists
            if None in framesInMemory:
                pos = framesInMemory.index(None)
                framesInMemory[pos] = page
                refBits[pos] = "10000000"  # MSB = 1
                steps.append(f"Step {step}: Inserted page {page} at empty frame {pos}.")
            else:
                # 3.b. Replace page with lowest reference value
                replaceIdx = min(range(framesNum), key=lambda i: int(refBits[i], 2))
                replacedPage = framesInMemory[replaceIdx]
                framesInMemory[replaceIdx] = page
                refBits[replaceIdx] = "10000000"  # New page, MSB = 1
                steps.append(
                    f"Step {step}: Replaced page {replacedPage} with page {page} at frame {replaceIdx}."
                )

        # Track each step
        frameState.append(framesInMemory.copy())
        refBitsHistory.append(
            [f"{pg}: {bits}" for pg, bits in zip(framesInMemory, refBits)]
        )

    # Output
    return {
        "frame_states": frameState,
        "logs": steps,
        "faults": pageFaults,
        "ref_bits": refBitsHistory,
    }
