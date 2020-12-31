import typing
from collections import Counter


class Solution:
    def minWindow(self, s: str, pattern: str) -> str:
        if len(s) == 0:
            return ''

        shortest = None  # the global state

        pattern_counter = Counter()
        for char in pattern:
            pattern_counter[char] += 1

        # window state variables
        start_idx = 0
        window_counter = Counter()
        effective_count = 0

        for end_idx in range(len(s)):
            char = s[end_idx]
            window_counter[char] += 1
            if window_counter[char] <= pattern_counter[char]:
                effective_count += 1

            # shrink window until it meets requirement
            while start_idx < len(s) and window_counter[s[start_idx]] > pattern_counter[s[start_idx]]:
                start_char = s[start_idx]
                window_counter[start_char] -= 1
                if window_counter[start_char] == 0:
                    window_counter.pop(start_char)
                start_idx += 1

            if effective_count == len(pattern):  # and meets requirement
                if shortest is None or (end_idx - start_idx + 1) < len(shortest):
                    shortest = s[start_idx:(end_idx + 1)]

        return shortest if shortest is not None else ''
