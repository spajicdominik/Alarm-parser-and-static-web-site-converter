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
    
    style = '''
    <style>
        * {
            box-sizing: border-box;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            margin-top: 2%;
        }

        th, td {
            border: 1px solid black;
            text-align: left;
            padding: 15px;
            background-color: rgba(231, 253, 255, 0.2);
            color: #000000;
        }

        th {
            cursor: pointer;
            text-align: left;
        }

        thead th {
            background-color: #c9feff;
        }

        html {
            height: 100%;
            width: 100%;
            background-size: cover;
            background-image: radial-gradient(ellipse at top left, #a0a0a0, #ffffff);
        }

        tbody tr:hover {
            background-color: rgba(255,255,255,0.3);
        }

        tbody td {
            position: relative;
        }

        tbody td:hover:before {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            top: -9999px;
            bottom: -9999px;
            background-color: rgba(255,255,255,0.2);
            z-index: -1;
        }

        .stats {
            width: 50%;
        }
    </style>
    '''

    script = '''
    <script>
        function filterAlarms() {
  const idInput = document.getElementById("search-id").value.toLowerCase();
  const textInput = document.getElementById("search-text").value.toLowerCase();
  const severityFilter = document.getElementById("filter-severity").value;
  const rows = document.querySelectorAll("#alarms-table tr");

  rows.forEach((row) => {
    const cells = row.getElementsByTagName("td");
    const idMatch = cells[0].textContent.toLowerCase().includes(idInput);
    const textMatch = Array.from(cells).some((cell) =>
      cell.textContent.toLowerCase().includes(textInput)
    );
    const severityMatch =
      severityFilter === "All" || cells[3].textContent === severityFilter;
    row.style.display = idMatch && textMatch && severityMatch ? "" : "none";
  });
}

document.querySelectorAll(".context-link").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    const context = event.target.dataset.context;
    document.querySelectorAll("#alarms-table tr").forEach((row) => {
      const contextCell = row.getElementsByTagName("td")[7];
      row.style.display =
        contextCell && contextCell.textContent === context ? "" : "none";
    });
  });
});

function filterByContext(event) {
  event.preventDefault();

  const context = event.target.getAttribute('data-context');

  const rows = document.querySelectorAll('#alarms-table tr');

  rows.forEach(row => {
      const link = row.querySelector('.context-link');
      if (link) {
          const rowContext = link.getAttribute('data-context');
          if (rowContext === context) {
              row.style.display = ''; 
          } else {
              row.style.display = 'none';
          }
      }
  });
}
    </script>
    '''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Alarms</title>
        {style}
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
       {script}
    </body>
    </html>
    '''

    with open('alarms.html', 'w', encoding='utf-8') as f:
        f.write(html_content)


#Main script
file_paths = ['alarms1.txt']
alarms = load_alarms(file_paths)
generate_html(alarms)

