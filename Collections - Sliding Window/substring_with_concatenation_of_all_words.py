import collections
from typing import List

"""
Input: s = "barfoothefoobarman", words = ["foo","bar"]
Output: [0,9]
"""


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if len(s) == 0 or len(words) == 0:
            return []

        match_indices = []

        pattern_counter = collections.Counter()
        for word in words:
            pattern_counter[word] += 1

        word_len = len(words[0])

        # window state variables
        for start_idx in range(word_len):
            window_counter = collections.Counter()
            effective_count = 0
            end_idx = start_idx

            while end_idx < len(s):
                end_word = s[end_idx:(end_idx + word_len)]
                window_counter[end_word] += 1
                if window_counter[end_word] <= pattern_counter[end_word]:
                    effective_count += 1

                # shrink window until it meets requirement
                while start_idx < len(s) and window_counter[s[start_idx:(start_idx + word_len)]] > pattern_counter[s[start_idx:(start_idx + word_len)]]:
                    start_word = s[start_idx:(start_idx + word_len)]
                    window_counter[start_word] -= 1
                    start_idx += word_len

                # and meets requirement
                if effective_count == len(words) and end_idx - start_idx + word_len == word_len * len(words):
                    match_indices.append(start_idx)

                end_idx += word_len

        return match_indices


print(Solution().findSubstring(
    "wordgoodgoodgoodbestword", ["word", "good", "best", "word"]))
