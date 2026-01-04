document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const detail = document.getElementById(btn.dataset.target);
      const isOpen = detail.classList.contains("is-open");

      detail.classList.toggle("is-open");
      btn.textContent = isOpen ? "Show" : "Hide";
    });
  });
});

function confirmStatusChange(ticketId, statusText) {
  return confirm(
    "Are you sure you want to change Ticket ID: " +
    ticketId +
    " to status: " +
    statusText +
    "?"
  );
}

const STATUS_CODE = {
  open: 1,
  'in-progress': 2,
  closed: 3
};

function updateDropdownRules(dropdown, currentStatus) {
    const items = dropdown.querySelectorAll('.status-item');
    items.forEach(item => {
      const targetStatus = item.dataset.status;
      let disabled = false;
      if (currentStatus === 'open') {
        disabled = targetStatus === 'open'  || targetStatus === 'closed';
      }
      if (currentStatus === 'in-progress') {
        disabled = targetStatus === 'open' || targetStatus === 'in-progress';
      }
      if (currentStatus === 'closed') {
        disabled = true;
      }
      item.classList.toggle('disabled', disabled);
      item.style.pointerEvents = disabled ? 'none' : 'auto';
      item.style.opacity = disabled ? '0.5' : '1';
    });
    dropdown.dataset.currentStatus = currentStatus;
  }

document.addEventListener('DOMContentLoaded', () => {
  // INIT status saat page load
  document.querySelectorAll('.status-dropdown').forEach(dropdown => {
    const statusInit = dropdown.dataset.status;
    applyStatus(dropdown, statusInit);
    updateDropdownRules(dropdown, statusInit);

  });
});


// toggle dropdown
function toggleDropdown(btn) {
  const menu = btn.nextElementSibling;

  document.querySelectorAll('.status-menu').forEach(m => {
    if (m !== menu) m.style.display = 'none';
  });

  menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

function setLoading(dropdown, isLoading) {
  const btn = dropdown.querySelector('.status-btn');

  if (isLoading) {
    btn.dataset.oldText = btn.innerText;
    console.log('Old text:', btn.dataset.oldText, isLoading);
    btn.innerText = 'Loading...';
    btn.disabled = true;
  } else {
    btn.innerText = btn.dataset.oldText;
    btn.disabled = false;
  }
}

window.showToast = function (message, type = 'success', duration = 3000) {
  const toast = document.getElementById('toast');
  if (!toast) return;

  toast.textContent = message;
  toast.className = `toast show ${type}`;

  setTimeout(() => {
    toast.classList.remove('show');
  }, duration);
};

function getCSRFToken() {
  let cookieValue = null;
  const name = 'csrftoken';

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
  }


// klik option
function setStatus(item) {
  if (item.classList.contains('disabled')) {
    return; // ⛔ stop total
  }
  console.log('Clicked status item', item);
  const statusText = item.innerText;
  const status = item.dataset.status;
  console.log('Clicked status status', status);
  const dropdown = item.closest('.status-dropdown');
  console.log('Clicked status dropdown', dropdown);
  const ticketId = dropdown.dataset.ticketId;
  console.log('Clicked status ticketId', ticketId);
  const statusCode = STATUS_CODE[status];
  console.log('AwaticketIdl:', ticketId,status,statusCode);
  
  function initializeStatusDropdowns() {
  document.querySelectorAll('.status-dropdown').forEach(dropdown => {
    const ticketId = dropdown.dataset.ticketId;
    console.log('Initializing dropdown for ticket ID:', ticketId);
    if (!dropdown.dataset.listenerAttached) {
      dropdown.addEventListener('click', e => {
        const item = e.target.closest('[data-status]');
        if (!item) return;

        const status = item.dataset.status;
        const currentStatus = dropdown.dataset.status;



        console.log('Clicked status:', status, 'Current status:', currentStatus);

        if ((currentStatus === 'open' || currentStatus === 'in-progress') && status === 'closed') {
          const confirmClose = confirm(
            'Ticket akan ditutup. Lanjutkan ke form penyelesaian?'
          );
          if (!confirmClose) return;

          window.location.href = `/ticket/history/${ticketId}`;
          return;
        }

        // update dataset supaya log berikutnya akurat
        dropdown.dataset.status = status;
      });

      dropdown.dataset.listenerAttached = "true";
    }
  });
}


// panggil setelah DOM siap

  initializeStatusDropdowns();



  // CONFIRM
  if (!confirmStatusChange(ticketId, statusText)) {
    dropdown.querySelector('.status-menu').style.display = 'none';
    return;
  }


  applyStatus(dropdown, status);
  dropdown.querySelector('.status-menu').style.display = 'none';


  if (dropdown.dataset.loading === 'true') return;
  dropdown.dataset.loading = 'true';

  function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

  // 🔥 START LOADING
  setLoading(dropdown, true);

  // TODO: fetch update ke backend
  console.log('Status changed to:', status);


  // kirim ke backend
  const updateRequest = fetch('/ticket/update/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({
      ticket_id: ticketId,
      status_code: statusCode
    })
  });

  Promise.all([
    updateRequest,
    sleep(2000) // ⏱️ MINIMUM 5 DETIK
  ])

  .then(([response]) => response.json())
  .then(data => {
    if (data.success) {
      applyStatus(dropdown, status);
      formatStatusIndex(status);
      updateDropdownRules(dropdown, status);
      showToast('Status updated successfully to ' + status, 'success');
    } else {
      applyStatus(dropdown, prevStatus);
      formatStatusIndex(status);
      showToast('Failed to update status', 'error');
      console.error('Error updating status:', data.error);
    }
  })
  .catch(() => {
    console.error('Network or server error');
    showToast('Server error', 'error');
  })
  .finally(() => {
  console.log('Finalizing status update');
  setTimeout(() => {
    setLoading(dropdown, false);
    dropdown.dataset.loading = 'false';
  });
  });
}




