(() => {
  'use strict';
  const data = window.VOYAGE;
  const root = document.documentElement;
  const $ = (s, scope = document) => scope.querySelector(s);
  const $$ = (s, scope = document) => [...scope.querySelectorAll(s)];
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const icon = name => `<svg aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const themes = {
    midnight: {name:'Midnight sea', title:'The Grand Line', subtitle:'Obsidian · Sea glass · Antique brass', chapter:'THE ORIGINAL VOYAGE', colors:['#0e1921','#85b6b3','#c4aa79']},
    dawn: {name:'Nika’s dawn', title:'Drums of Liberation', subtitle:'Parchment · Ivory · Warm bronze', chapter:'GEAR 05 / AWAKENING', colors:['#f0ebdf','#cdbba0','#7b522b']},
    wano: {name:'Wano dusk', title:'An Emperor’s Resolve', subtitle:'Ink violet · Sakura · Moonstone', chapter:'THE EMPEROR’S CHAPTER', colors:['#1b1724','#dba5aa','#b0a2d4']}
  };
  const readPreference = key => {try {return localStorage.getItem(key);} catch {return null;}};
  const savePreference = (key,value) => {try {localStorage.setItem(key,value);} catch { /* The voyage also works without storage. */ }};
  let theme = readPreference('mounesh-voyage-theme');
  if (!Object.hasOwn(themes,theme)) theme = 'midnight';
  let quiet = readPreference('mounesh-voyage-motion') === 'off' || matchMedia('(prefers-reduced-motion: reduce)').matches;
  let activePillar = 0;
  let toastTimer;
  const modal = $('#modal');
  function toast(message) {
    clearTimeout(toastTimer); $('#toast').textContent = message; $('#toast').classList.add('visible');
    toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 3000);
  }
  function themeCards() {
    return Object.entries(themes).map(([key,t]) => `<button class="theme-card" data-theme-choice="${key}" aria-pressed="${theme===key}" aria-label="Select ${escape(t.name)} theme"><div class="theme-preview ${key}"><span class="preview-chapter">${t.chapter}</span><span class="preview-word"><small>MOUNESH’S VOYAGE</small>${t.title}</span></div><div class="theme-info"><div><strong>${t.name}</strong><small>${t.subtitle}</small></div><span class="swatches" aria-hidden="true">${t.colors.map(c=>`<i style="background:${c}"></i>`).join('')}</span></div><div class="theme-selection"><span data-selection-label>${theme===key?'CURRENT ATMOSPHERE':'SAIL THESE WATERS'}</span><span data-selection-icon>${theme===key?'✓':'↗'}</span></div></button>`).join('');
  }
  function applyTheme(value,announce = true) {
    if (!Object.hasOwn(themes,value)) return;
    theme = value; root.dataset.theme = theme; savePreference('mounesh-voyage-theme',theme);
    $('#theme-label').textContent = themes[theme].name;
    $$('[data-theme-choice]').forEach(button => {const chosen=button.dataset.themeChoice===theme;button.setAttribute('aria-pressed',String(chosen));$('[data-selection-label]',button).textContent=chosen?'CURRENT ATMOSPHERE':'SAIL THESE WATERS';$('[data-selection-icon]',button).textContent=chosen?'✓':'↗';});
    if (announce) toast(`${themes[theme].name} selected. Your atmosphere is saved on this browser.`);
  }
  function applyMotion() {
    root.dataset.motion = quiet?'off':'on';
    $('#motion-toggle').setAttribute('aria-pressed',String(quiet));
    $('#motion-toggle').innerHTML = `Motion: ${quiet?'off':'on'} <span aria-hidden="true">${quiet?'○':'◉'}</span>`;
  }
  function chapter(index) {
    const c=data.chapters[index];
    $$('.chapter-tabs button').forEach((button,i)=>{button.setAttribute('aria-selected',String(i===index));button.tabIndex=i===index?0:-1;});
    const panel=$('#chapter-panel');panel.setAttribute('aria-labelledby',`chapter-${index}`);
    panel.innerHTML=`<p class="eyebrow">${c.date} / ${c.island.toUpperCase()}</p><h3>${c.title}</h3><p class="chapter-role">${c.role}</p><p class="chapter-copy">${c.text}</p><ul class="chapter-facts">${c.facts.map(f=>`<li>${f}</li>`).join('')}</ul><span class="chapter-number">Chapter 0${index+1} of 03</span>`;
    $('#map-ship').setAttribute('transform',`translate(${[[111,296],[316,230],[568,129]][index].join(' ')})`);
  }
  function projects(filter='All') {
    const list=data.projects.filter(p=>filter==='All'||p.category===filter);
    $('#project-grid').innerHTML=list.map(p=>`<article class="project-card"><div class="project-scene"><span class="vessel-no">VESSEL 0${data.projects.indexOf(p)+1}</span><svg class="vessel-icon" aria-hidden="true"><use href="#i-${p.icon}"/></svg><img src="assets/vessel-${p.id}.svg" alt="" loading="lazy" width="420" height="180"></div><div class="project-body"><p class="eyebrow">${p.sea}</p><h3>${p.name}</h3><p class="project-summary">${p.summary}</p><div class="tags">${p.stack.map(t=>`<span>${t}</span>`).join('')}</div><div class="project-bottom"><span class="project-status">${p.status}</span><button data-project="${p.id}" aria-label="Read the ${p.name} story">Read the log ${icon('external')}</button></div></div></article>`).join('');
    $('#fleet-count').textContent=`0${list.length} VESSEL${list.length===1?'':'S'} IN VIEW`;
    $$('[data-filter]').forEach(b=>{b.classList.toggle('active',b.dataset.filter===filter);b.setAttribute('aria-pressed',String(b.dataset.filter===filter));});
  }
  function pillar(index) {
    activePillar=index;const p=data.pillars[index];
    $$('[data-pillar]').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
    $('#pillar-detail').innerHTML=`<div><strong>${p.label}</strong><span>${p.stack}</span></div><p>${p.detail}</p>`;
  }
  function showModal(html) {
    $('#modal-content').innerHTML=html;
    if (!modal.open) modal.showModal();
    modal.scrollTop=0;
  }
  function openProject(id) {
    const p=data.projects.find(p=>p.id===id);if (!p) return;
    showModal(`<article class="case-study"><p class="modal-eyebrow">${p.sea}</p><h2 id="modal-title">${p.name}</h2><p>${p.status}</p><div class="tags">${p.stack.map(t=>`<span>${t}</span>`).join('')}</div><h3>The challenge</h3><p>${p.problem}</p><h3>What I built</h3><p>${p.build}</p><div class="case-flow" aria-label="System flow">${p.flow.map((s,i)=>`${i?'<b aria-hidden="true">→</b>':''}<span>${s}</span>`).join('')}</div><h3>The result</h3><p>${p.outcome}</p><p class="case-note">${p.note}</p></article>`);
  }
  function open(kind) {
    if (kind==='themes') showModal(`<p class="modal-eyebrow">CHOOSE YOUR WATERS</p><h2 id="modal-title">Find your atmosphere.</h2><p class="modal-description">The same real engineering story, seen through three One Piece worlds. Your choice carries into the profile export.</p><div class="theme-grid dialog-themes">${themeCards()}</div>`);
    if (kind==='readme') showModal(`<p class="modal-eyebrow">THE PROFILE / ${themes[theme].name.toUpperCase()}</p><h2 id="modal-title">Your flag on GitHub.</h2><p class="modal-description">A focused, readable profile with self-hosted art, real project stories, and the career behind the voyage.</p><div class="readme-actions"><a class="button primary" href="themes/${theme}.md" download="README.md">Download README ${icon('arrow')}</a><a class="button" href="profile-preview.html?theme=${theme}" target="_blank" rel="noopener">Open full preview ${icon('external')}</a></div><p class="readme-note">The download is designed for the root of this profile repository with its assets folder. GitHub renders the static profile; this gallery provides the interactive voyage.</p><iframe class="readme-frame" src="profile-preview.html?theme=${theme}" title="Static GitHub profile preview"></iframe>`);
    if (kind==='contact') showModal(`<p class="modal-eyebrow">INCOMING TRANSPONDER CONNECTION</p><h2 id="modal-title">Let’s build something<br>worth sailing for.</h2><p class="modal-description">Tell me what you’re building, where the hard part is, and what a good result would look like.</p><div class="contact-options"><a class="button primary" href="mailto:mounesh0711@gmail.com?subject=Let%E2%80%99s%20build%20something">Open email ${icon('arrow')}</a><a class="button" href="https://www.linkedin.com/in/mounesh-s-131a56273" target="_blank" rel="noopener noreferrer">LinkedIn ${icon('external')}</a><button class="button" id="copy-email">Copy email</button></div><p class="copy-status" id="copy-status" role="status">mounesh0711@gmail.com</p>`);
  }
  document.addEventListener('click',async event=>{
    const button=event.target.closest('button');if (!button) return;
    if (button.dataset.open) open(button.dataset.open);
    if (button.dataset.themeChoice) applyTheme(button.dataset.themeChoice);
    if (button.dataset.chapter!==undefined) chapter(Number(button.dataset.chapter));
    if (button.dataset.filter) projects(button.dataset.filter);
    if (button.dataset.project) openProject(button.dataset.project);
    if (button.dataset.pillar!==undefined) pillar(Number(button.dataset.pillar));
    if (button.classList.contains('close-modal')) modal.close();
    if (button.id==='motion-toggle') {quiet=!quiet;savePreference('mounesh-voyage-motion',quiet?'off':'on');applyMotion();}
    if (button.id==='copy-email') {
      try {await navigator.clipboard.writeText('mounesh0711@gmail.com');$('#copy-status').textContent='Email address copied.';}
      catch {$('#copy-status').textContent='Copy this address: mounesh0711@gmail.com';const selection=window.getSelection();const range=document.createRange();range.selectNodeContents($('#copy-status'));selection.removeAllRanges();selection.addRange(range);}
    }
  });
  $('.chapter-tabs').addEventListener('keydown',event=>{
    if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();let i=Number(document.activeElement.dataset.chapter);
    if (!Number.isInteger(i)) return;
    i=event.key==='Home'?0:event.key==='End'?2:(i+(event.key==='ArrowRight'?1:2))%3;
    chapter(i);$(`#chapter-${i}`).focus();
  });
  modal.addEventListener('click',event=>{if(event.target!==modal)return;const r=modal.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)modal.close();});
  $('#theme-gallery').innerHTML=themeCards();
  $('#pillar-grid').innerHTML=data.pillars.map((p,i)=>`<button class="pillar" data-pillar="${i}" aria-pressed="${i===activePillar}" aria-controls="pillar-detail"><div class="stone"><span class="glyph-text" aria-hidden="true">⊞⫶⊏⊡⌑⊢⊥⊞⊡⫶⊣⊏⊥⊡⊞⌑⊢⊏⫶⊣⊥⊡⊞⌑⊢⊏⫶⊣</span>${icon(p.icon)}<span class="stone-number">ROAD PONEGLYPH 0${i+1}</span></div><div class="pillar-label"><h3>${p.title}</h3><span aria-hidden="true">↗</span></div><p>${p.summary}</p></button>`).join('');
  applyTheme(theme,false);applyMotion();chapter(2);projects();pillar(0);
})();
