#!/bin/python

## PART 1 - Read the YAML File
# script to read the information from the queue config yaml file

# import libraries

import yaml
import subprocess
import os
import pprint
import sqlite3


pp = pprint.PrettyPrinter(indent=4)

# read data from the config file
def read_yaml(file):
    with open(file, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print("\n")
    return config

data = read_yaml("queue.yaml")


## PART 2 - SQLITE3 database

# establish connection to sqlite database and save into db
conn = sqlite3.connect('queues.db')
c = conn.cursor()

# create a sqlite3 database to store the dictionary values
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS queues(job TEXT, team TEXT, problem TEXT, CPU INT, memory TEXT)")

create_table()

# insert data into the tab

def dynamic_data_entry():
    c.executemany("INSERT INTO queues (job, team, problem, CPU, memory) VALUES (:jobname, :team, :problem, :CPU, :memory);", data)
    conn.commit()

dynamic_data_entry()

def query_db():
    c.execute('SELECT * FROM queues GROUP BY job, team')
    data = c.fetchall()
    return data

queues_data = query_db()
print(type(queues_data))

## PART 3 - Flask App for display

from flask import Flask, g, render_template
app = Flask(__name__)

# index page for displaying a table with the db contents
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', data=queues_data)

if __name__ == '__main__':
    app.run(debug=True)

c.close()
conn.close()
