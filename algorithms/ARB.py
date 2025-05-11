import json


def replaceFrame(inMemory, currentState, requiredFrame):
    Min = float("inf")
    replaceIdx = -1
    for idx, state in enumerate(currentState):
        if Min > int(state, 2):
            Min = int(state, 2)
            replaceIdx = idx
    message = f"Replaced page {inMemory[replaceIdx]} with page {requiredFrame} at frame {replaceIdx}"
    currentState[replaceIdx] = "10000000"
    inMemory[replaceIdx] = requiredFrame
    return inMemory, currentState, message, replaceIdx


def run(referenceString: list, framesNum: int) -> dict:
    countNotReferenced = [0 for _ in range(framesNum)]
    framesInMemory = [None for _ in range(framesNum)]
    frames = ["00000000" for _ in range(framesNum)]
    steps = []
    pageFaults = 0
    refBitsHistory = []
    frameState = []

    # Logic
    for step, page in enumerate(referenceString):
        ## Apply Aging for non-used Pages
        for i in range(framesNum):
            if framesInMemory[i] != page and framesInMemory[i] is not None:
                countNotReferenced[i] += 1
                if countNotReferenced[i] % 5 == 0:
                    frames[i] = "0" + frames[i][:-1]
            elif framesInMemory[i] == page:
                countNotReferenced[i] = 0

        ## The Main Logic
        if page in framesInMemory:
            steps.append(f"Step {step}: Page {page} hit.")
            pos = framesInMemory.index(page)
            frames[pos] = "1" + frames[pos][:-1]
            countNotReferenced[pos] = 0
        else:
            if None in framesInMemory:
                pos = framesInMemory.index(None)
                framesInMemory[pos] = page
                pageFaults += 1
                steps.append(f"Step {step}: Page {page} fault.")
                steps.append(
                    f"Step {step}: Inserted page {page} at the empty frame {pos}."
                )
                countNotReferenced[pos] = 0
                frames[pos] = "1" + frames[pos][:-1]
            else:
                pageFaults += 1
                steps.append(f"Step {step}: Page {page} fault.")
                replaceIdx = min(range(framesNum), key=lambda i: int(frames[i], 2))
                replacedPage = framesInMemory[replaceIdx]
                framesInMemory[replaceIdx] = page
                frames[replaceIdx] = "10000000"
                countNotReferenced[replaceIdx] = 0
                steps.append(
                    f"Step {step}: Replaced page {replacedPage} with page {page} at frame {replaceIdx}."
                )
        frameState.append(framesInMemory.copy())

        ## Frame State of Each Step
        logs = []
        logs = [f"{inMem}: {frame}" for inMem, frame in zip(framesInMemory, frames)]
        refBitsHistory.append(logs)

    # Output
    return {
        "frame_states": frameState,
        "logs": steps,
        "faults": pageFaults,
        "ref_bits": refBitsHistory,
    }
