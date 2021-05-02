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
assignment_names=[]

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
    session['start_day_string'] = request.form['start_day']
    session['end_day'] = int(request.form['end_day'].split(":", 1)[0])
    session['end_day_string'] = request.form['end_day']

    session['break'] = int(request.form['break'])
    session['finish_hours'] = int(request.form['finish_hours'])
    
    events = populateCalendar()
    dates = getStartEndDates() 

    session['events'] = events
    session['index'] = 0

    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events = events, dates = dates, index = 0, assignments = assignments, assignment_names=assignment_names)

@app.route('/home')
def home():
    events = populateCalendar()
    dates = getStartEndDates() 
    session['events'] = events
    session['index'] = 0

    return render_template('index.html', start_hour = 1, end_hour= 24, events = events, dates = dates, index = 0, assignments = assignments, assignment_names=assignment_names)

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
    start_time = datetime.strptime(str(session['start_day'])+ ":00", '%H:%M').time()
    end_time = datetime.strptime(str(session['end_day'])+ ":00", '%H:%M').time()
    leeway = timedelta(hours = session['finish_hours'])
    breaks = timedelta(minutes = session['break'])

    
    busy_blocks = populateBusyBlocks()
    task = Task(name, deadline, timedelta(hours = hours), blocks, priority, start)

    task_blocks = schedule([task], busy_blocks, start_time, end_time, leeway, breaks )
    new_events = addTaskToEvent(task_blocks, session['events'])
    dates = getStartEndDates() 
    new_assign = {
        "name": name,
        "blocks": blocks,
        "priority": priority,
        "deadline": deadline,
        "hours": hours
    }
    assignments.append(new_assign)
    assignment_names.append(name)
    print(assignment_names)
    print(new_assign['name'])
    print(new_assign['name']in assignment_names)

    session['events']=new_events
    index= session['index']

    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events =  new_events, dates = dates, index = index, assignments = assignments, assignment_names=assignment_names)


@app.route('/nextpage', methods=['GET', 'POST'])
def nextPage():
    events = session['events']
    session['index'] = session['index'] + 7
    dates = getStartEndDates()
    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events =  events, dates = dates, index = session['index'], assignments = assignments, assignment_names=assignment_names)

@app.route('/backpage', methods=['GET', 'POST'])
def backPage():
    events = session['events']
    dates = getStartEndDates()
    session['index'] = session['index'] - 7
    return render_template('index.html', start_hour = session['start_day'], end_hour= session['end_day'], events =  events, dates = dates, index = session['index'], assignments = assignments, assignment_names=assignment_names)


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
