import os
import html

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


def generate_html(alarms):              #function for generating HTML code based on the input alarms
    severity_options = set(alarm['Internal Severity'] for alarm in alarms)
    severity_options_html = '\n'.join(f'<option value="{severity}">{severity}</option>' for severity in sorted(severity_options))   #generating option elements for a severity menu

    alarms_html = ''
    for alarm in alarms:
        context = alarm['Context']
        context_html = f'<a href="#" class="context-link" data-context="{html.escape(context)}">{context}</a>'      #hyperlink for displaying alarms with corresponding context - !!!WORK IN PROGRESS!!!!

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
        #generating a table row with the alarm specifications for each alarm and adding it to our HTML code
                                     
    total_alarms = len(alarms)
    severity_counts = {severity: sum(1 for alarm in alarms if alarm['Internal Severity'] == severity) for severity in severity_options}     #total number of alarms and severities 

    stats_html = f'<p>Total alarms: {total_alarms}</p>'
    for severity, count in severity_counts.items():         #generating HTML code displaying the number of alarms and number of severities respectively
        stats_html += f'<p>{severity}: {count}</p>'

    #GENERATING FULL HTML CONTENT
    
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Alarms</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            th {{
                cursor: pointer;
            }}
        </style>
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
        <script>
            function filterAlarms() {{
                const idInput = document.getElementById('search-id').value.toLowerCase();  
                const textInput = document.getElementById('search-text').value.toLowerCase();
                const severityFilter = document.getElementById('filter-severity').value;
                const rows = document.querySelectorAll('#alarms-table tr');

                rows.forEach(row => {{
                    const cells = row.getElementsByTagName('td');
                    const idMatch = cells[0].textContent.toLowerCase().includes(idInput);
                    const textMatch = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(textInput));
                    const severityMatch = severityFilter === 'All' || cells[3].textContent === severityFilter;
                    row.style.display = idMatch && textMatch && severityMatch ? '' : 'none';
                }});
            }}

            document.querySelectorAll('.context-link').forEach(link => {{
                link.addEventListener('click', event => {{
                    event.preventDefault();
                    const context = event.target.dataset.context;
                    document.querySelectorAll('#alarms-table tr').forEach(row => {{
                        const contextCell = row.getElementsByTagName('td')[7];
                        row.style.display = contextCell && contextCell.textContent === context ? '' : 'none';
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    '''

    with open('alarms.html', 'w', encoding='utf-8') as f:       #creating and writing a HTML file
        f.write(html_content)

#Main script
file_paths = ['alarms1.txt', 'alarms2.txt']
alarms = load_alarms(file_paths)
generate_html(alarms)

