import os
import html
from flask import Flask, render_template, request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time

app = Flask(__name__)

data_folder = 'data'

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

alarms_data = []

def update_alarms_data():
    global alarms_data
    file_paths = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.txt')]
    alarms_data = load_alarms(file_paths)
    print(file_paths)
    
class Watcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.txt'):
            update_alarms_data()
            
    def on_created(self, event):
        self.on_modified(event)
        
    def on_deleted(self, event):
        self.on_modified(event)
        
def start_observer():
    observer = Observer()
    event_handler = Watcher()
    observer.schedule(event_handler, path=data_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    

@app.route('/')
def index():
    global alarms_data

    severity_options = sorted(set(alarm['Internal Severity'] for alarm in alarms_data))
    severity_counts = {severity: sum(1 for alarm in alarms_data if alarm['Internal Severity'] == severity) for severity in severity_options}
    
    return render_template('alarms.html', alarms = alarms_data, severity_options=severity_options, severity_counts=severity_counts)

if __name__ == '__main__':
    update_alarms_data()
    observer_thread = threading.Thread(target=start_observer, daemon=True)
    observer_thread.start()
    app.run(debug=True)