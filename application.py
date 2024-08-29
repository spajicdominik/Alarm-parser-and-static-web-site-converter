import os
import html

def clean_field(field):
    field = field.strip().strip('"').strip("'")
    prefixes = ["parameter=", "short=", "long=", "repair=", "context="]
    for prefix in prefixes:
        if field.startswith(prefix):
            field = field[len(prefix):]
    return html.escape(field)

def load_alarms(file_paths):
    alarms = []

    for file_path in file_paths:
        text = open(file_path, "r", encoding='utf-8')
        lines = text.readlines()
        for line in lines[1:]:
            fields = line.split('¤')
            if len(fields) < 8:
                    continue
            alarm = {
                    'Alarm ID': clean_field(fields[0]),
                    'Alarm Information': clean_field(fields[1]),
                    'Parameters': clean_field(fields[2]),
                    'Internal Severity': clean_field(fields[3]),
                    'Explanation': clean_field(fields[4]),
                    'Long Description': clean_field(fields[5]),
                    'Troubleshooting': clean_field(fields[6]),
                    'Context': clean_field(fields[7])
                }
            alarms.append(alarm)
    return alarms


def generate_html(alarms):
    severity_options = set(alarm['Internal Severity'] for alarm in alarms)
    severity_options_html = '\n'.join(f'<option value="{severity}">{severity}</option>' for severity in sorted(severity_options))

    alarms_html = ''
    for alarm in alarms:
        context = alarm['Context']
        context_html = f'<a href="#" class="context-link" data-context="{context}" onclick="filterByContext(event)">{context}</a>'

        alarms_html += f'''
        <tr>
            <td>{(alarm["Alarm ID"])}</td>
            <td>{alarm["Alarm Information"]}</td>
            <td>{alarm["Parameters"]}</td>
            <td>{alarm["Internal Severity"]}</td>
            <td>{alarm["Explanation"]}</td>
            <td>{alarm["Long Description"]}</td>
            <td>{alarm["Troubleshooting"]}</td>
            <td>{context_html}</td>
        </tr>
        '''
                                     
    total_alarms = len(alarms)
    severity_counts = {severity: sum(1 for alarm in alarms if alarm['Internal Severity'] == severity) for severity in severity_options}

    stats_html = f'''
    <table class="stats" id="stats-table">
        <thead>
            <tr>
                <th>Severity</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Total alarms</td>
                <td>{total_alarms}</td>
            </tr>
    '''
    for severity, count in severity_counts.items():
        stats_html += f'''
            <tr>
                <td>{severity}</td>
                <td>{count}</td>
            </tr>
        '''
    stats_html += '''
        </tbody>
    </table>
    '''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Alarms</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <h1>Alarms</h1>
        <p>Here is the list of all alarms.</p>
        <label for="search-id">Search by Alarm ID:</label>
        <input type="text" id="search-id" onkeyup="filterAlarms()">
        <label for="search-text">Search by text:</label>
        <input type="text" id="search-text" onkeyup="filterAlarms()">
        <label for="filter-severity">Filter by Severity:</label>
        <select id="filter-severity" onchange="filterAlarms()">
            <option value="All">All</option>
            {severity_options_html}
        </select>
        <table>
            <thead>
                <tr>
                    <th>Alarm ID</th>
                    <th>Alarm Information</th>
                    <th>Parameters</th>
                    <th>Internal Severity</th>
                    <th>Explanation</th>
                    <th>Long Description</th>
                    <th>Troubleshooting</th>
                    <th>Context</th>
                </tr>
            </thead>
            <tbody id="alarms-table">
                {alarms_html}
            </tbody>
        </table>
        <div id="stats">
            {stats_html}
        </div>
        <script src="script.js"></script>
    </body>
    </html>
    '''

    with open('alarms.html', 'w', encoding='utf-8') as f:
        f.write(html_content)


#Main script
file_paths = ['alarms1.txt']
alarms = load_alarms(file_paths)
generate_html(alarms)

