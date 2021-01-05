from typing import List


class Event:
    def __init__(self, time):
        self.time = time


class BusyEvent(Event):
    pass


class FreeEvent(Event):
    pass


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        events = []
        for interval in intervals:
            events.append(BusyEvent(interval[0]))
            events.append(FreeEvent(interval[1]))

        events.sort(key=lambda event: (
            event.time, (-1 if isinstance(event, FreeEvent) else 1)))

        busy_count = 0
        max_busy_count = 0

        for event in events:
            if isinstance(event, BusyEvent):
                busy_count += 1
            else:
                busy_count -= 1

            max_busy_count = max(busy_count, max_busy_count)

        return max_busy_count
