import collections


def slide_window(str):
    if len(str) == 0:
        return ''

    longest = ''  # the global state

    # window state variables
    start_idx = 0
    window_counter = collections.Counter()

    for end_idx in range(len(str)):
        char = str[end_idx]
        window_counter[char] += 1

        # shrink window until it meets requirement
        while len(window_counter) > k:
            start_char = str[start_idx]
            window_counter[start_char] -= 1
            if window_counter[start_char] == 0:
                window_counter.pop(start_char)
            start_idx += 1

        if end_idx - start_idx + 1 > len(longest):  # and meets requirement
            longest = str[start_idx:(end_idx + 1)]

    return longest
