document.addEventListener("DOMContentLoaded", () => {
  const toast = sessionStorage.getItem('toast');

  if (toast) {
    const { message, type } = JSON.parse(toast);
    showToast(message, type);
    sessionStorage.removeItem('toast');
  }
<<<<<<< HEAD
  initializeStatusDropdowns()

  document.querySelectorAll(".toggle-btn").forEach(btn => {
  const detail = document.getElementById(btn.dataset.target);
  const icon = btn.querySelector(".toggle-icon");

  const isOpen = detail.classList.contains("is-open");

  icon.src = isOpen
    ? "/static/ticket/img/up-arrow.svg"
    : "/static/ticket/img/down-arrow.svg";

  icon.alt = isOpen ? "hide" : "show";

  btn.addEventListener("click", () => {
    const open = detail.classList.toggle("is-open");

    icon.src = open
      ? "/static/ticket/img/up-arrow.svg"
      : "/static/ticket/img/down-arrow.svg";

    icon.alt = open ? "hide" : "show";
  });
});


=======




  document.querySelectorAll(".toggle-btn").forEach(btn => {
    const detail = document.getElementById(btn.dataset.target);
    const icon = btn.querySelector(".toggle-icon");

    const isOpen = detail.classList.contains("is-open");

    icon.src = isOpen
      ? "/static/ticket/img/up-arrow.svg"
      : "/static/ticket/img/down-arrow.svg";

    icon.alt = isOpen ? "hide" : "show";

    btn.addEventListener("click", () => {
      const open = detail.classList.toggle("is-open");

      icon.src = open
        ? "/static/ticket/img/up-arrow.svg"
        : "/static/ticket/img/down-arrow.svg";

      icon.alt = open ? "hide" : "show";
    });
  });
>>>>>>> banyak
  ChangeColor();

  setTimeout(() => {
    const msg = document.getElementById('flash-message');
    if (msg) {
      msg.classList.add('fade');
      setTimeout(() => msg.remove(), 500);
    }
  }, 500);
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
      disabled = targetStatus === 'open' || targetStatus === 'closed';
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




window.showToast = function (message, type = 'success', duration = 500) {
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

function handleStatusChange(item) {
  const statusText = item.innerText;
  const status = item.dataset.status;
  const dropdown = item.closest('.status-dropdown');
  const ticketId = dropdown.dataset.ticketId;
  const statusCode = STATUS_CODE[status];

  // CONFIRM
  if (!confirmStatusChange(ticketId, statusText)) {
    dropdown.querySelector('.status-menu').style.display = 'none';
    return false;
  }

  console.log('Status handleStatusChange= ', status);
  if (status === 'closed') {
    console.log('Masuk status === closed');



    // Kirim update status ke server dengan AJAX/fetch

    fetch('/ticket/update/', {
      method: 'POST',
      body: JSON.stringify({ status: 'closed' }),  // Kirim status baru
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({
        ticket_id: ticketId,
        status_code: statusCode
      })
    })

      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showToast(`Ticket ${data.ticket_id} Successfully Update to ${data.status}`, 'success');
          setTimeout(() => {
            const nextUrl = encodeURIComponent(window.location.pathname + window.location.search);
            window.location.href = `/ticket/history/${ticketId}?next=${nextUrl}`;
          }, 500);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showToast('Error updating status', 'error');
      });
  } else {
    setStatus(item);  // Pastikan status diperbarui jika tidak 'closed'
  }


  return false; // Kalau button ada di form, ini penting
}



// klik option
function setStatus(item) {
  if (item.classList.contains('disabled')) {
    return; // ⛔ stop total
  }
  console.log('Clicked status item', item);
  const statusText = item.innerText;
  const status = item.dataset.status;
  console.log('Status yang di click', status);
  const dropdown = item.closest('.status-dropdown');
  console.log('Clicked status dropdown', dropdown);
  const ticketId = dropdown.dataset.ticketId;
  console.log('Clicked status ticketId', ticketId);
  const statusCode = STATUS_CODE[status];
  console.log('AwaticketIdl:', ticketId, status, statusCode);


  const row = item.closest('tr');
  console.log('Row', row)
  const statusEl = row.querySelector('.IndexStatusShow');


  applyStatus(dropdown, status);
  dropdown.querySelector('.status-menu').style.display = 'none';


  if (dropdown.dataset.loading === 'true') return;
  dropdown.dataset.loading = 'true';

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }



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
  const prevStatus = dropdown.dataset.status;

  Promise.all([
    updateRequest,
    sleep(500)
  ])

    .then(([response]) => {
      if (!response.ok) throw response;
      return response.json();
    })


    .then(data => {
      if (data.success) {
        applyStatus(dropdown, status);
        formatStatusIndex(statusEl, status);
        updateDropdownRules(dropdown, status);
        showToast(`Ticket ${data.ticket_id} Successfully Update to ${data.status}`, 'success');


      } else {
        applyStatus(dropdown, prevStatus);
        formatStatusIndex(statusEl, status);
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
        dropdown.dataset.loading = 'true';
      });
    });


}






// apply UI status (dipakai ulang)
function applyStatus(dropdown, status) {
  const btn = dropdown.querySelector('.status-btn');
  btn.className = 'status-btn ' + status;
<<<<<<< HEAD
  
=======

>>>>>>> banyak
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
function formatStatusIndex(statusEl, status) {
  const formattedStatus = formatStatus(status);

  statusEl.innerText = formattedStatus;

  statusEl.classList.remove('open', 'in-progress', 'closed');

  if (status === 'open') {
    statusEl.classList.add('open');
  } else if (status === 'in-progress') {
    statusEl.classList.add('in-progress');
  } else if (status === 'closed') {
    statusEl.classList.add('closed');
  }
}


function ChangeColor() {
  document.querySelectorAll('.IndexStatusShow').forEach(el => {
    const status = el.dataset.status;
    console.log('Masuk Change COlor=', status)
    console.log('Masuk Change ALL=', el)
    el.classList.remove('open', 'in-progress', 'closed');

    if (status === 'open') {
      el.classList.add('open');
    } else if (status === 'in-progress') {
      el.classList.add('in-progress');
    } else if (status === 'closed') {
      el.classList.add('closed');
    }
  });

}



// BLOCK CONFIRM DELETE TICKET //
function confirmDelete(ticketId) {
  return confirm("Are you sure you want to delete Ticket ID: " + ticketId + "?");
};
// ENDBLOCK CONFIRM DELETE TICKET //


function cancelAndBack() {
  window.history.back();
}




// BLOCK delete ticket //
document.addEventListener('submit', function (e) {
  const form = e.target.closest('.button-delete');
  if (!form) return;

  e.preventDefault(); // ⛔ STOP submit normal

  const ticketId = form.dataset.ticketId;
  const url = form.dataset.url;


  if (!confirm(`Delete ticket ${ticketId}?`)) return;

  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // HAPUS ROW / CARD dari DOM
        form.closest('tr')?.remove();
        // atau
        // form.closest('.ticket-card')?.remove();
        showToast(`Data Success Delete ${data.id_ticket}`, 'success');
        console.log('Ticket deleted, page stays', data.id_ticket);

      }
    });
});

// ENDBLOCK delete ticket //
