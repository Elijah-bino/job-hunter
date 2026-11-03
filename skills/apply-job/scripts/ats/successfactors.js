// SAP SuccessFactors (career10.successfactors.com). Needs common.js.
// Comboboxes are <input id="NN:_input"> with a popup list. Setting .value alone does NOT stick;
// must open the popup and click the option. This does it without screenshots.
// pairs: [[labelRegex, optionRegex], ...]
window.sfCombo = async pairs => {
  const out = [];
  for (const [re, opt] of pairs) {
    const inp = qa('input[id$=":_input"]').find(x => re.test(labelOf(x)));
    if (!inp) { out.push('MISSING ' + re); continue; }
    inp.scrollIntoView({ block: 'center' });
    const btn = inp.parentElement.querySelector('button,[role=button],.sfDropDownButton') || inp.nextElementSibling;
    inp.focus(); inp.click(); if (btn) btn.click(); await sleep(700);
    const opts = qa('[role=option],li,div.listItem').filter(x => x.offsetParent && x.innerText && x.innerText.length < 200);
    const o = opts.find(x => opt.test(x.innerText.trim()));
    if (o) { o.dispatchEvent(new MouseEvent('mousedown', { bubbles: true })); o.click(); o.dispatchEvent(new MouseEvent('mouseup', { bubbles: true })); }
    await sleep(500); document.body.click(); await sleep(200);
    out.push(re + '=' + inp.value + (o ? '' : ' (NO OPTION; seen: ' + opts.slice(0, 8).map(x => x.innerText.trim().slice(0, 25)).join('/') + ')'));
  }
  return out;
};
// Text fields by label: reuse fillText from common.js.
// Verify: sfRequiredEmpty() lists starred fields still blank.
window.sfRequiredEmpty = () => qa('input,textarea').filter(e => /^\s*\*/.test(labelOf(e)) && !e.value).map(e => labelOf(e).replace(/\s+/g, ' ').slice(0, 60));
// Expand collapsed sections first or fields won't exist in innerText.
window.sfExpandAll = () => { const b = qa('button,a').find(x => /Expand all sections/i.test(x.innerText || x.getAttribute('aria-label') || '')); if (b) b.click(); return !!b; };
