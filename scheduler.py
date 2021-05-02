from events import Task, BusyBlock, TaskBlock
from quickstart import populateBusyBlocks
import datetime
from datetime import datetime, timedelta, time

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
def schedule(tasks, busy_blocks, day_start_time=time(hour=9), day_end_time=time(hour=23), 
             leeway=timedelta(minutes=0), buffer=timedelta(minutes=5)):
    task_blocks = []
    # make overlapping tasks one big task to satisfy schedule_with_earliest_start() precondition
    scheduled_blocks = consolidate_blocks(busy_blocks.copy())
    # sort tasks by descending priority with earlier deadlines first for tiebreaks
    priority_scheduling = lambda task: (task.due, -task.priority)
    sorted_tasks = sorted(tasks, key=priority_scheduling) 
    
    # schedule taskblocks for all tasks, in sorted order
    for task in sorted_tasks:
        targeted_finish = task.due - leeway
        time_till_due = targeted_finish - task.start
        # attempt to equally space task blocks from task start till the targeted finish time
        secs_btwn_blocks = time_till_due.total_seconds() / task.num_blocks
        
        while task.num_blocks_assigned < task.num_blocks:
            # calulate ideal start time to equally space task blocks
            time_from_blockstart_to_finish = timedelta(seconds=(task.num_blocks_assigned + 1) * secs_btwn_blocks)
            targeted_block_start_time = targeted_finish - time_from_blockstart_to_finish
            try:
                # schedule_with_earliest_start() will increment task.num_blocks_assigned
                scheduled = schedule_with_earliest_start(task, targeted_block_start_time, day_start_time, day_end_time, scheduled_blocks, leeway, buffer)
                task_blocks.append(scheduled)
                scheduled_blocks.append(BusyBlock(scheduled.task.name, scheduled.start_time, scheduled.end_time))
            except Exception as e:
                raise e
            
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
def schedule_with_earliest_start(task, start, day_start_time, day_end_time, scheduled_blocks, leeway, buffer):
    block_duration = timedelta(seconds=task.expected_duration.total_seconds() / task.num_blocks)
    targeted_finish = task.due - leeway
    task_block_num = task.num_blocks - task.num_blocks_assigned
    
    # remove all scheduled blocks that end before the earliest start time - buffer or start after the deadline
    starts_after_start_time = lambda block: block.end_time > start - buffer and block.start_time < task.due
    blocks_before_task_due = filter(starts_after_start_time, scheduled_blocks)
    
    # sort with earliest event first
    sorted_blocks = sorted(blocks_before_task_due, key=lambda block: block.start_time)
    
    end_of_start_day = datetime.combine(start.date(), day_end_time)
    start_of_start_day = datetime.combine(start.date(), day_start_time)
    next_start = start_of_start_day if start.time() < day_start_time else start_of_start_day + timedelta(days=1)
    first_feasible_start = start if end_of_start_day - start >= block_duration and \
                                    start.time() > day_start_time and \
                                    start.time() < day_end_time \
                                 else next_start
    
    ## Case 1: no scheduled blocks OR 
    #   new task block can be scheduled before the first already scheduled task block
    if sorted_blocks == [] or \
        (sorted_blocks[0].start_time - buffer) - first_feasible_start >= block_duration:
        task.num_blocks_assigned += 1
        return TaskBlock(first_feasible_start, first_feasible_start + block_duration, task, task_block_num)
    
    ## Case 2: task block will be scheduled at earliest possible time between 2 other blocks
    for i in range(len(sorted_blocks) - 1):
        this_block = sorted_blocks[i]
        next_block = sorted_blocks[i+1]
        
        end_of_this_block_day = datetime.combine(this_block.end_time.date(), day_end_time)
        start_of_next_day = datetime.combine(this_block.end_time.date(), day_start_time) + timedelta(days=1)
        
        earliest_start = this_block.end_time + buffer
        latest_end = next_block.start_time - buffer
        end_of_free_period = end_of_this_block_day if end_of_this_block_day < latest_end else latest_end
        # Case 2.1: if there is enough time from end of current block + buffer to end of free period
        if end_of_free_period - earliest_start >= block_duration:
            task.num_blocks_assigned += 1
            return TaskBlock(earliest_start, earliest_start + block_duration, task, task_block_num)
        # Case 2.2: if next task is not on the same date as the current 
        # AND there is enough time from the start of the next day to start of next block
        elif this_block.end_time.date() != next_block.start_time.date() and \
            latest_end - start_of_next_day >= block_duration:
            task.num_blocks_assigned += 1
            return TaskBlock(start_of_next_day, start_of_next_day + block_duration, task, task_block_num)
        
    ## Case 3: schedule new task block after last scheduled task but before target deadline
    last_block = sorted_blocks[len(sorted_blocks) - 1]
    end_of_last_block_day = datetime.combine(last_block.end_time.date(), day_end_time)
    end_of_feasible_period = end_of_last_block_day if end_of_last_block_day < targeted_finish else targeted_finish
    next_earliest_start = last_block.end_time + buffer
    start_of_day_after_last_block = datetime.combine(last_block.end_time.date(), day_start_time) + timedelta(days=1)
    # Case 3.1: attempt to schedule immediately after last block
    if end_of_feasible_period - next_earliest_start >= block_duration:
        task.num_blocks_assigned += 1
        return TaskBlock(next_earliest_start, next_earliest_start + block_duration, task, task_block_num)
    # Case 3.2: attempt to schedule at beginning of day after last block
    elif targeted_finish - start_of_day_after_last_block >= block_duration:
        task.num_blocks_assigned += 1
        return TaskBlock(start_of_day_after_last_block, start_of_day_after_last_block + block_duration, task, task_block_num)
    
    raise Exception("Cannot schedule before deadline with current parameters :-(")

"""
consolidate_blocks() finds any overlapping blocks and combines them into one
    longer BusyBlock.
block_list : BusyBlock list

precondition: block_list is sorted in ascending start_time order
"""
def consolidate_blocks(block_list):
    if len(block_list) == 0:
        return []
    
    blocks = [block_list[0]]
    for i in range(1, len(block_list)):
        next_block = block_list[i]
        top_block = blocks[len(blocks) - 1]
        if next_block.start_time < top_block.end_time:
            top_block.end_time = next_block.end_time
        else:
            blocks.append(next_block)
    return blocks
