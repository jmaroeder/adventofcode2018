import io
import re
from collections import defaultdict
from typing import Sequence, Tuple, Mapping, Iterable, NamedTuple, MutableMapping


class GuardData:
    def __init__(self, guard_id: int):
        self.guard_id = guard_id
        self.minutes_asleep = defaultdict(int)

    def log_nap(self, start: int, stop: int) -> None:
        for i in range(start, stop):
            self.minutes_asleep[i] += 1

    def total_minutes_asleep(self) -> int:
        return sum(self.minutes_asleep.values())

    @staticmethod
    def _sleepiest_minute_sort(item: Tuple[int, int]) -> int:
        minute, value = item
        return value

    def sleepiest_minute(self) -> int:
        return sorted(self.minutes_asleep.items(), key=self._sleepiest_minute_sort, reverse=True)[0][0]


def part1(x: str) -> int:
    """
    Computes the number of overlapping points
    """
    guards: MutableMapping[int, GuardData] = {}
    guard: GuardData = None
    fell_asleep_at: int = None
    for match in re.finditer(r'\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\]'
                             r' (?P<log>.*)', '\n'.join(sorted(x.splitlines()))):
        # print(match.groupdict())
        entry = match.groupdict()
        if entry['log'] == 'falls asleep':
            fell_asleep_at = int(entry['minute'])
        elif entry['log'] == 'wakes up':
            guard.log_nap(fell_asleep_at, int(entry['minute']))
        else:
            new_guard = re.match(r'Guard #(\d+) begins shift', entry['log'])
            guard_id = int(new_guard.group(1))
            guard = guards.setdefault(guard_id, GuardData(guard_id))
        # claim = Claim(**match.groupdict())
        # add_claim(claim, fabric)

    for guard_id, guard in guards.items():
        print(f'{guard_id}: {guard.total_minutes_asleep()}, {guard.sleepiest_minute()}')

    sleepiest_guard = max(guards.values(), key=lambda g: g.total_minutes_asleep())
    return sleepiest_guard.guard_id * sleepiest_guard.sleepiest_minute()