// apply UI status (dipakai ulang)
function applyStatus(dropdown, status) {
  const btn = dropdown.querySelector('.status-btn');
  btn.className = 'status-btn ' + status;
  btn.innerText = formatStatus(status) + ' ▼';
}

// helper text
function formatStatus(status) {
  if (status === 'in-progress') return 'In Progress';
  return status.charAt(0).toUpperCase() + status.slice(1);
}

// close dropdown on outside click
document.addEventListener('click', e => {
    if (!e.target.closest('.status-dropdown')) {
    document.querySelectorAll('.status-menu')
          .forEach(m => m.style.display = 'none');
  }
});


document.querySelectorAll('.history-item').forEach(htn => {
  const statusLabel = htn.querySelectorAll('.label');

  statusLabel.forEach(item => {
    const status = item.dataset.status;
    const dataTicketId = item.dataset.ticketid;
    console.log('History item status:', status);
    console.log('History item ticket ID:', dataTicketId);
    if (status === 'closed') {
      item.innerHTML = 'Status: Closed';
    } else if (status === 'in-progress') {
      item.innerHTML = 'Status: in-progress';
    } else if (status === 'open') {
      item.innerHTML = 'Status: open';
    }
  });
});


// update status index display after change
const showStatusIndex = document.getElementById('showStatusIndex');
console.log('Show Status Index Element:', showStatusIndex.dataset.ticketId, showStatusIndex.dataset.status);


function formatStatusIndex(status) {
  const IndexStatusShow = document.querySelector('.IndexStatusShow');
  IndexStatusShow.innerText = formatStatus(status);
}




// BLOCK CONFIRM DELETE TICKET //
function confirmDelete(ticketId) {
    return confirm("Are you sure you want to delete Ticket ID: " + ticketId + "?");
};
// ENDBLOCK CONFIRM DELETE TICKET //