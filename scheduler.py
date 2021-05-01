from events import Task, BusyBlock, TaskBlock
from quickstart import populateBusyBlocks
import datetime import datetime, time, timedelta

"""
schedule() will use a modified version of the Earliest Deadline First (EDF)
    algorithm to schedule blocks of time to complete all tasks by their 
    deadlines while avoiding scheduling over pre-existing busy blocks of time.
    Returns a list of TaskBlocks.
tasks : Task list
busy_blocks : BusyBlock list, sorted in time increasing order
day_start_time : datetime.time
day_end_time : datetime.time
buffer : datetime.timedelta - amount of time before the deadline a task should 
    be completed by
"""
def schedule(tasks, busy_blocks, day_start_time, day_end_time, buffer):
    task_blocks = []
    # sort by descending priority
    sorted_tasks = sorted(tasks, key=lambda task: task.priority, reverse=True) 
    
    for task in sorted_tasks:
        schedule_with_latest_endtime(task, task.end_time - buffer)
        
    for task in sorted_tasks:
        if (task.num_blocks_assigned < task.num_blocks):
            schedule_with_latest_endtime(task, )
    
    return []

"""
schedule_with_latest_endtime() attempts to schedule 1 block of the task at the 
    latest possible timeslot so that the latest end_time is endtime. Returns 
    an object of type TaskBlock.
task : Task - the task to be scheduled
endtime : datetime.datetime - the latest possible endtime
"""
def schedule_with_latest_endtime(task, endtime):
    return [TaskBlock()]
