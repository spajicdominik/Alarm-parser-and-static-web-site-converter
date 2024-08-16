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