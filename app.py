from events import Task, BusyBlock, TaskBlock
from scheduler import schedule
from quickstart import populateCalendar, getStartEndDates
from flask import Flask, render_template, request, redirect, jsonify


app = Flask(__name__)
temp_assign = {
    "name": "INFO 3300 project",
    "blocks": 3,
    "priority": "High",
    "deadline": "5/5/2021",
    "hours": 4
}
assignments = [temp_assign]

"""
purpose: Render our website pages.
"""

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    events = populateCalendar()
    dates = getStartEndDates()  

    return render_template('index.html', start_hour = 8, end_hour= 24, events =events, dates = dates, index = 0, assignments = [temp_assign])

#add in backend algorithm
@app.route('/addAssignment', methods = ['POST'])
def addAssignment():
    name = request.form['name']
    deadline = request.form['deadline']
    start = request.form['start']
    priority = request.form['priority']
    blocks = request.form['blocks']
    hours = request.form['hours']

    #pass this info to backend algorithm
    #backend algorithm will return new schedule of events
    #events need to be in the form of a list of lists where each index is day of week (0 = Monday, 6 =Sunday)
    events = populateCalendar()
    dates = getStartEndDates() 
    new_assign = {
        "name": name,
        "blocks": blocks,
        "priority": priority,
        "deadline": deadline,
        "hours": hours
    }
    assignments.append(new_assign)

    return render_template('index.html', start_hour = 8, end_hour= 24, events =events, dates = dates, index = 0, assignments = assignments)


@app.route('/nextpage<index>', methods=['GET', 'POST'])
def nextPage(index):
    events = populateCalendar()
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events = events, dates = dates, index = int(index) + 7, assignments = assignments)

@app.route('/backpage<index>', methods=['GET', 'POST'])
def backPage(index):
    events = populateCalendar()
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events = events, dates = dates, index = int(index) - 7, assignments = assignments)


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
