from events import Task, BusyBlock, TaskBlock
from scheduler import schedule
from quickstart import populateCalendar, getStartEndDates, populateBusyBlocks, addTaskToEvent
from flask import Flask, render_template, request, redirect, jsonify, session
from datetime import datetime, timedelta, time

app = Flask(__name__)
app.secret_key = "any random string"

temp_assign = {
    "name": "INFO 3300 project",
    "blocks": 3,
    "priority": "High",
    "deadline": "5/5/2021",
    "hours": 4
}
assignments = []

"""
purpose: Render our website pages.
"""

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/main', methods = ['POST'])
def main():
    print(request.form['start_day'])
    session['start_day'] = int(request.form['start_day'].split(":", 1)[0])
    session['end_day'] = int(request.form['end_day'].split(":", 1)[0])
    session['break'] = int(request.form['break'])
    finish_hours = int(request.form['finish_hours'])
    
    events = populateCalendar()
    dates = getStartEndDates() 

    session['events'] = events
    session['index'] = 0

    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events = events, dates = dates, index = 0, assignments = assignments)

@app.route('/home')
def home():
    events = populateCalendar()
    dates = getStartEndDates() 
    session['events'] = events
    session['index'] = 0

    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events = events, dates = dates, index = 0, assignments = assignments)

#add in backend algorithm
@app.route('/addAssignment', methods = ['POST'])
def addAssignment():
    events = session['events']
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
    session['events']=new_events
    index= session['index']


    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events =  new_events, dates = dates, index = index, assignments = assignments)


@app.route('/nextpage', methods=['GET', 'POST'])
def nextPage():
    events = session['events']
    session['index'] = session['index'] + 7
    dates = getStartEndDates()
    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events =  events, dates = dates, index = session['index'], assignments = assignments)

@app.route('/backpage', methods=['GET', 'POST'])
def backPage():
    events = session['events']
    dates = getStartEndDates()
    session['index'] = session['index'] - 7
    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events =  events, dates = dates, index = session['index'], assignments = assignments)


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
