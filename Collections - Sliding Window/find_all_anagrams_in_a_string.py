# https://leetcode.com/problems/find-all-anagrams-in-a-string/

# substr 是 p 的anagram => substr对应的hash 和 p 的hash完全相同
import collections


class Solution:
    def findAnagrams(self, s: str, pattern: str) -> List[int]:
        if len(s) == 0:
            return ''

        match_indices = []  # the global state
        pattern_counter = collections.Counter()
        for char in pattern:
            pattern_counter[char] += 1

        # window state variables
        start_idx = 0
        window_counter = collections.Counter()

        for end_idx in range(len(s)):
            char = s[end_idx]
            window_counter[char] += 1

            # shrink window until it meets requirement
            while start_idx < len(s) and window_counter[s[start_idx]] > pattern_counter[s[start_idx]]:
                window_counter[s[start_idx]] -= 1
                if window_counter[s[start_idx]] == 0:
                    window_counter.pop(s[start_idx])
                start_idx += 1

            # and meets requirement
            if window_counter == pattern_counter:
                match_indices.append(start_idx)

        return match_indices
