// Workday (myworkdayjobs.com). Needs common.js.
// Dropdown buttons: [[labelRegex, optionText], ...].
window.wdSelect = async pairs => {
  const out = [];
  for (const [re, v] of pairs) {
    const b = qa('button[aria-haspopup=listbox]').find(x => re.test(labelOf(x)) || re.test(x.id));
    if (!b) { out.push('MISSING ' + re); continue; }
    b.click(); await sleep(700);
    const o = qa('[role=listbox] [role=option]').filter(x => x.offsetParent).find(x => x.innerText.trim() === v || new RegExp('^' + v, 'i').test(x.innerText.trim()));
    if (o) o.click(); await sleep(500);
    out.push(re + '=' + b.innerText.trim());
  }
  return out;
};
// Multiselect prompt (e.g. "How did you hear"): type then Enter.
window.wdPrompt = async (re, text) => {
  const i = qa('input[placeholder="Search"],input[data-uxi-widget-type=selectinput]').find(x => re.test(labelOf(x)));
  if (!i) return 'MISSING ' + re;
  setText(i, text); i.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })); await sleep(800);
  const o = qa('[role=option]').filter(x => x.offsetParent)[0]; if (o) o.click(); return re + ' -> ' + (o ? o.innerText : 'none');
};
// Radios by question text: [[questionRegex, 'Yes'|'No'], ...]
window.wdRadio = pairs => pairs.map(([q, a]) => answerChoice(q, new RegExp('^' + a + '$', 'i')));
// Required fields still empty / error list
window.wdErrors = () => qa('[data-automation-id=errorMessage],[role=alert]').map(e => e.innerText.slice(0, 120));
