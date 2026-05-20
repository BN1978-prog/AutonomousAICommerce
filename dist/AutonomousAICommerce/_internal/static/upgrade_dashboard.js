async function loadUpgradeStatus() {
  try {
    const res = await fetch('/upgrade/status');
    const data = await res.json();
    console.log('Upgrade status', data);
  } catch (e) {
    console.warn('Upgrade status unavailable', e);
  }
}
loadUpgradeStatus();
