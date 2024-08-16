import os
import html
from flask import Flask, render_template, request

app = Flask(__name__)

def load_alarms(file_paths):
    alarms = []
    categories = ["parameter=", "short=", "long=", "repair=", "context="]       #separators

    for file_path in file_paths:
        text = open(file_path, "r", encoding='utf-8')
        lines = text.readlines()
        new_lines = []                                      #loading all alarm files and removing unwanted character and empty spaces 
        for line in lines:
            new_lines.append(line.removesuffix('\n'))
            line = line.removesuffix('\n')

        s = ""
        new_text = s.join(new_lines).strip().strip("'").strip('"').split("¤")

        if len(new_text) == 8:
            alarm = {
                'Alarm ID' : new_text[0],
                'Alarm Information' : new_text[1],
                'Parameters' : new_text[2].split(categories[0])[1],
                'Internal Severity' : new_text[3],                          #removing separators and saving information to a dictionary
                'Explanation' : new_text[4].split(categories[1])[1],
                'Long Description' : new_text[5].split(categories[2])[1],
                'Troubleshooting' : new_text[6].split(categories[3])[1],
                'Context' : new_text[7].split(categories[4])[1],
            }
        alarms.append(alarm)
    return alarms

@app.route('/')
def index():
    file_paths = ['alarms1.txt', 'alarms2.txt', 'alarms3.txt']
    alarms = load_alarms(file_paths)
    
    severity_options = sorted(set(alarm['Internal Severity'] for alarm in alarms))
    severity_counts = {severity: sum(1 for alarm in alarms if alarm['Internal Severity'] == severity) for severity in severity_options}
    
    return render_template('alarms.html', alarms = alarms, severity_options=severity_options, severity_counts=severity_counts)

if __name__ == '__main__':
    app.run(debug=True)