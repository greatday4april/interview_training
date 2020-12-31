# https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/

"""
Given a string s and an integer k, return the length of the longest substring of s that contains at most k distinct characters.

Example 1:

Input: s = "eceba", k = 2
Output: 3
Explanation: The substring is "ece" with length 3.
"""

import collections


class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        if len(s) == 0:
            return 0

        longest_length = 0  # the global state

        # window state variables
        start_idx = 0
        window_counter = collections.Counter()

        for end_idx in range(len(s)):
            char = s[end_idx]
            window_counter[char] += 1

            # shrink window until it meets requirement
            while len(window_counter) > k:
                start_char = s[start_idx]
                window_counter[start_char] -= 1
                if window_counter[start_char] == 0:
                    window_counter.pop(start_char)
                start_idx += 1

            if end_idx - start_idx + 1 > longest_length:  # and meets requirement
                longest_length = end_idx - start_idx + 1

        return longest_length
