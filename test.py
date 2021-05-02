import unittest
import datetime
from datetime import datetime, timedelta, time
from events import Task, BusyBlock, TaskBlock
from scheduler import schedule, schedule_with_earliest_start, consolidate_blocks

## consolidate_blocks tests
two_overlapping = [
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 2, 30, 0, 0)),
    BusyBlock("2", datetime(2021, 5, 1, 2, 00, 0, 0), datetime(2021, 5, 1, 3, 30, 0, 0))]

two_overlapping_combined = [
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 3, 30, 0, 0))]

two_overlapping_one_not = [
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 2, 30, 0, 0)),
    BusyBlock("2", datetime(2021, 5, 1, 2, 00, 0, 0), datetime(2021, 5, 1, 3, 30, 0, 0)),
    BusyBlock("3", datetime(2021, 5, 1, 5, 30, 0, 0), datetime(2021, 5, 1, 7, 30, 0, 0))]

two_overlapping_one_not_combined = [
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 3, 30, 0, 0)),
    BusyBlock("3", datetime(2021, 5, 1, 5, 30, 0, 0), datetime(2021, 5, 1, 7, 30, 0, 0))]

two_overlapping_two_not = [
    BusyBlock("0", datetime(2021, 5, 1, 0, 00, 0, 0), datetime(2021, 5, 1, 1, 30, 0, 0)),
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 2, 30, 0, 0)),
    BusyBlock("2", datetime(2021, 5, 1, 2, 00, 0, 0), datetime(2021, 5, 1, 3, 30, 0, 0)),
    BusyBlock("3", datetime(2021, 5, 1, 5, 30, 0, 0), datetime(2021, 5, 1, 7, 30, 0, 0))]

two_overlapping_two_not_combined = [
    BusyBlock("0", datetime(2021, 5, 1, 0, 00, 0, 0), datetime(2021, 5, 1, 1, 30, 0, 0)),
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 3, 30, 0, 0)),
    BusyBlock("3", datetime(2021, 5, 1, 5, 30, 0, 0), datetime(2021, 5, 1, 7, 30, 0, 0))]

three_overlapping = [
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 1, 2, 30, 0, 0)),
    BusyBlock("2", datetime(2021, 5, 1, 2, 00, 0, 0), datetime(2021, 5, 2, 3, 30, 0, 0)),
    BusyBlock("3", datetime(2021, 5, 2, 3, 29, 0, 0), datetime(2021, 5, 2, 7, 30, 0, 0))]

three_overlapping_combined = [
    BusyBlock("1", datetime(2021, 5, 1, 1, 30, 0, 0), datetime(2021, 5, 2, 7, 30, 0, 0))]

## schedule_with_earliest_start tests
start = time(6, 30)
end = time(20)
zero = timedelta(seconds=0)
five = timedelta(minutes=5)
fifteen = timedelta(minutes=15)

