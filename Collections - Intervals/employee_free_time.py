class Solution:
    def employeeFreeTime(self, schedule: '[[Interval]]', start_time, end_time) -> '[Interval]':
        intervals = []
        for schedule_per_person in schedule:
            intervals += schedule_per_person

        intervals = sorted(intervals, key=lambda interval: interval.start)

        output = []
        # start_time = intervals[0].end
        for idx in range(1, len(intervals)):
            interval = intervals[idx]
            free_window_end_time = min(end_time, interval.start)
            if interval.start - start_time > 0:
                output.append(Interval(start_time, interval.start))

            start_time = max(start_time, interval.end)

        # output.append([start_time, end_time])
        return output
