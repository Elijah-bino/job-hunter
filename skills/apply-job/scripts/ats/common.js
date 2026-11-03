// Shared helpers. Paste before site scripts.
window.sleep = ms => new Promise(r => setTimeout(r, ms));
window.roots = () => { const R = [document]; const walk = r => r.querySelectorAll('*').forEach(e => { if (e.shadowRoot) { R.push(e.shadowRoot); walk(e.shadowRoot); } }); walk(document); return R; };
window.qa = sel => roots().flatMap(r => [...r.querySelectorAll(sel)]);
window.labelOf = e => {
  if (e.labels && e.labels[0]) return e.labels[0].innerText;
  const by = e.getAttribute('aria-labelledby'); if (by) { const l = document.getElementById(by.split(' ')[0]); if (l) return l.innerText; }
  if (e.getAttribute('aria-label')) return e.getAttribute('aria-label');
  let p = e; for (let i = 0; i < 6 && p; i++) { p = p.parentElement; const l = p && p.querySelector('label,legend'); if (l) return l.innerText; }
  return e.placeholder || e.name || '';
};
window.setText = (e, v) => {
  const proto = e.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : e.tagName === 'SELECT' ? HTMLSelectElement.prototype : HTMLInputElement.prototype;
  e.focus(); Object.getOwnPropertyDescriptor(proto, 'value').set.call(e, v);
  ['input', 'change'].forEach(t => e.dispatchEvent(new Event(t, { bubbles: true }))); e.blur(); return e.value;
};
window.selectByText = (sel, re) => { const o = [...sel.options].find(x => re.test(x.text.trim())); if (!o) return null; return setText(sel, o.value) && o.text; };
// Compact field list: idx|tag|type|id|label|value
window.dump = () => qa('input:not([type=hidden]):not([type=checkbox][id*=cookie]),textarea,select,button[aria-haspopup=listbox]')
  .map((e, i) => [i, e.tagName[0], e.type || '', e.id || e.name || '', labelOf(e).replace(/\s+/g, ' ').slice(0, 60),
    (e.type === 'radio' || e.type === 'checkbox') ? e.checked : (e.value || e.innerText || '').slice(0, 30)].join('|')).join('\n');
// Fill text-like fields by label regex: [[/First Name/i,'Alex'], ...]
window.fillText = pairs => pairs.map(([re, v]) => {
  const e = qa('input[type=text],input[type=email],input[type=tel],input:not([type]),textarea').find(x => re.test(labelOf(x)));
  return e ? re + '=' + setText(e, v) : 'MISSING ' + re;
});
// Click radio/checkbox label inside the group whose text matches question regex.
window.answerChoice = (qRe, aRe) => {
  const g = qa('fieldset,[role=radiogroup],[role=group]').find(x => qRe.test(x.innerText));
  if (!g) return 'NOQ ' + qRe;
  const sel = g.querySelector('select'); if (sel) return 'sel ' + selectByText(sel, aRe);
  const l = [...g.querySelectorAll('label')].find(x => aRe.test(x.innerText.trim()));
  if (!l) return 'NOA ' + aRe;
  const inp = l.control || l.querySelector('input'); if (!inp || !inp.checked) l.click(); return 'ok ' + l.innerText.trim().slice(0, 40);
};
