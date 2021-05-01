from events import Task, BusyBlock, TaskBlock
from quickstart import populateBusyBlocks
import datetime

"""
schedule() will use a modified version of the Priority Scheduling algorithm, 
    with Earliest Deadline First for tiebreaks, to schedule blocks of time to 
    complete all tasks by their deadlines while avoiding scheduling over 
    pre-existing busy blocks of time. Returns a list of TaskBlocks.
tasks : Task list
busy_blocks : BusyBlock list, sorted in time increasing order
day_start_time : datetime.time
day_end_time : datetime.time
leeway : datetime.timedelta - amount of time before the deadline a task should 
    be completed by
buffer : datetime.timedelta - minimum amount of time between each scheduled block
"""
def schedule(tasks, busy_blocks, day_start_time, day_end_time, leeway, buffer=datetime.timedelta(minutes=5)):
    task_blocks = []
    """TODO: make overlapping tasks one big task to satisfy schedule_with_earliest_start() precondition"""
    scheduled_blocks = busy_blocks.copy()
    # sort tasks by descending priority with earlier deadlines first for tiebreaks
    priority_scheduling = lambda task: (task.priority, -task.end_time)
    sorted_tasks = sorted(tasks, key=priority_scheduling, reverse=True) 
    
    # schedule taskblocks for all tasks, in sorted order
    for task in sorted_tasks:
        targeted_finish = task.due - leeway
        time_till_due = targeted_finish - datetime.datetime.now()
        # attempt to equally space task blocks from now till the targeted finish time
        secs_btwn_blocks = time_till_due.total_seconds() / task.num_blocks
        
        while task.num_blocks_assigned < task.num_blocks:
            # calulate ideal start time to equally space task blocks
            time_from_blockstart_to_finish = datetime.timedelta(seconds=task.num_blocks_assigned * secs_btwn_blocks)
            targeted_block_start_time = targeted_finish - time_from_blockstart_to_finish
            
            # schedule_with_earliest_start() will increment task.num_blocks_assigned
            scheduled = schedule_with_earliest_start(task, targeted_block_start_time, day_start_time, day_end_time, scheduled_blocks, buffer)
            task_blocks.append(scheduled)
            scheduled_blocks.append(BusyBlock(scheduled.name, scheduled.start_time, scheduled.end_time))
            
    return task_blocks

"""
schedule_with_earliest_start() attempts to schedule 1 block of the task at the 
    earliest possible timeslot so that the earliest start_time is start. Returns 
    an object of type TaskBlock.
task : Task - the task to be scheduled
start : datetime.datetime - the earliest possible start_time
day_start_time : datetime.time
day_end_time : datetime.time
scheduled_blocks : BusyBlock list - contains all scheduled events 
buffer : int - minimum amount of seconds between each scheduled block

precondition: scheduled_blocks has no overlapping blocks
"""
def schedule_with_earliest_start(task, start, day_start_time, day_end_time, scheduled_blocks, buffer):
    # remove all scheduled blocks that end before the earliest start time - buffer
    starts_after_start_time = lambda block: block.start_time > start - buffer
    blocks_before_task_due = filter(starts_after_start_time, scheduled_blocks)
    
    # sort with earliest event first
    sorted_blocks = sorted(blocks_before_task_due, key=lambda block: block.start_time)
    
    block_duration = datetime.timedelta(seconds=task.expected_duration.total_seconds() / task.num_blocks)
    
    end_of_start_day = datetime.datetime.combine(start.date, day_end_time)
    start_of_next_day = datetime.datetime.combine(start.date, day_start_time) + datetime.timedelta(days=1)
    first_feasible_start = start if end_of_start_day - start >= block_duration else start_of_next_day
    
    # Case 0: no scheduled blocks
    if sorted_blocks == []:
        task.num_blocks_assigned += 1
        return TaskBlock(first_feasible_start, first_feasible_start + block_duration, task, task.num_blocks_assigned)
    
    # Case 1: task block can be scheduled before the first already scheduled task block
    """TODO: WIP, fix this case"""
    end_of_first_feasible_start_day = datetime.datetime.combine(first_feasible_start.date, day_end_time)
    ideal_block_end = first_feasible_start + block_duration
    latest_end_before_first_block = sorted_blocks[0].start_time - buffer
    first_blocker = end_of_first_feasible_start_day if end_of_first_feasible_start_day < latest_end_before_first_block else latest_end_before_first_block
    if (ideal_block_end + buffer) <= sorted_blocks[0].start_time:
        task.num_blocks_assigned += 1
        return TaskBlock(start, ideal_block_end, task, task.num_blocks_assigned)
    
    # Case 2: task block will be scheduled at earliest possible time between 2 other blocks
    for i in range(len(sorted_blocks) - 1):
        this_block = sorted_blocks[i]
        next_block = sorted_blocks[i+1]
        
        end_of_this_block_day = datetime.datetime.combine(this_block.end_time.date, day_end_time)
        start_of_next_block_day = datetime.datetime.combine(next_block.start_time.date, day_start_time)
        
        earliest_start = this_block.end_time + buffer
        latest_end = next_block.start_time - buffer
        end_of_free_period = end_of_this_block_day if end_of_this_block_day < latest_end else latest_end
        
        # case if there is enough time from end of this block + buffer to end of free period
        if end_of_free_period - earliest_start >= block_duration:
            task.num_blocks_assigned += 1
            return TaskBlock(earliest_start, earliest_start + block_duration, task, task.num_blocks_assigned)
        # case if second task is not on the same date as the first 
        # AND there is enough time from the start of the day to start of second block
        elif this_block.end_time.date != next_block.start_time.date and \
            latest_end - start_of_next_block_day >= block_duration:
            task.num_blocks_assigned += 1
            return TaskBlock(start_of_next_block_day, start_of_next_block_day + block_duration, task, task.num_blocks_assigned)
        
    # Case 3: schedule new task block after last scheduled task but before target deadline
    """TODO: case 3"""
    
    return TaskBlock()
