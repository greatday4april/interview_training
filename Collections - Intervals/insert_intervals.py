from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        window = newInterval
        left = []
        right = []

        for interval in intervals:
            if window[0] > interval[1]:
                left.append(interval)
            elif window[1] < interval[0]:
                right.append(interval)
            else:
                window[0] = min(window[0], interval[0])
                window[1] = max(window[1], interval[1])

        return left + [window] + right
