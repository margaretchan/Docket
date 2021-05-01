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
    print(events[0][0]['start_day'])
    print(dates[0])
    return render_template('index.html', start_hour = 8, end_hour= 24, events =events, dates = dates)


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
