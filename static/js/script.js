document.addEventListener("DOMContentLoaded", function () {
    var socket = io.connect(window.location.origin);

    socket.on('connect', function() {
        console.log('Connected to server via WebSocket');
    });

    socket.on('file_change', function(data) {
        console.log('File change detected, refreshing the page...');
        location.reload(); 
    });


    socket.on('update_alarms', function (data) {
        console.log('Received update_alarms event', data);  
        const alarms = data.alarms;
        const alarmsTable = document.getElementById('alarms-table');
        alarmsTable.innerHTML = '';  

        alarms.forEach(function(alarm) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${alarm["Alarm ID"]}</td>
                <td>${alarm["Alarm Information"]}</td>
                <td>${alarm["Parameters"]}</td>
                <td>${alarm["Internal Severity"]}</td>
                <td>${alarm["Explanation"]}</td>
                <td>${alarm["Long Description"]}</td>
                <td>${alarm["Troubleshooting"]}</td>
                <td><a href="#" class="context-link" data-context="${alarm["Context"]}" onclick="filterByContext(event)">${alarm["Context"]}</a></td>
            `;
            alarmsTable.appendChild(row);
        });
    });
});

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