task1 = Task("task1", datetime(2021, 4, 30, 10, 0), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task11 = Task("task11", datetime(2021, 4, 30, 10, 0), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task12 = Task("task12", datetime(2021, 4, 30, 10, 0), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task13 = Task("task13", datetime(2021, 4, 30, 10, 0), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task2 = Task("task2", datetime(2021, 5, 1, 11, 30), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task21 = Task("task21", datetime(2021, 5, 1, 11, 30), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task22 = Task("task22", datetime(2021, 5, 1, 11, 30), timedelta(hours=2), 2, 1, datetime(2021, 4, 30, 8, 0))
task3 = Task("task3", datetime(2021, 5, 1, 11, 30), timedelta(hours=1), 1, 1, datetime(2021, 4, 30, 8, 0))
task4 = Task("task4", datetime(2021, 5, 1, 23), timedelta(hours=4), 3, 2, datetime(2021, 4, 30, 3, 30))

time0 = datetime(2021, 4, 30, 0, 0)
time630 = datetime(2021, 4, 30, 6, 30)
time7 = datetime(2021, 4, 30, 7, 0)
time750 = datetime(2021, 4, 30, 7, 50)
time8 = datetime(2021, 4, 30, 8, 0)
time815 = datetime(2021, 4, 30, 8, 15)
time820 = datetime(2021, 4, 30, 8, 20)
time830 = datetime(2021, 4, 30, 8, 30)
time835 = datetime(2021, 4, 30, 8, 35)
time9 = datetime(2021, 4, 30, 9, 0)
time905 = datetime(2021, 4, 30, 9, 5)
time920 = datetime(2021, 4, 30, 9, 20)
time925 = datetime(2021, 4, 30, 9, 25)
time935 = datetime(2021, 4, 30, 9, 35)
time10 = datetime(2021, 4, 30, 10, 0)
time1930 = datetime(2021, 4, 30, 19, 30)

time_nextday630 = datetime(2021, 5, 1, 6, 30)
time_nextday730 = datetime(2021, 5, 1, 7, 30)
time_nextday955 = datetime(2021, 5, 1, 9, 55)
time_nextday10 = datetime(2021, 5, 1, 10, 0)
time_nextday11 = datetime(2021, 5, 1, 11, 0)

block_8_815 = BusyBlock("8 to 8:15", time8, time815)
block_8_830 = BusyBlock("8 to 8:30", time8, time830)
block_830_1930 = BusyBlock("8:30 to 19:30", time830, time1930)
block_905_935 = BusyBlock("9:05 to 9:35", time905, time935)
block_925_935 = BusyBlock("9:25 to 9:35", time925, time935)

block_nextday_630_955 = BusyBlock("next day 6:30 to 9:55", time_nextday630, time_nextday955)
block_nextday_10_11 = BusyBlock("next day 10 to 11", time_nextday10, time_nextday11)

## schedule() tests, advanced
may2_12 = datetime(2021, 5, 2, 12)
may2_17 = datetime(2021, 5, 2, 17)
may3_7 = datetime(2021, 5, 3, 7)
may3_715 = datetime(2021, 5, 3, 7, 15)
may3_915 = datetime(2021, 5, 3, 9, 15)
may6_1715 = datetime(2021, 5, 6, 17, 15)
may6_9 = datetime(2021, 5, 6, 9)
may6_1915 = datetime(2021, 5, 6, 19, 15)
may6_17 = datetime(2021, 5, 6, 17)
may10_1715 = datetime(2021, 5, 10, 17, 15)
may10_9 = datetime(2021, 5, 10, 9)
may10_1915 = datetime(2021, 5, 10, 19, 15)
may10_17 = datetime(2021, 5, 10, 17)
may14_9 = datetime(2021, 5, 14, 9)
may14_17 = datetime(2021, 5, 14, 17)

block_may2_12_may3_7 = BusyBlock("may 2nd 12:00 to may 3rd 7:00", may2_12, may3_7)

task5 = Task("task5", may14_17, timedelta(hours=6), 3, 0, may2_17)
task6 = Task("task6", may14_9, timedelta(hours=16), 2, 2, may6_9)

class TestScheduler(unittest.TestCase):
    maxDiff = None
    
    def test_consolidate_blocks(self):
        self.assertEqual([], consolidate_blocks([]))
        self.assertEqual(two_overlapping_combined, 
                         consolidate_blocks(two_overlapping_combined))
        self.assertEqual(two_overlapping_combined, 
                         consolidate_blocks(two_overlapping))
        self.assertEqual(two_overlapping_one_not_combined, 
                         consolidate_blocks(two_overlapping_one_not))
        self.assertEqual(two_overlapping_two_not_combined, 
                         consolidate_blocks(two_overlapping_two_not))
        self.assertEqual(three_overlapping_combined, 
                         consolidate_blocks(three_overlapping))
        
    def test_schedule_with_earliest_start_Case1(self):
        self.assertEqual(TaskBlock(time8, time9, task1, 2),
            schedule_with_earliest_start(task1, time8, start, end, [], zero, zero))
        self.assertEqual(TaskBlock(time8, time9, task11, 2), 
            schedule_with_earliest_start(task11, time8, start, end, [block_905_935], zero, five))
        self.assertEqual(TaskBlock(time835, time935, task12, 2), 
            schedule_with_earliest_start(task12, time8, start, end, [block_8_830], zero, five))
        # case where release time is not during working hours
        self.assertEqual(TaskBlock(time630, time750, task4, 3), 
            schedule_with_earliest_start(task4, time0, start, end, [], zero, five))
        
    def test_schedule_with_earliest_start_Case21(self):
        self.assertEqual(TaskBlock(time820, time920, task13, 2), 
            schedule_with_earliest_start(task13, time8, start, end, 
                                         [block_8_815, block_925_935], zero, five))
        self.assertEqual(TaskBlock(time820, time920, task13, 1), 
            schedule_with_earliest_start(task13, time8, start, end, 
                                         [block_8_815, block_nextday_10_11], zero, five))
        
    def test_schedule_with_earliest_start_Case22(self):
        self.assertEqual(TaskBlock(time_nextday630, time_nextday730, task2, 2), 
            schedule_with_earliest_start(task2, time8, start, end, 
                                         [block_830_1930, block_nextday_10_11], zero, five))
        
    def test_schedule_with_earliest_start_Case31(self):
        self.assertEqual(TaskBlock(time_nextday10, time_nextday11, task21, 2), 
            schedule_with_earliest_start(task21, time8, start, end, 
                                         [block_830_1930, block_nextday_630_955], zero, five))
        
    def test_schedule_with_earliest_start_Case32(self):
        self.assertEqual(TaskBlock(time_nextday630, time_nextday730, task22, 2), 
            schedule_with_earliest_start(task22, time8, start, end, [block_830_1930], zero, five))
        
    def test_schedule_basic(self):
        self.assertEqual([TaskBlock(time8, time9, task3, 1)], 
            schedule([task3], [block_905_935], start, end))
        
    def test_schedule_advanced(self):
        self.assertEqual([TaskBlock(may10_9, may10_17, task6, 2), 
                          TaskBlock(may6_9, may6_17, task6, 1),
                          TaskBlock(may10_1715, may10_1915, task5, 3),
                          TaskBlock(may6_1715, may6_1915, task5, 2),
                          TaskBlock(may3_715, may3_915, task5, 1)], 
            schedule([task5, task6], [block_may2_12_may3_7], start, end, zero, fifteen))
        
        
if __name__ == '__main__':
    unittest.main()