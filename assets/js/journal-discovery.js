/* All cards remain HTML anchors; pagination is a progressive enhancement. */
(() => {
  const input = document.getElementById('journal-search');
  const more = document.getElementById('journal-more');
  const count = document.getElementById('journal-count');
  const cards = [...document.querySelectorAll('#latest .cards a.card')];
  if (!input || !more || !count || !cards.length) return;
  const batch = 24;
  let limit = batch;
  const terms = cards.map(card => card.textContent.toLocaleLowerCase('en'));
  function render() {
    const query = input.value.trim().toLocaleLowerCase('en');
    const matches = cards.filter((card, index) => terms[index].includes(query));
    const shown = new Set(matches.slice(0, limit));
    cards.forEach(card => { card.hidden = !shown.has(card); });
    more.hidden = matches.length <= limit;
    count.textContent = matches.length ? `Showing ${Math.min(limit, matches.length)} of ${matches.length} articles` : 'No matching articles';
  }
  input.addEventListener('input', () => { limit = batch; render(); });
  more.addEventListener('click', () => { limit += batch; render(); });
  render();
})();
