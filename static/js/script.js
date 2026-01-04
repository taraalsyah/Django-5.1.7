document.addEventListener('DOMContentLoaded', () => {
  const sidebars = document.getElementById('sidebarid');
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const topbar = document.getElementById('topbar');

  // pastikan elemen ada sebelum akses classList
  if (!sidebars || !hamburgerBtn || !topbar) return;

  // Load saved state
  const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  if (collapsed) {
    sidebars.classList.add('collapsed');
    topbar.classList.add('collapsed');
  }

  // Toggle and save state
  hamburgerBtn.addEventListener('click', () => {
    sidebars.classList.toggle('collapsed');
    topbar.classList.toggle('collapsed');
    const isCollapsed = sidebars.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', isCollapsed);
  });

  
  
});


function confirmDelete(ticketId) {
    return confirm("Are you sure you want to delete Ticket ID: " + ticketId + "?");
};


// DASHBOARD CHART
const canvas = document.getElementById('statusChart');
const ctx = canvas.getContext('2d');
  
function getLegendPercent() {
  const result = {};

  document.querySelectorAll('.legend-item').forEach(item => {
    const status = item.dataset.status;      // open | progress | closed
    const value = Number(item.dataset.value);
    result[status] = value;
  });
  
  console.log('Legend Data:', result);
  return result;
}




const chartConfig = {
  radius: 110,        // ukuran chart
  innerRadius: 60,    // 0 = pie, >0 = donut
  data: [
    {
      label: 'Open',
      percent: 0,           // ⬅️ UBAH PERSEN DI SINI
      color: '#ef4444'
    },
    {
      label: 'In Progress',
      percent: 0,
      color: '#f59e0b'
    },
    {
      label: 'Closed',
      percent: 0,
      color: '#22c55e'
    }
  ]
};

const legendData = getLegendPercent();

chartConfig.data.forEach(item => {
  const key =
    item.label === 'Open' ? 'open' :
    item.label === 'In Progress' ? 'progress' :
    'closed';

  item.percent = legendData[key] ?? 0;
  console.log(`Set percent for ${item.label}:`, item.percent);
});

console.log(chartConfig.data);

function drawChart(config) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const cx = canvas.width / 2;
  const cy = canvas.height / 2;

  let startAngle = -Math.PI / 2; // start from top

  config.data.forEach(item => {
    const sliceAngle = (item.percent / 100) * Math.PI * 2;

    // outer slice
    ctx.beginPath();
    ctx.arc(cx, cy, config.radius, startAngle, startAngle + sliceAngle);
    ctx.arc(cx, cy, config.innerRadius, startAngle + sliceAngle, startAngle, true);
    ctx.closePath();

    ctx.fillStyle = item.color;
    ctx.fill();

    // text inside slice
    const midAngle = startAngle + sliceAngle / 2;
    const textX = cx + Math.cos(midAngle) * ((config.radius + config.innerRadius) / 2);
    const textY = cy + Math.sin(midAngle) * ((config.radius + config.innerRadius) / 2);

    ctx.fillStyle = '#fff';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`${item.percent}%`, textX, textY);

    startAngle += sliceAngle;
  });
}

// render
drawChart(chartConfig);
