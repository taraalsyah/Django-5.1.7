console.log('SCRIPT LOADED');




document.addEventListener('DOMContentLoaded', () => {
    updateTicketStatus();
});


// Function to fetch and update ticket counts
function updateTicketStatus() {

    fetch('/ticket/get_ticket_status/')  // Replace with your actual URL

        .then(response => response.json())
        .then(data => {
            document.getElementById('percentopen').textContent = data.openpercent;
            document.getElementById('percentinprogress').textContent = data.inProgresspercent;
            document.getElementById('percentclosed').textContent = data.closedpercent;
            document.getElementById('total_count').textContent = data.total_count;

        })
        .catch(error => console.error('Error fetching ticket status:', error));
};
