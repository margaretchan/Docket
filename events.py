import datetime

""" 
Task is an assignment or job which must be completed by a specific due date.
    name : string
    due : datetime.datetime
    expected_duration : datetime.time - the total time it is expected to take to 
      complete this task
    num_blocks : int - the amount of scheduled TaskBlocks this task will need to 
      be completed
    priority : int - higher number is higher priority
    released : datetime.datetime - the earliest time the user can begin working on the task
"""
class Task:
    def __init__(self, name, due, expected_duration, num_blocks, priority=0, 
                 start=datetime.datetime.now()):
        self.name = name
        self.due = due.replace(tzinfo=None)
        self.expected_duration = expected_duration
        self.num_blocks = num_blocks
        self.priority = priority
        self.start = start.replace(tzinfo=None)
        self.num_blocks_assigned = 0
        
    def __eq__(self, other):
        if (isinstance(other, Task)):
            return self.name == other.name and self.due == other.due and \
                self.expected_duration == other.expected_duration and \
                self.num_blocks == other.num_blocks and self.priority == other.priority and \
                self.start == other.start
        return False


""" 
BusyBlock is a block of time which is pre-allotted in the user's calendar and 
  should not be scheduled over.
    name : string
    start_time : datetime.datetime
    end_time : datetime.datetime
"""
class BusyBlock:
    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time.replace(tzinfo=None)
        self.end_time = end_time.replace(tzinfo=None)
    
    def __eq__(self, other):
        if (isinstance(other, BusyBlock)):
            return self.start_time == other.start_time and self.end_time == other.end_time
        return False


""" 
TaskBlock is a block of time which is scheduled for a specific task. 
    start_time : datetime.datetime
    end_time : datetime.datetime
    task : Task - the task which should be worked on in this time block
    task_block_num : int - the nth occourance of a time block to work on the 
      specified task
"""
class TaskBlock:
    def __init__(self, start_time, end_time, task, task_block_num):
        self.start_time = start_time
        self.end_time = end_time
        self.task = task
        self.task_block_num = task_block_num
        
    def __eq__(self, other):
        if (isinstance(other, TaskBlock)):
            return self.start_time == other.start_time and self.end_time == other.end_time and \
              self.task == other.task and self.task_block_num == other.task_block_num
        return False
    
    def __repr__(self):
        return "TaskBlock(start_time = " + self.start_time.strftime("%m/%d, %H:%M") + \
            ",\n\tend_time = " + self.end_time.strftime("%m/%d, %H:%M") + \
            ",\n\ttask = " + self.task.name + ",\n\ttask_block_num = " + str(self.task_block_num)
