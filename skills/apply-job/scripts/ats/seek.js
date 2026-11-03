// SEEK "Answer employer questions" step. Needs common.js.
// pairs: [[questionRegex, answerRegex], ...]. Handles radios, checkboxes, and <select>.
window.seekAnswer = async pairs => {
  const out = [];
  for (const [q, a] of pairs) {
    let r = answerChoice(q, a);
    if (r.startsWith('NOQ')) { // question may be a bare <select> with a label
      const s = qa('select').find(x => q.test(labelOf(x)));
      r = s ? 'sel ' + selectByText(s, a) : r;
    }
    out.push(r); await sleep(150);
  }
  return out;
};
// Unanswered required questions (for verify step)
window.seekUnanswered = () => qa('fieldset').filter(f => !f.querySelector('input:checked') && !(f.querySelector('select') && f.querySelector('select').selectedIndex > 0)).map(f => f.innerText.split('\n')[0].slice(0, 80));
// Selects often sit outside fieldsets with aria-labelledby.
window.seekSelect = pairs => pairs.map(([q, a]) => {
  const lab = e => (e.labels && e.labels[0] ? e.labels[0].innerText : (e.getAttribute('aria-labelledby') || '').split(' ').map(x => document.getElementById(x)?.innerText || '').join(' '));
  const s = [...document.querySelectorAll('select')].find(s => q.test(lab(s))); if (!s) return 'NOSEL ' + q;
  return selectByText(s, a) || 'NOA ' + q;
});
// Checkboxes by label text (multi-select questions)
window.seekChecks = re => [...document.querySelectorAll('input[type=checkbox]')].filter(b => re.test((b.labels && b.labels[0] ? b.labels[0].innerText : '').trim()) && !b.checked).map(b => (b.click(), b.labels[0].innerText.trim()));
