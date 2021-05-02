from events import Task, BusyBlock, TaskBlock
from scheduler import schedule
from quickstart import populateCalendar, getStartEndDates, populateBusyBlocks, addTaskToEvent
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime, timedelta, time

app = Flask(__name__)
temp_assign = {
    "name": "INFO 3300 project",
    "blocks": 3,
    "priority": "High",
    "deadline": "5/5/2021",
    "hours": 4
}
assignments = []
global_events = populateCalendar()

"""
purpose: Render our website pages.
"""

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    dates = getStartEndDates()  
    return render_template('index.html', start_hour = 8, end_hour= 24, events = global_events, dates = dates, index = 0, assignments = [temp_assign])

#add in backend algorithm
@app.route('/addAssignment', methods = ['POST'])
def addAssignment():
    name = request.form['name']
    deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M')
    start = datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M')
    priority = int(request.form['priority'])
    blocks = int(request.form['blocks'])
    hours = int(request.form['hours'])
    
    busy_blocks = populateBusyBlocks()
    task = Task(name, deadline, timedelta(hours = hours), blocks, priority, start)

    task_blocks = schedule([task], busy_blocks)
    new_events = addTaskToEvent(task_blocks, global_events)
    dates = getStartEndDates() 
    new_assign = {
        "name": name,
        "blocks": blocks,
        "priority": priority,
        "deadline": deadline,
        "hours": hours
    }
    assignments.append(new_assign)
    print(new_events[6])
    global_events = new_events

    return render_template('index.html', start_hour = 8, end_hour= 24, events =  global_events, dates = dates, index = 0, assignments = assignments)


@app.route('/nextpage<index>', methods=['GET', 'POST'])
def nextPage(index):
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events =  global_events, dates = dates, index = int(index) + 7, assignments = assignments)

@app.route('/backpage<index>', methods=['GET', 'POST'])
def backPage(index):
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events =  global_events, dates = dates, index = int(index) - 7, assignments = assignments)


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