# def part2(x: str) -> Iterable[int]:
#     """
#     Returns the ID(s) of in-tact claims
#     """
#     fabric = {}
#     for match in re.finditer(r'#(?P<id>\d+)\s+@\s+(?P<x>\d+),(?P<y>\d+):\s+(?P<width>\d+)x(?P<height>\d+)', x):
#         claim = Claim(**match.groupdict())
#         add_claim(claim, fabric)
#     for match in re.finditer(r'#(?P<id>\d+)\s+@\s+(?P<x>\d+),(?P<y>\d+):\s+(?P<width>\d+)x(?P<height>\d+)', x):
#         claim = Claim(**match.groupdict())
#         if is_claim_intact(claim, fabric):
#             yield claim.id
#
#
puzzle_input = '''
[1518-10-31 00:58] wakes up
[1518-02-27 00:57] wakes up
[1518-04-05 00:03] falls asleep
[1518-06-03 00:18] falls asleep
[1518-08-06 00:39] falls asleep
[1518-08-15 00:54] falls asleep
[1518-03-07 00:00] falls asleep
[1518-05-01 00:12] falls asleep
[1518-06-17 00:53] wakes up
[1518-03-13 00:13] falls asleep
[1518-08-05 00:34] wakes up
[1518-11-23 00:57] wakes up
[1518-07-01 23:59] Guard #1301 begins shift
[1518-02-08 00:51] wakes up
[1518-11-10 00:59] wakes up
[1518-07-06 00:01] falls asleep
[1518-07-08 00:11] falls asleep
[1518-04-04 00:40] wakes up
[1518-04-26 00:04] wakes up
[1518-03-26 00:35] falls asleep
[1518-06-05 00:33] falls asleep
[1518-07-25 23:56] Guard #433 begins shift
[1518-10-20 00:33] wakes up
[1518-02-05 00:44] falls asleep
[1518-02-15 00:58] wakes up
[1518-03-20 00:51] wakes up
[1518-11-02 00:36] wakes up
[1518-03-05 23:46] Guard #401 begins shift
[1518-05-31 00:39] wakes up
[1518-09-11 00:09] falls asleep
[1518-04-15 00:39] wakes up
[1518-09-20 23:58] Guard #1877 begins shift
[1518-11-18 00:52] wakes up
[1518-02-11 00:18] wakes up
[1518-06-25 00:47] wakes up
[1518-08-24 00:56] wakes up
[1518-10-17 00:51] falls asleep
[1518-11-14 00:51] falls asleep
[1518-04-24 00:24] falls asleep
[1518-11-18 00:41] wakes up
[1518-04-12 23:58] Guard #3191 begins shift
[1518-07-14 23:59] Guard #3469 begins shift
[1518-10-28 00:31] falls asleep
[1518-04-15 00:35] falls asleep
[1518-02-22 00:57] wakes up
[1518-08-04 00:35] falls asleep
[1518-03-21 00:56] wakes up
[1518-11-19 23:54] Guard #3271 begins shift
[1518-07-27 00:55] falls asleep
[1518-10-27 00:38] wakes up
[1518-03-08 00:02] Guard #619 begins shift
[1518-06-01 00:25] falls asleep
[1518-05-08 00:18] wakes up
[1518-07-09 00:42] falls asleep
[1518-03-12 00:46] wakes up
[1518-08-15 00:51] wakes up
[1518-02-14 00:35] falls asleep
[1518-02-12 00:38] falls asleep
[1518-05-23 00:04] Guard #401 begins shift
[1518-10-02 00:54] wakes up
[1518-11-20 00:44] falls asleep
[1518-04-28 00:33] falls asleep
[1518-09-30 00:32] falls asleep
[1518-06-15 00:06] falls asleep
[1518-10-05 00:57] wakes up
[1518-05-02 00:58] wakes up
[1518-02-27 00:20] falls asleep
[1518-05-27 00:04] falls asleep
[1518-03-04 00:02] falls asleep
[1518-02-22 00:14] falls asleep
[1518-06-19 23:57] Guard #509 begins shift
[1518-08-10 00:54] wakes up
[1518-09-25 00:34] wakes up
[1518-08-12 00:16] falls asleep
[1518-05-18 00:56] falls asleep
[1518-09-08 00:47] falls asleep
[1518-02-08 00:03] Guard #1327 begins shift
[1518-03-16 00:31] falls asleep
[1518-07-02 00:48] wakes up
[1518-11-16 23:48] Guard #2861 begins shift
[1518-07-03 00:19] falls asleep
[1518-08-10 00:00] Guard #2207 begins shift
[1518-07-30 00:48] wakes up
[1518-06-29 23:59] Guard #1409 begins shift
[1518-10-16 00:39] wakes up
[1518-08-30 23:57] Guard #1877 begins shift
[1518-03-05 00:46] wakes up
[1518-02-02 00:10] falls asleep
[1518-08-18 00:47] falls asleep
[1518-03-25 00:23] wakes up
[1518-08-04 00:37] wakes up
[1518-09-03 23:57] Guard #2417 begins shift
[1518-03-12 00:49] falls asleep
[1518-10-25 23:52] Guard #73 begins shift
[1518-08-16 00:40] falls asleep
[1518-04-03 00:46] wakes up
[1518-06-22 00:02] Guard #619 begins shift
[1518-10-20 23:57] Guard #3499 begins shift
[1518-07-19 00:55] wakes up
[1518-11-14 00:04] Guard #2663 begins shift
[1518-02-15 00:46] falls asleep
[1518-01-31 00:00] Guard #1301 begins shift
[1518-06-27 00:48] wakes up
[1518-02-27 00:32] wakes up
[1518-05-05 00:05] falls asleep
[1518-02-28 00:56] wakes up
[1518-10-10 00:39] wakes up
[1518-04-17 00:22] falls asleep
[1518-05-09 00:07] falls asleep
[1518-02-21 00:16] falls asleep
[1518-07-12 00:17] falls asleep
[1518-11-01 00:45] wakes up
[1518-07-03 00:02] Guard #73 begins shift
[1518-08-01 00:58] wakes up
[1518-07-08 00:36] wakes up
[1518-05-28 00:44] wakes up
[1518-08-05 00:10] falls asleep
[1518-09-03 00:51] wakes up
[1518-05-17 00:55] wakes up
[1518-07-29 23:59] Guard #3469 begins shift
[1518-10-22 00:49] wakes up
[1518-02-17 00:13] falls asleep
[1518-11-15 00:11] falls asleep
[1518-04-21 00:52] wakes up
[1518-05-03 00:51] wakes up
[1518-04-23 00:58] wakes up
[1518-09-27 00:35] wakes up
[1518-06-08 00:04] Guard #2207 begins shift
[1518-02-03 00:22] falls asleep
[1518-08-08 00:55] wakes up
[1518-06-04 00:58] wakes up
[1518-08-30 00:29] wakes up
[1518-06-02 00:04] Guard #1301 begins shift
[1518-07-23 00:26] falls asleep
[1518-02-25 00:49] wakes up
[1518-05-15 23:56] Guard #3499 begins shift
[1518-10-14 23:59] Guard #3541 begins shift
[1518-03-19 23:59] Guard #2459 begins shift
[1518-07-26 00:58] wakes up
[1518-05-11 00:26] wakes up
[1518-03-11 00:30] wakes up
[1518-08-11 23:56] Guard #2411 begins shift
[1518-07-10 00:11] wakes up
[1518-08-30 00:35] falls asleep
[1518-04-11 00:05] falls asleep
[1518-04-03 23:59] Guard #619 begins shift
[1518-10-26 00:35] falls asleep
[1518-07-07 00:02] Guard #1877 begins shift
[1518-07-11 00:28] falls asleep
[1518-09-28 00:09] falls asleep
[1518-07-17 00:00] Guard #1409 begins shift
[1518-11-12 00:58] wakes up
[1518-09-12 00:27] wakes up
[1518-02-04 00:58] wakes up
[1518-02-14 00:48] wakes up
[1518-08-25 23:57] Guard #73 begins shift
[1518-09-29 00:01] falls asleep
[1518-10-20 00:23] falls asleep
[1518-05-23 00:37] wakes up
[1518-08-15 00:12] falls asleep
[1518-09-12 00:56] falls asleep
[1518-10-15 00:27] falls asleep
[1518-04-06 23:58] Guard #433 begins shift
[1518-10-05 00:00] falls asleep
[1518-07-21 00:50] falls asleep
[1518-03-15 00:33] wakes up
[1518-10-26 00:25] wakes up
[1518-06-12 00:47] wakes up
[1518-08-27 00:50] wakes up
[1518-03-08 00:22] falls asleep
[1518-04-02 00:48] wakes up
[1518-02-06 00:59] wakes up
[1518-10-19 23:56] Guard #433 begins shift
[1518-05-26 00:21] falls asleep
[1518-04-30 00:01] Guard #3499 begins shift
[1518-04-25 00:00] Guard #1877 begins shift
[1518-03-29 23:52] Guard #401 begins shift
[1518-04-08 00:26] falls asleep
[1518-03-24 00:16] wakes up
[1518-10-27 00:22] falls asleep
[1518-04-02 00:10] falls asleep
[1518-09-23 00:46] wakes up
[1518-02-13 00:55] wakes up
[1518-09-15 00:44] falls asleep
[1518-03-03 00:06] falls asleep
[1518-03-06 00:02] falls asleep
[1518-05-06 00:51] wakes up
[1518-05-24 00:23] falls asleep
[1518-09-10 00:33] falls asleep
[1518-09-20 00:23] falls asleep
[1518-03-26 00:54] wakes up
[1518-05-02 00:48] wakes up
[1518-08-10 00:33] wakes up
[1518-10-09 00:12] falls asleep
[1518-09-16 00:51] wakes up
[1518-10-19 00:09] falls asleep
[1518-04-29 00:02] falls asleep
[1518-07-29 00:13] wakes up
[1518-08-28 00:16] falls asleep
[1518-02-06 00:54] falls asleep
[1518-10-19 00:54] falls asleep
[1518-11-09 23:59] Guard #73 begins shift
[1518-03-16 00:35] wakes up
[1518-11-16 00:41] wakes up
[1518-03-18 23:57] Guard #1301 begins shift
[1518-10-12 00:52] falls asleep
[1518-09-18 00:03] Guard #3469 begins shift
[1518-09-25 00:59] wakes up
[1518-09-19 00:02] Guard #3499 begins shift
[1518-11-12 00:50] falls asleep
[1518-02-27 23:59] Guard #2861 begins shift
[1518-09-12 00:57] wakes up
[1518-02-18 23:59] Guard #2663 begins shift
[1518-01-29 23:57] Guard #2417 begins shift
[1518-03-30 00:05] falls asleep
[1518-02-16 23:59] Guard #1327 begins shift
[1518-04-28 00:59] wakes up
[1518-05-11 00:54] wakes up
[1518-04-19 23:47] Guard #619 begins shift
[1518-09-01 00:51] falls asleep
[1518-05-21 23:58] Guard #509 begins shift
[1518-09-14 00:58] wakes up
[1518-04-26 00:00] falls asleep
[1518-04-07 00:57] wakes up
[1518-06-04 00:48] falls asleep
[1518-11-21 00:40] wakes up
[1518-11-15 00:59] wakes up
[1518-11-09 00:23] falls asleep
[1518-10-20 00:57] wakes up
[1518-05-02 00:04] Guard #1409 begins shift
[1518-11-19 00:45] wakes up
[1518-09-16 00:42] falls asleep
[1518-07-06 00:48] falls asleep
[1518-07-15 00:24] falls asleep
[1518-07-21 00:01] Guard #2411 begins shift
[1518-05-30 23:56] Guard #2861 begins shift
[1518-10-24 00:19] falls asleep
[1518-02-17 00:57] falls asleep
[1518-05-21 00:10] falls asleep
[1518-09-19 00:53] wakes up
[1518-02-19 00:55] wakes up
[1518-10-16 00:44] falls asleep
[1518-03-18 00:03] Guard #1409 begins shift
[1518-07-28 00:03] Guard #3499 begins shift
[1518-09-05 00:56] wakes up
[1518-07-24 00:32] falls asleep
[1518-02-16 00:26] wakes up
[1518-09-28 00:03] Guard #1409 begins shift
[1518-06-24 23:49] Guard #3271 begins shift
[1518-11-16 00:58] wakes up
[1518-04-01 00:59] wakes up
[1518-02-16 00:04] Guard #2459 begins shift
[1518-02-13 00:10] falls asleep
[1518-07-13 00:39] wakes up
[1518-09-06 23:58] Guard #3499 begins shift
[1518-07-08 00:04] Guard #3541 begins shift
[1518-05-18 00:59] wakes up
[1518-10-01 00:01] Guard #2207 begins shift
[1518-02-24 00:19] falls asleep
[1518-04-24 00:43] wakes up
[1518-02-01 00:42] falls asleep
[1518-03-24 00:30] wakes up
[1518-06-09 00:16] falls asleep
[1518-06-02 00:27] falls asleep
[1518-08-28 00:04] Guard #1301 begins shift
[1518-07-27 00:04] falls asleep
[1518-10-26 00:36] wakes up
[1518-02-09 00:50] wakes up
[1518-05-30 00:48] falls asleep
[1518-08-22 00:43] wakes up
[1518-08-02 00:40] wakes up
[1518-02-10 23:47] Guard #3541 begins shift
[1518-04-28 23:48] Guard #2663 begins shift
[1518-10-17 00:13] falls asleep
[1518-06-20 00:16] falls asleep
[1518-02-21 00:26] wakes up
[1518-07-05 23:51] Guard #1327 begins shift
[1518-11-23 00:00] Guard #3271 begins shift
[1518-03-05 00:03] Guard #401 begins shift
[1518-06-07 00:41] falls asleep
[1518-11-08 23:56] Guard #1831 begins shift
[1518-02-21 00:56] wakes up
[1518-03-25 00:52] wakes up
[1518-06-26 00:57] wakes up
[1518-03-02 00:56] falls asleep
[1518-10-07 00:53] falls asleep
[1518-07-12 00:08] wakes up
[1518-09-04 00:34] falls asleep
[1518-03-16 00:53] wakes up
[1518-05-18 00:38] falls asleep
[1518-06-10 00:51] wakes up
[1518-05-08 00:00] Guard #2411 begins shift
[1518-03-16 23:58] Guard #1409 begins shift
[1518-10-31 00:01] Guard #3499 begins shift
[1518-11-11 00:39] falls asleep
[1518-06-14 00:04] falls asleep
[1518-06-10 23:59] Guard #433 begins shift
[1518-02-26 00:08] falls asleep
[1518-09-09 00:02] falls asleep
[1518-08-29 00:34] falls asleep
[1518-08-13 00:33] wakes up
[1518-11-15 00:38] wakes up
[1518-01-30 00:50] wakes up
[1518-10-11 00:50] wakes up
[1518-03-02 00:58] wakes up
[1518-06-12 00:50] falls asleep
[1518-10-14 00:32] wakes up
[1518-09-03 00:48] falls asleep
[1518-11-07 00:26] falls asleep
[1518-04-30 00:31] wakes up
[1518-05-24 00:57] falls asleep
[1518-07-10 00:00] Guard #2861 begins shift
[1518-05-08 00:59] wakes up
[1518-04-08 00:45] falls asleep
[1518-02-21 23:57] Guard #1409 begins shift
[1518-04-01 00:09] falls asleep
[1518-04-11 23:59] Guard #1697 begins shift
[1518-06-01 00:03] Guard #2417 begins shift
[1518-06-18 23:57] Guard #2411 begins shift
[1518-09-10 00:58] wakes up
[1518-02-23 00:19] wakes up
[1518-09-22 00:27] wakes up
[1518-06-30 00:57] wakes up
[1518-10-29 00:28] falls asleep
[1518-11-05 00:39] wakes up
[1518-06-29 00:11] wakes up
[1518-11-05 00:47] wakes up
[1518-07-26 23:50] Guard #3541 begins shift
[1518-04-08 00:00] Guard #2663 begins shift
[1518-07-04 00:54] falls asleep
[1518-05-27 00:12] wakes up
[1518-10-19 00:00] Guard #1877 begins shift
[1518-02-25 00:42] wakes up
[1518-04-16 00:59] wakes up
[1518-07-25 00:01] Guard #509 begins shift
[1518-07-19 00:19] wakes up
[1518-05-16 00:36] falls asleep
[1518-08-04 00:18] falls asleep
[1518-06-02 00:54] wakes up
[1518-08-24 23:52] Guard #2663 begins shift
[1518-07-08 23:57] Guard #619 begins shift
[1518-10-07 00:57] wakes up
[1518-04-10 23:49] Guard #73 begins shift
[1518-09-22 00:24] falls asleep
[1518-10-30 00:14] falls asleep
[1518-11-05 23:58] Guard #3499 begins shift
[1518-03-22 00:02] Guard #619 begins shift
[1518-05-31 00:32] falls asleep
[1518-05-30 00:20] falls asleep
[1518-10-04 23:49] Guard #3271 begins shift
[1518-10-13 00:54] wakes up
[1518-03-07 00:43] wakes up
[1518-08-11 00:51] wakes up
[1518-08-04 00:41] falls asleep
[1518-11-21 00:38] falls asleep
[1518-03-28 00:43] falls asleep
[1518-03-15 00:18] falls asleep
[1518-03-08 00:30] falls asleep
[1518-09-06 00:46] wakes up
[1518-02-04 00:03] Guard #2207 begins shift
[1518-02-26 00:04] Guard #619 begins shift
[1518-05-15 00:10] falls asleep
[1518-11-06 00:59] wakes up
[1518-04-23 00:57] falls asleep
[1518-04-14 00:38] wakes up
[1518-07-22 00:35] falls asleep
[1518-09-03 00:25] falls asleep
[1518-10-07 00:18] falls asleep
[1518-02-24 00:50] wakes up
[1518-11-15 00:56] falls asleep
[1518-06-15 00:44] falls asleep
[1518-07-20 00:55] wakes up
[1518-02-12 00:35] wakes up
[1518-03-22 00:20] falls asleep
[1518-04-09 00:04] Guard #1697 begins shift
[1518-05-15 00:04] Guard #1301 begins shift
[1518-09-22 00:02] Guard #2663 begins shift
[1518-08-29 00:59] wakes up
[1518-04-01 23:58] Guard #1877 begins shift
[1518-03-20 00:23] falls asleep
[1518-08-07 00:54] wakes up
[1518-10-21 00:33] falls asleep
[1518-09-07 00:36] wakes up
[1518-04-26 00:14] falls asleep
[1518-08-10 00:42] falls asleep
[1518-09-22 00:17] wakes up
[1518-02-12 00:01] Guard #1831 begins shift
[1518-09-04 00:58] wakes up
[1518-11-20 00:07] wakes up
[1518-02-08 00:07] falls asleep
[1518-10-20 00:53] falls asleep
[1518-02-03 00:56] wakes up
[1518-08-30 00:58] wakes up
[1518-06-06 00:25] falls asleep
[1518-05-13 00:40] falls asleep
[1518-11-18 00:37] falls asleep
[1518-04-18 00:31] falls asleep
[1518-01-30 00:13] falls asleep
[1518-07-01 00:37] falls asleep
[1518-03-11 00:49] wakes up
[1518-04-04 00:50] falls asleep
[1518-08-24 00:04] falls asleep
[1518-04-04 23:54] Guard #2663 begins shift
[1518-08-23 00:56] wakes up
[1518-09-14 00:25] falls asleep
[1518-03-30 00:55] wakes up
[1518-07-22 23:56] Guard #2459 begins shift
[1518-09-13 23:58] Guard #1877 begins shift
[1518-02-14 00:57] wakes up
[1518-08-28 00:42] wakes up
[1518-06-13 00:01] falls asleep
[1518-04-28 00:01] Guard #3541 begins shift
[1518-01-31 00:54] wakes up
[1518-07-14 00:46] wakes up
[1518-09-25 00:39] falls asleep
[1518-04-22 00:47] falls asleep
[1518-08-31 00:48] falls asleep
[1518-07-21 00:54] wakes up
[1518-04-21 00:12] falls asleep
[1518-05-16 00:31] wakes up
[1518-09-12 00:22] falls asleep
[1518-11-17 00:49] wakes up
[1518-05-24 00:28] wakes up
[1518-07-13 00:36] falls asleep
[1518-02-21 00:55] falls asleep
[1518-06-11 00:19] falls asleep
[1518-08-25 00:48] wakes up
[1518-09-27 00:45] wakes up
[1518-10-29 00:55] falls asleep
[1518-05-07 00:02] Guard #73 begins shift
[1518-03-14 23:59] Guard #2861 begins shift
[1518-07-10 00:10] falls asleep
[1518-03-09 00:00] Guard #1831 begins shift
[1518-06-21 00:31] falls asleep
[1518-11-10 00:48] falls asleep
[1518-07-26 00:35] falls asleep
[1518-09-21 00:57] wakes up
[1518-06-12 23:54] Guard #73 begins shift
[1518-07-30 00:56] wakes up
[1518-03-18 00:19] falls asleep
[1518-09-24 00:46] wakes up
[1518-10-12 00:29] wakes up
[1518-04-22 00:53] wakes up
[1518-05-09 23:49] Guard #3541 begins shift
[1518-08-20 00:59] wakes up
[1518-07-14 00:54] falls asleep
[1518-10-16 00:02] Guard #3499 begins shift
[1518-08-16 00:30] wakes up
[1518-06-23 00:32] falls asleep
[1518-08-03 00:02] Guard #3191 begins shift
[1518-07-11 23:47] Guard #3469 begins shift
[1518-02-02 00:03] Guard #2207 begins shift
[1518-02-23 00:00] Guard #2207 begins shift
[1518-03-27 23:56] Guard #2459 begins shift
[1518-03-14 00:06] falls asleep
[1518-03-02 00:00] Guard #2207 begins shift
[1518-05-10 00:59] wakes up
[1518-11-19 00:16] falls asleep
[1518-04-26 00:46] falls asleep
[1518-11-06 00:27] falls asleep
[1518-05-26 00:03] Guard #2411 begins shift
[1518-04-25 00:49] wakes up
[1518-05-02 00:33] falls asleep
[1518-06-24 00:28] falls asleep
[1518-10-28 23:58] Guard #433 begins shift
[1518-10-10 00:04] Guard #1301 begins shift
[1518-06-23 00:10] falls asleep
[1518-05-11 00:52] falls asleep
[1518-05-19 00:40] wakes up
[1518-09-19 00:35] falls asleep
[1518-08-22 00:59] wakes up
[1518-10-30 00:03] Guard #1877 begins shift
[1518-06-18 00:02] falls asleep
[1518-09-03 00:42] wakes up
[1518-06-11 00:31] falls asleep
[1518-10-28 00:52] wakes up
[1518-08-30 00:04] falls asleep
[1518-07-04 00:59] wakes up
[1518-10-03 00:58] wakes up
[1518-02-02 00:49] wakes up
[1518-04-18 00:01] Guard #401 begins shift
[1518-10-07 00:00] Guard #1831 begins shift
[1518-08-23 23:49] Guard #2207 begins shift
[1518-03-21 00:04] Guard #1831 begins shift
[1518-06-12 00:59] wakes up
[1518-02-13 00:02] Guard #1301 begins shift
[1518-05-11 00:16] falls asleep
[1518-08-19 00:00] Guard #2417 begins shift
[1518-06-05 00:45] wakes up
[1518-03-01 00:26] falls asleep
[1518-05-02 00:52] falls asleep
[1518-10-27 23:57] Guard #2663 begins shift
[1518-09-05 00:06] falls asleep
[1518-06-03 00:01] Guard #3469 begins shift
[1518-02-19 00:52] falls asleep
[1518-11-05 00:12] falls asleep
[1518-10-01 00:32] falls asleep
[1518-08-06 00:55] wakes up
[1518-07-20 00:03] Guard #433 begins shift
[1518-07-06 00:24] wakes up
[1518-10-18 00:42] wakes up
[1518-11-06 23:58] Guard #401 begins shift
[1518-10-18 00:08] falls asleep
[1518-05-24 23:50] Guard #3271 begins shift
[1518-03-23 00:04] Guard #509 begins shift
[1518-07-10 00:26] wakes up
[1518-08-16 00:56] wakes up
[1518-11-14 00:15] falls asleep
[1518-04-20 23:58] Guard #2663 begins shift
[1518-03-03 23:54] Guard #1327 begins shift
[1518-03-29 00:39] falls asleep
[1518-08-21 00:55] wakes up
[1518-04-17 00:53] wakes up
[1518-04-24 00:01] Guard #2207 begins shift
[1518-07-21 23:59] Guard #1409 begins shift
[1518-11-18 23:57] Guard #1409 begins shift
[1518-03-27 00:29] wakes up
[1518-03-26 00:03] Guard #2207 begins shift
[1518-03-06 00:57] wakes up
[1518-10-23 00:04] Guard #509 begins shift
[1518-10-08 00:56] wakes up
[1518-09-05 00:00] Guard #3271 begins shift
[1518-09-26 00:34] wakes up
[1518-09-18 00:34] wakes up
[1518-07-30 00:38] falls asleep
[1518-02-28 00:31] falls asleep
[1518-03-25 00:01] falls asleep
[1518-06-23 00:54] falls asleep
[1518-10-09 00:56] wakes up
[1518-09-07 00:17] falls asleep
[1518-09-10 23:57] Guard #619 begins shift
[1518-03-18 00:29] wakes up
[1518-09-16 00:35] wakes up
[1518-05-18 00:04] Guard #2417 begins shift
[1518-09-21 00:13] falls asleep
[1518-04-17 00:34] wakes up
[1518-03-07 00:46] falls asleep
[1518-11-23 00:07] falls asleep
[1518-10-29 00:56] wakes up
[1518-06-18 00:49] wakes up
[1518-02-25 00:46] falls asleep
[1518-09-29 23:59] Guard #433 begins shift
[1518-06-28 23:57] Guard #1327 begins shift
[1518-09-04 00:56] falls asleep
[1518-09-22 00:07] falls asleep
[1518-08-28 23:57] Guard #401 begins shift
[1518-03-21 00:09] falls asleep
[1518-03-12 00:01] Guard #2663 begins shift
[1518-05-13 23:59] Guard #509 begins shift
[1518-11-11 00:54] wakes up
[1518-05-12 00:53] wakes up
[1518-04-19 00:00] Guard #1409 begins shift
[1518-02-12 00:51] wakes up
[1518-07-12 00:04] falls asleep
[1518-09-15 00:51] wakes up
[1518-10-07 00:44] wakes up
[1518-07-29 00:09] falls asleep
[1518-10-04 00:47] falls asleep
[1518-08-24 00:33] wakes up
[1518-11-03 00:04] Guard #73 begins shift
[1518-06-12 00:00] Guard #2861 begins shift
[1518-11-20 23:56] Guard #433 begins shift
[1518-04-08 00:54] wakes up
[1518-03-23 00:48] wakes up
[1518-03-22 00:56] falls asleep
[1518-08-14 00:00] Guard #2861 begins shift
[1518-03-12 00:38] falls asleep
[1518-09-06 00:37] falls asleep
[1518-05-23 00:29] falls asleep
[1518-06-23 00:59] wakes up
[1518-11-14 00:42] wakes up
[1518-05-12 00:00] Guard #1301 begins shift
[1518-08-16 00:25] falls asleep
[1518-09-02 00:41] falls asleep
[1518-07-15 00:27] wakes up
[1518-08-04 00:04] Guard #3541 begins shift
[1518-03-15 00:42] falls asleep
[1518-09-23 00:00] Guard #73 begins shift
[1518-06-29 00:07] falls asleep
[1518-04-27 00:03] Guard #2333 begins shift
[1518-07-29 00:19] falls asleep
[1518-05-29 00:18] falls asleep
[1518-06-24 00:42] wakes up
[1518-06-06 00:36] wakes up
[1518-06-17 00:57] falls asleep
[1518-02-01 00:51] wakes up
[1518-11-04 00:55] wakes up
[1518-11-19 00:40] falls asleep
[1518-07-13 00:58] wakes up
[1518-04-14 00:04] Guard #3469 begins shift
[1518-06-20 23:58] Guard #619 begins shift
[1518-03-21 00:45] falls asleep
[1518-09-07 00:45] falls asleep
[1518-06-17 23:50] Guard #401 begins shift
[1518-09-10 00:45] wakes up
[1518-02-04 00:09] falls asleep
[1518-07-18 23:54] Guard #2411 begins shift
[1518-04-04 00:30] falls asleep
[1518-06-30 00:18] falls asleep
[1518-11-13 00:47] wakes up
[1518-04-11 00:49] falls asleep
[1518-10-01 23:59] Guard #3499 begins shift
[1518-08-16 23:56] Guard #3191 begins shift
[1518-10-25 00:17] falls asleep
[1518-04-25 00:37] falls asleep
[1518-04-17 00:41] falls asleep
[1518-05-05 00:50] wakes up
[1518-04-07 00:50] wakes up
[1518-02-10 00:00] Guard #2411 begins shift
[1518-08-22 00:46] falls asleep
[1518-05-01 00:48] wakes up
[1518-11-22 00:55] wakes up
[1518-06-12 00:33] falls asleep
[1518-07-23 00:45] wakes up
[1518-05-30 00:51] wakes up
[1518-11-03 00:46] wakes up
[1518-05-15 00:53] wakes up
[1518-06-26 00:28] falls asleep
[1518-07-30 00:16] falls asleep
[1518-02-26 23:58] Guard #1301 begins shift
[1518-02-08 00:31] falls asleep
[1518-10-01 00:57] wakes up
[1518-04-07 00:46] wakes up
[1518-04-26 00:49] wakes up
[1518-05-16 00:14] falls asleep
[1518-08-24 00:40] falls asleep
[1518-10-18 00:04] Guard #509 begins shift
[1518-08-29 00:50] falls asleep
[1518-07-25 00:16] falls asleep
[1518-08-26 00:18] falls asleep
[1518-07-19 00:04] falls asleep
[1518-02-21 00:49] wakes up
[1518-04-15 00:00] Guard #1831 begins shift
[1518-08-14 00:35] wakes up
[1518-09-18 00:27] falls asleep
[1518-04-10 00:26] falls asleep
[1518-02-16 00:39] falls asleep
[1518-08-01 00:40] falls asleep
[1518-03-24 23:54] Guard #3469 begins shift
[1518-03-07 00:36] falls asleep
[1518-06-19 00:21] falls asleep
[1518-09-10 00:16] falls asleep
[1518-09-24 23:56] Guard #2663 begins shift
[1518-08-23 00:04] Guard #73 begins shift
[1518-08-28 00:55] wakes up
[1518-03-03 00:00] Guard #433 begins shift
[1518-05-26 00:48] wakes up
[1518-08-19 23:59] Guard #2663 begins shift
[1518-08-26 00:34] wakes up
[1518-11-19 00:27] wakes up
[1518-08-13 00:22] falls asleep
[1518-03-09 00:30] falls asleep
[1518-03-16 00:51] falls asleep
[1518-03-13 00:56] wakes up
[1518-10-13 00:04] falls asleep
[1518-09-09 00:43] wakes up
[1518-03-09 00:58] wakes up
[1518-04-14 00:29] falls asleep
[1518-05-25 00:56] wakes up
[1518-04-02 23:56] Guard #3271 begins shift
[1518-06-28 00:57] wakes up
[1518-10-25 00:00] Guard #3499 begins shift
[1518-05-30 00:02] Guard #3499 begins shift
[1518-07-29 00:53] wakes up
[1518-06-17 00:58] wakes up
[1518-11-05 00:59] wakes up
[1518-10-25 00:53] wakes up
[1518-06-17 00:03] Guard #3499 begins shift
[1518-11-20 00:52] wakes up
[1518-05-02 23:57] Guard #1301 begins shift
[1518-09-26 00:01] Guard #2417 begins shift
[1518-10-30 00:53] falls asleep
[1518-08-15 00:01] Guard #2411 begins shift
[1518-07-16 00:00] Guard #509 begins shift
[1518-02-05 23:57] Guard #2207 begins shift
[1518-03-12 00:52] wakes up
[1518-03-19 00:33] falls asleep
[1518-02-18 00:01] falls asleep
[1518-06-09 00:01] Guard #1831 begins shift
[1518-06-30 00:40] falls asleep
[1518-10-24 00:35] falls asleep
[1518-04-09 23:58] Guard #2861 begins shift
[1518-08-25 00:04] falls asleep
[1518-07-28 23:58] Guard #619 begins shift
[1518-05-25 00:05] falls asleep
[1518-10-23 00:52] wakes up
[1518-03-15 23:59] Guard #2459 begins shift
[1518-05-01 00:02] Guard #3271 begins shift
[1518-10-30 00:57] wakes up
[1518-10-23 00:11] falls asleep
[1518-04-11 00:35] wakes up
[1518-06-04 00:29] wakes up
[1518-05-05 23:58] Guard #3271 begins shift
[1518-07-13 00:43] falls asleep
[1518-07-05 00:48] wakes up
[1518-06-10 00:10] falls asleep
[1518-05-19 00:02] Guard #2411 begins shift
[1518-09-01 00:54] wakes up
[1518-10-21 00:58] wakes up
[1518-10-04 00:48] wakes up
[1518-06-14 00:58] wakes up
[1518-10-22 00:32] falls asleep
[1518-07-28 00:48] wakes up
[1518-10-03 00:57] falls asleep
[1518-02-16 00:41] wakes up
[1518-08-28 00:48] falls asleep
[1518-09-26 00:08] falls asleep
[1518-06-25 00:03] falls asleep
[1518-07-02 00:06] falls asleep
[1518-03-17 00:46] wakes up
[1518-03-25 00:31] falls asleep
[1518-04-30 00:28] falls asleep
[1518-07-31 00:23] falls asleep
[1518-03-16 00:48] wakes up
[1518-09-20 00:03] Guard #433 begins shift
[1518-02-17 23:47] Guard #2417 begins shift
[1518-10-19 00:55] wakes up
[1518-09-25 00:28] falls asleep
[1518-02-14 00:00] Guard #2459 begins shift
[1518-06-02 00:42] falls asleep
[1518-07-17 00:56] wakes up
[1518-04-05 00:55] wakes up
[1518-11-09 00:59] wakes up
[1518-02-25 00:22] falls asleep
[1518-05-20 00:47] wakes up
[1518-11-02 00:13] falls asleep
[1518-05-16 00:51] wakes up
[1518-04-08 00:28] wakes up
[1518-03-27 00:09] falls asleep
[1518-05-29 00:58] wakes up
[1518-10-17 00:52] wakes up
[1518-11-12 23:59] Guard #2663 begins shift
[1518-04-03 00:56] wakes up
[1518-11-08 00:00] Guard #2861 begins shift
[1518-05-20 00:25] falls asleep
[1518-11-10 00:26] falls asleep
[1518-06-27 00:30] falls asleep
[1518-10-03 23:59] Guard #2663 begins shift
[1518-02-23 00:11] falls asleep
[1518-05-07 00:17] falls asleep
[1518-06-05 23:59] Guard #509 begins shift
[1518-06-26 00:03] Guard #2459 begins shift
[1518-03-27 00:01] Guard #509 begins shift
[1518-03-31 00:03] Guard #2663 begins shift
[1518-09-29 00:54] wakes up
[1518-04-11 00:52] wakes up
[1518-05-20 23:56] Guard #1301 begins shift
[1518-08-29 00:28] wakes up
[1518-11-10 00:30] wakes up
[1518-08-11 00:16] falls asleep
[1518-08-18 00:53] wakes up
[1518-07-27 00:59] wakes up
[1518-06-05 00:00] Guard #619 begins shift
[1518-10-02 00:32] falls asleep
[1518-08-07 00:02] Guard #2207 begins shift
[1518-04-30 00:58] wakes up
[1518-06-23 00:28] wakes up
[1518-05-09 00:41] wakes up
[1518-09-04 00:47] wakes up
[1518-10-12 23:47] Guard #509 begins shift
[1518-05-04 00:10] falls asleep
[1518-03-01 00:00] Guard #2411 begins shift
[1518-11-16 00:57] falls asleep
[1518-09-12 00:34] falls asleep
[1518-03-14 00:47] wakes up
[1518-07-24 00:45] wakes up
[1518-09-08 00:54] wakes up
[1518-10-17 00:48] wakes up
[1518-07-20 00:41] falls asleep
[1518-08-02 00:06] falls asleep
[1518-06-27 00:44] wakes up
[1518-03-24 00:26] falls asleep
[1518-06-13 00:41] wakes up
[1518-03-22 00:59] wakes up
[1518-10-12 00:00] Guard #509 begins shift
[1518-08-08 00:17] falls asleep
[1518-03-22 00:43] falls asleep
[1518-10-03 00:36] falls asleep
[1518-05-28 00:00] Guard #2417 begins shift
[1518-06-30 00:24] wakes up
[1518-10-14 00:57] wakes up
[1518-06-22 00:06] falls asleep
[1518-11-12 00:03] Guard #1877 begins shift
[1518-04-28 00:27] falls asleep
[1518-02-17 00:46] wakes up
[1518-04-01 00:00] Guard #2861 begins shift
[1518-05-13 00:00] Guard #3499 begins shift
[1518-05-04 23:50] Guard #2207 begins shift
[1518-03-23 00:26] wakes up
[1518-08-23 00:11] falls asleep
[1518-08-21 23:56] Guard #1301 begins shift
[1518-09-13 00:21] falls asleep
[1518-11-05 00:55] falls asleep
[1518-07-11 00:01] Guard #619 begins shift
[1518-05-05 00:11] wakes up
[1518-09-26 00:43] wakes up
[1518-06-15 00:00] Guard #1409 begins shift
[1518-03-15 00:47] wakes up
[1518-08-31 23:59] Guard #1831 begins shift
[1518-03-31 00:09] falls asleep
[1518-09-28 00:27] wakes up
[1518-09-30 00:42] wakes up
[1518-06-13 23:53] Guard #73 begins shift
[1518-06-28 00:00] Guard #433 begins shift
[1518-10-11 00:40] wakes up
[1518-10-24 00:27] wakes up
[1518-07-26 00:37] wakes up
[1518-07-18 00:35] falls asleep
[1518-08-01 00:03] Guard #3499 begins shift
[1518-08-14 00:25] falls asleep
[1518-10-11 00:43] falls asleep
[1518-07-04 00:38] wakes up
[1518-02-12 00:17] falls asleep
[1518-07-09 00:56] wakes up
[1518-06-04 00:19] falls asleep
[1518-11-15 00:26] wakes up
[1518-06-19 00:24] wakes up
[1518-02-09 00:34] falls asleep
[1518-03-05 00:45] falls asleep
[1518-08-10 00:21] falls asleep
[1518-08-06 00:27] wakes up
[1518-05-19 23:57] Guard #3541 begins shift
[1518-08-31 00:55] wakes up
[1518-05-26 00:14] falls asleep
[1518-03-11 00:09] falls asleep
[1518-06-24 00:03] Guard #3541 begins shift
[1518-05-07 00:54] wakes up
[1518-08-08 00:01] Guard #3541 begins shift
[1518-10-12 00:56] wakes up
[1518-11-13 00:14] falls asleep
[1518-09-30 00:28] wakes up
[1518-08-26 00:52] wakes up
[1518-03-01 00:34] wakes up
[1518-10-16 00:26] falls asleep
[1518-07-25 00:42] wakes up
[1518-06-03 00:27] wakes up
[1518-11-04 23:56] Guard #3541 begins shift
[1518-02-05 00:00] Guard #2663 begins shift
[1518-11-01 23:57] Guard #2207 begins shift
[1518-04-16 23:57] Guard #2861 begins shift
[1518-08-15 00:58] wakes up
[1518-07-10 00:23] falls asleep
[1518-09-07 23:58] Guard #433 begins shift
[1518-09-07 00:58] wakes up
[1518-09-05 23:59] Guard #73 begins shift
[1518-09-02 00:08] falls asleep
[1518-08-12 23:59] Guard #619 begins shift
[1518-05-26 23:49] Guard #3271 begins shift
[1518-08-20 00:18] falls asleep
[1518-05-12 00:32] falls asleep
[1518-11-01 00:04] Guard #509 begins shift
[1518-03-18 00:56] wakes up
[1518-08-02 00:03] Guard #3469 begins shift
[1518-08-06 00:00] Guard #3541 begins shift
[1518-02-21 00:00] Guard #3469 begins shift
[1518-09-01 23:57] Guard #3271 begins shift
[1518-06-15 00:20] wakes up
[1518-04-06 00:44] falls asleep
[1518-07-27 00:45] wakes up
[1518-03-08 00:24] wakes up
[1518-04-16 00:00] Guard #2207 begins shift
[1518-04-03 00:49] falls asleep
[1518-04-11 00:24] wakes up
[1518-04-20 00:42] wakes up
[1518-02-04 00:42] falls asleep
[1518-08-29 00:26] falls asleep
[1518-11-15 00:35] falls asleep
[1518-07-30 00:25] wakes up
[1518-09-17 00:03] Guard #1697 begins shift
[1518-05-12 00:44] falls asleep
[1518-06-11 00:54] wakes up
[1518-07-03 00:58] wakes up
[1518-02-17 00:59] wakes up
[1518-10-02 00:42] falls asleep
[1518-11-18 00:04] Guard #2411 begins shift
[1518-05-19 00:35] falls asleep
[1518-11-16 00:36] falls asleep
[1518-02-10 00:42] falls asleep
[1518-11-03 00:15] falls asleep
[1518-07-13 23:56] Guard #401 begins shift
[1518-04-23 00:00] Guard #1327 begins shift
[1518-08-18 00:01] Guard #401 begins shift
[1518-02-27 00:43] falls asleep
[1518-07-26 00:46] falls asleep
[1518-02-19 00:37] wakes up
[1518-03-28 00:22] falls asleep
[1518-05-17 00:33] falls asleep
[1518-06-28 00:25] falls asleep
[1518-06-08 00:47] wakes up
[1518-08-04 00:55] wakes up
[1518-09-23 00:11] falls asleep
[1518-09-14 23:59] Guard #2207 begins shift
[1518-07-04 00:22] falls asleep
[1518-05-30 00:42] wakes up
[1518-03-10 23:58] Guard #509 begins shift
[1518-08-21 00:01] falls asleep
[1518-08-12 00:31] wakes up
[1518-03-13 00:02] Guard #2663 begins shift
[1518-05-29 00:53] falls asleep
[1518-11-08 00:57] wakes up
[1518-02-24 00:00] Guard #3271 begins shift
[1518-01-31 23:59] Guard #401 begins shift
[1518-02-16 00:59] wakes up
[1518-02-07 00:53] wakes up
[1518-03-22 00:40] wakes up
[1518-05-24 00:58] wakes up
[1518-08-07 00:47] falls asleep
[1518-07-05 00:01] Guard #2663 begins shift
[1518-08-02 00:14] falls asleep
[1518-05-08 00:50] falls asleep
[1518-07-17 00:12] falls asleep
[1518-05-03 23:59] Guard #1831 begins shift
[1518-04-07 00:16] falls asleep
[1518-05-14 00:48] wakes up
[1518-09-14 00:54] wakes up
[1518-06-09 23:56] Guard #3271 begins shift
[1518-02-05 00:50] wakes up
[1518-04-11 00:57] falls asleep
[1518-11-05 00:46] falls asleep
[1518-06-03 23:58] Guard #509 begins shift
[1518-02-28 00:43] falls asleep
[1518-09-10 00:52] falls asleep
[1518-09-02 00:57] wakes up
[1518-03-23 23:48] Guard #3271 begins shift
[1518-03-31 00:46] wakes up
[1518-08-26 00:44] falls asleep
[1518-07-14 00:30] falls asleep
[1518-09-02 23:59] Guard #3541 begins shift
[1518-04-03 00:29] falls asleep
[1518-02-07 00:44] falls asleep
[1518-10-10 23:59] Guard #401 begins shift
[1518-06-22 00:52] wakes up
[1518-03-22 00:52] wakes up
[1518-06-08 00:38] falls asleep
[1518-02-19 00:27] falls asleep
[1518-02-18 00:53] wakes up
[1518-04-26 00:29] wakes up
[1518-10-26 23:57] Guard #2411 begins shift
[1518-11-07 00:48] wakes up
[1518-04-07 00:53] falls asleep
[1518-05-14 00:25] falls asleep
[1518-09-10 00:00] Guard #401 begins shift
[1518-09-30 00:19] falls asleep
[1518-09-10 00:26] wakes up
[1518-11-18 00:44] falls asleep
[1518-03-21 00:16] wakes up
[1518-09-12 00:02] Guard #509 begins shift
[1518-06-16 00:48] falls asleep
[1518-09-15 23:59] Guard #73 begins shift
[1518-02-04 00:26] wakes up
[1518-09-12 00:42] wakes up
[1518-11-15 00:03] Guard #73 begins shift
[1518-10-30 00:35] wakes up
[1518-03-07 00:05] wakes up
[1518-11-01 00:08] falls asleep
[1518-09-24 00:24] falls asleep
[1518-08-02 00:09] wakes up
[1518-08-10 23:57] Guard #1877 begins shift
[1518-10-06 00:51] wakes up
[1518-11-11 00:00] Guard #1409 begins shift
[1518-04-30 00:47] falls asleep
[1518-10-14 00:55] falls asleep
[1518-08-05 00:03] Guard #509 begins shift
[1518-06-22 23:57] Guard #619 begins shift
[1518-04-15 00:53] wakes up
[1518-07-28 00:34] falls asleep
[1518-03-23 00:30] falls asleep
[1518-09-28 23:52] Guard #1831 begins shift
[1518-10-13 23:50] Guard #2207 begins shift
[1518-05-06 00:43] falls asleep
[1518-05-29 00:45] wakes up
[1518-03-28 00:47] wakes up
[1518-05-17 00:46] falls asleep
[1518-07-06 00:55] wakes up
[1518-10-03 00:00] Guard #2417 begins shift
[1518-08-19 00:07] falls asleep
[1518-04-04 00:51] wakes up
[1518-05-26 00:17] wakes up
[1518-05-24 00:00] Guard #509 begins shift
[1518-08-08 23:58] Guard #2333 begins shift
[1518-02-08 00:22] wakes up
[1518-11-15 00:52] wakes up
[1518-10-02 00:34] wakes up
[1518-09-02 00:36] wakes up
[1518-06-27 00:01] Guard #1877 begins shift
[1518-04-11 00:28] falls asleep
[1518-03-14 00:00] Guard #2663 begins shift
[1518-08-29 00:45] wakes up
[1518-02-16 00:13] falls asleep
[1518-07-07 00:35] falls asleep
[1518-04-16 00:24] falls asleep
[1518-07-01 00:47] wakes up
[1518-10-31 00:28] falls asleep
[1518-10-07 23:56] Guard #619 begins shift
[1518-07-31 00:02] Guard #401 begins shift
[1518-07-22 00:50] wakes up
[1518-04-22 00:02] Guard #2207 begins shift
[1518-09-13 00:35] wakes up
[1518-08-27 00:21] falls asleep
[1518-09-27 00:00] Guard #2411 begins shift
[1518-09-27 00:38] falls asleep
[1518-06-07 00:57] wakes up
[1518-03-17 00:06] falls asleep
[1518-11-15 00:50] falls asleep
[1518-05-08 23:59] Guard #2861 begins shift
[1518-08-16 00:04] Guard #509 begins shift
[1518-08-29 23:52] Guard #2417 begins shift
[1518-10-29 00:52] wakes up
[1518-10-15 00:41] wakes up
[1518-07-14 00:57] wakes up
[1518-07-16 00:24] falls asleep
[1518-05-13 00:50] wakes up
[1518-07-05 00:40] falls asleep
[1518-03-07 00:50] wakes up
[1518-05-10 00:03] falls asleep
[1518-06-15 00:47] wakes up
[1518-06-27 00:47] falls asleep
[1518-04-23 00:40] falls asleep
[1518-02-10 00:49] wakes up
[1518-09-26 00:39] falls asleep
[1518-04-25 23:54] Guard #1301 begins shift
[1518-06-17 00:22] falls asleep
[1518-02-21 00:36] falls asleep
[1518-04-20 00:01] falls asleep
[1518-10-08 00:19] falls asleep
[1518-06-20 00:54] wakes up
[1518-09-14 00:57] falls asleep
[1518-03-23 00:21] falls asleep
[1518-02-26 00:42] wakes up
[1518-11-17 00:00] falls asleep
[1518-07-30 00:55] falls asleep
[1518-10-26 00:02] falls asleep
[1518-05-28 23:57] Guard #401 begins shift
[1518-11-08 00:09] falls asleep
[1518-11-22 00:38] falls asleep
[1518-02-14 00:52] falls asleep
[1518-03-24 00:01] falls asleep
[1518-06-16 00:03] Guard #3271 begins shift
[1518-09-27 00:15] falls asleep
[1518-05-17 00:42] wakes up
[1518-03-27 00:56] wakes up
[1518-08-27 00:02] Guard #2663 begins shift
[1518-09-11 00:59] wakes up
[1518-04-23 00:53] wakes up
[1518-03-28 23:57] Guard #2207 begins shift
[1518-08-04 00:26] wakes up
[1518-06-21 00:59] wakes up
[1518-02-16 00:45] falls asleep
[1518-07-04 00:01] Guard #2417 begins shift
[1518-08-06 00:17] falls asleep
[1518-07-18 00:55] wakes up
[1518-02-15 00:03] Guard #3499 begins shift
[1518-04-07 00:49] falls asleep
[1518-05-12 00:38] wakes up
[1518-09-16 00:28] falls asleep
[1518-05-18 00:48] wakes up
[1518-05-04 00:58] wakes up
[1518-07-01 00:01] Guard #73 begins shift
[1518-09-24 00:04] Guard #3499 begins shift
[1518-06-16 00:56] wakes up
[1518-03-16 00:43] falls asleep
[1518-03-06 23:53] Guard #3469 begins shift
[1518-11-04 00:38] falls asleep
[1518-03-09 23:56] Guard #2333 begins shift
[1518-10-12 00:24] falls asleep
[1518-11-21 23:56] Guard #433 begins shift
[1518-10-10 00:07] falls asleep
[1518-11-03 23:57] Guard #3499 begins shift
[1518-03-08 00:48] wakes up
[1518-10-24 00:42] wakes up
[1518-10-16 00:56] wakes up
[1518-10-17 00:04] Guard #1831 begins shift
[1518-07-16 00:29] wakes up
[1518-04-06 00:01] Guard #3271 begins shift
[1518-10-09 00:00] Guard #509 begins shift
[1518-04-10 00:44] wakes up
[1518-05-22 00:31] wakes up
[1518-11-16 00:03] Guard #2861 begins shift
[1518-02-11 00:05] falls asleep
[1518-04-18 00:59] wakes up
[1518-03-28 00:27] wakes up
[1518-09-08 23:52] Guard #73 begins shift
[1518-04-11 00:59] wakes up
[1518-07-11 00:56] wakes up
[1518-02-28 00:38] wakes up
[1518-04-29 00:26] wakes up
[1518-10-03 00:50] wakes up
[1518-08-19 00:50] wakes up
[1518-08-20 23:54] Guard #1831 begins shift
[1518-03-03 00:08] wakes up
[1518-10-11 00:37] falls asleep
[1518-09-20 00:51] wakes up
[1518-03-04 00:44] wakes up
[1518-11-20 00:04] falls asleep
[1518-05-17 00:04] Guard #2411 begins shift
[1518-05-08 00:06] falls asleep
[1518-07-07 00:52] wakes up
[1518-02-03 00:03] Guard #3541 begins shift
[1518-03-18 00:40] falls asleep
[1518-06-23 00:41] wakes up
[1518-10-06 00:28] falls asleep
[1518-02-20 00:02] Guard #3191 begins shift
[1518-10-05 23:57] Guard #73 begins shift
[1518-10-22 00:00] Guard #3499 begins shift
[1518-07-19 00:37] falls asleep
[1518-04-19 00:51] wakes up
[1518-06-01 00:57] wakes up
[1518-04-28 00:30] wakes up
[1518-04-19 00:46] falls asleep
[1518-07-13 00:00] Guard #1831 begins shift
[1518-10-24 00:02] Guard #3541 begins shift
[1518-05-11 00:01] Guard #3469 begins shift
[1518-06-11 00:26] wakes up
[1518-01-31 00:24] falls asleep
[1518-04-06 00:57] wakes up
[1518-06-02 00:36] wakes up
[1518-05-21 00:49] wakes up
[1518-04-15 00:52] falls asleep
[1518-08-22 00:12] falls asleep
[1518-06-09 00:41] wakes up
[1518-03-19 00:34] wakes up
[1518-03-29 00:46] wakes up
[1518-10-19 00:39] wakes up
[1518-10-14 00:05] falls asleep
[1518-05-05 00:23] falls asleep
[1518-09-12 23:59] Guard #3541 begins shift
[1518-11-14 00:52] wakes up
[1518-05-03 00:12] falls asleep
[1518-02-08 23:58] Guard #2411 begins shift
[1518-07-17 23:57] Guard #1301 begins shift
[1518-05-28 00:07] falls asleep
[1518-02-25 00:02] Guard #1877 begins shift
[1518-03-27 00:32] falls asleep
[1518-07-31 00:50] wakes up
[1518-02-07 00:00] Guard #1301 begins shift
[1518-03-11 00:34] falls asleep
[1518-07-24 00:04] Guard #1409 begins shift
[1518-07-12 00:37] wakes up
[1518-05-22 00:22] falls asleep
[1518-06-06 23:56] Guard #3271 begins shift
'''

if __name__ == '__main__':
    print(part1(puzzle_input))
    print(list(part2(puzzle_input)))
