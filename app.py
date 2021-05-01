from events import Task, BusyBlock, TaskBlock
from scheduler import schedule
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

"""
purpose: Render our website pages.
"""
@app.route('/')
def home():
    return render_template('index.html')


"""
purpose: Run server.
"""
if __name__ == '__main__':
    app.run()
