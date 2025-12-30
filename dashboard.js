async function loadBrains() {
  const res = await fetch('_brain_index.json');
  const data = await res.json();

  const grid = document.getElementById('grid');
  const updated = document.getElementById('last-updated');

  updated.textContent = `Last scan: ${data.generated}`;

  data.brains.forEach(brain => {
    const div = document.createElement('div');
    div.classList.add('brain');

    if (brain.status === 'healthy') div.classList.add('healthy');
    else if (brain.status === 'not-a-repo') div.classList.add('broken');
    else div.classList.add('dirty');

    div.innerHTML = `
      <h2>${brain.name}</h2>
      <small>${brain.branch || 'no-branch'}</small><br>
      <small>${brain.status}</small>
    `;

    div.onclick = () => {
      alert(`Brain: ${brain.name}\nStatus: ${brain.status}\nPath: ${brain.path}`);
    };

    grid.appendChild(div);
  });
}

loadBrains();
