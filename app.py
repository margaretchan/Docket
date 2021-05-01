from events import Task, BusyBlock, TaskBlock
from scheduler import schedule
from quickstart import populateCalendar, getStartEndDates
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

"""
purpose: Render our website pages.
"""
@app.route('/')
def home():
    events = populateCalendar()
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events =events, dates = dates, index = 0)

@app.route('/nextpage<index>', methods=['GET', 'POST'])
def nextPage(index):
    events = populateCalendar()
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events = events, dates = dates, index = int(index) + 7)

@app.route('/backpage<index>', methods=['GET', 'POST'])
def backPage(index):
    events = populateCalendar()
    dates = getStartEndDates()
    return render_template('index.html', start_hour = 8, end_hour= 24, events = events, dates = dates, index = int(index) - 7)


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
