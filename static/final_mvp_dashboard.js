async function finalMvpStatus() {
  const box = document.getElementById('final-mvp-status');
  if (!box) return;
  try {
    const res = await fetch('/final/status');
    const data = await res.json();
    box.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    box.textContent = 'Final MVP status unavailable: ' + e;
  }
}

async function runFinalCycle() {
  const out = document.getElementById('final-mvp-output');
  out.textContent = 'Running autonomous dry-run cycle...';
  const res = await fetch('/final/autonomous/cycle', { method: 'POST' });
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
  finalMvpStatus();
}

async function startFinalWorker() {
  const out = document.getElementById('final-mvp-output');
  const res = await fetch('/final/autonomous/start', { method: 'POST' });
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
  finalMvpStatus();
}

async function stopFinalWorker() {
  const out = document.getElementById('final-mvp-output');
  const res = await fetch('/final/autonomous/stop', { method: 'POST' });
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
  finalMvpStatus();
}

window.addEventListener('load', finalMvpStatus);
