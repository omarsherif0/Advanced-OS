from collections import deque

def run(reference_string: str, frames_num: int) -> list: 
    frames = deque(maxlen=frames_num)
    page_fault = 0
    steps = []
    frame_state = []

    for i, page in enumerate(reference_string):
        if page in frames:
            steps.append(f"Step number {i} page {page} hit.")
        if page not in frames:
            page_fault += 1
            if len(frames) == frames_num:
                removed = frames.popleft()
                steps.append(f"Step number {i} replaced page {removed} with page {page}.")
            else:
                steps.append(f"Step number {i} page {page} were added.")
            frames.append(page)
        else:
            frames.remove(page)
            frames.append(page)
            steps.append(f"Step number {i} page {page} were used.")
        frame_state.append(list(frames))
    return [frame_state, steps, page_fault]