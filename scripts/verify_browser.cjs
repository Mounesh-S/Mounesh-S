const {chromium}=require('playwright');
const {default:AxeBuilder}=require('@axe-core/playwright');
const {spawn}=require('node:child_process');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const output=path.join(root,'test-results');
fs.mkdirSync(output,{recursive:true});
const port=Number(process.env.TEST_PORT||4187);
const base=`http://127.0.0.1:${port}`;
const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1'],{cwd:root,stdio:'ignore'});
let browser;
const checks=[];
const check=(label)=>{checks.push(label);console.log('PASS '+label);};
async function settleImages(page){await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(img=>{img.loading='eager';return img.decode().catch(()=>{});})));}
async function axe(page,label){const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();fs.writeFileSync(path.join(output,`axe-${label}.json`),JSON.stringify(result.violations,null,2));assert.equal(result.violations.length,0,`${label} accessibility: ${result.violations.map(v=>v.id+' '+v.nodes.map(n=>n.target.join(' ')).join(', ')).join('\n')}`);}
(async()=>{
  for(let i=0;i<50;i++){try{if((await fetch(base)).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
  const executablePath=process.env.CHROME_PATH||(fs.existsSync('/usr/bin/google-chrome')?'/usr/bin/google-chrome':undefined);
  browser=await chromium.launch({executablePath,headless:true,args:['--no-sandbox']});
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  const page=await context.newPage();const errors=[],badResponses=[],external=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)badResponses.push(`${r.status()} ${r.url()}`);});page.on('request',r=>{if(!r.url().startsWith(base)&&!r.url().startsWith('data:'))external.push(r.url());});
  await page.goto(base,{waitUntil:'networkidle'});await settleImages(page);
  assert.equal(await page.locator('h1').innerText(),'Mounesh S.');assert.equal(await page.locator('.project-card').count(),6);
  assert.equal(await page.locator('.profession').count(),1);check('Initial profile and six evidence-backed projects');
  for(const [filter,count] of [['AI & Product',2],['Systems',2],['Full Stack',1],['Research',1],['All',6]]){await page.locator(`[data-filter="${filter}"]`).click();assert.equal(await page.locator('.project-card').count(),count);}
  check('Every project filter returns the correct vessels');
  for(const id of ['routing','pulse','onboarding','streaming','billing','anomaly']){await page.locator(`[data-project="${id}"]`).click();assert(await page.locator('#modal').isVisible());assert(await page.locator('.case-flow').isVisible());await page.keyboard.press('Escape');assert(!(await page.locator('#modal').isVisible()));}
  check('All six project logs open and close with Escape');
  await page.locator('#chapter-0').click();assert((await page.locator('#chapter-panel').innerText()).includes('B.Tech'));await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#chapter-1').getAttribute('aria-selected'),'true');assert((await page.locator('#chapter-panel').innerText()).includes('Intern'));await page.keyboard.press('End');assert.equal(await page.locator('#chapter-2').getAttribute('aria-selected'),'true');check('Career tabs update content and support arrow / End keys');
  for(let i=0;i<4;i++){await page.locator(`[data-pillar="${i}"]`).click();assert.equal(await page.locator(`[data-pillar="${i}"]`).getAttribute('aria-pressed'),'true');assert((await page.locator('#pillar-detail').innerText()).length>80);}check('All four Poneglyphs reveal their engineering detail');
  for(const theme of ['midnight','dawn','wano']){
    await page.locator(`#theme-gallery [data-theme-choice="${theme}"]`).click();assert.equal(await page.locator('html').getAttribute('data-theme'),theme);await page.reload({waitUntil:'networkidle'});assert.equal(await page.locator('html').getAttribute('data-theme'),theme);await settleImages(page);
    await axe(page,theme);
    await page.evaluate(()=>{document.activeElement?.blur();window.scrollTo(0,0);});
    await page.screenshot({path:path.join(output,`${theme}-desktop.png`),fullPage:true});
    for(const width of [768,390,320]){await page.setViewportSize({width,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${theme} overflow at ${width}`);if(width===390){await page.screenshot({path:path.join(output,`${theme}-mobile.png`),fullPage:true});}}
    await page.setViewportSize({width:1440,height:1000});
  }
  check('Three themes persist, pass accessibility checks, and fit 1440 / 768 / 390 / 320px');
  await page.locator('[data-open="themes"]').click();await axe(page,'theme-dialog');await page.locator('#modal [data-theme-choice="midnight"]').click();await page.locator('.close-modal').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'midnight');check('Header theme chooser applies selection');
  await page.locator('.hero [data-open="readme"]').click();await page.frameLocator('.readme-frame').locator('h1').waitFor();const downloadPromise=page.waitForEvent('download');await page.getByRole('link',{name:'Download README'}).click();const download=await downloadPromise;assert.equal(download.suggestedFilename(),'README.md');await download.saveAs(path.join(output,'downloaded-README.md'));assert(fs.readFileSync(path.join(output,'downloaded-README.md'),'utf8').includes('assets/banner-midnight.svg'));await axe(page,'readme-dialog');await page.keyboard.press('Escape');check('Static profile preview and real Markdown download');
  await page.locator('[data-open="contact"]').click();assert.equal(await page.locator('#modal a').first().getAttribute('href'),'mailto:mounesh0711@gmail.com?subject=Let%E2%80%99s%20build%20something');await context.grantPermissions(['clipboard-read','clipboard-write']);await page.locator('#copy-email').click();assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'mounesh0711@gmail.com');await axe(page,'contact-dialog');await page.keyboard.press('Escape');check('Contact destinations and email copy');
  await page.locator('#motion-toggle').click();assert.equal(await page.locator('html').getAttribute('data-motion'),'off');await page.reload();assert.equal(await page.locator('html').getAttribute('data-motion'),'off');check('Motion switch and persistence');
  const reduced=await browser.newPage({reducedMotion:'reduce'});await reduced.goto(base);assert.equal(await reduced.locator('html').getAttribute('data-motion'),'off');await reduced.close();check('Operating-system reduced-motion preference');
  const nested=await context.newPage();await nested.route('**/portfolio/**',async route=>{const url=route.request().url().replace('/portfolio/','/');const response=await route.fetch({url});await route.fulfill({response});});await nested.goto(base+'/portfolio/index.html');await settleImages(nested);assert.equal(await nested.locator('.project-card').count(),6);assert(await nested.locator('img').evaluateAll(imgs=>imgs.every(i=>i.naturalWidth>0)));await nested.close();check('Repository-subpath compatibility for GitHub Pages');
  await page.goto(base+'/profile-preview.html?theme=dawn',{waitUntil:'networkidle'});await axe(page,'static-profile');assert.equal(await page.locator('html').getAttribute('data-theme'),'dawn');await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));check('Static README preview accessibility and mobile layout');
  assert.deepEqual(errors,[]);assert.deepEqual(badResponses,[]);assert.deepEqual(external,[]);check('No browser errors, failed assets, or external runtime requests');
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({checks,errors,badResponses,external},null,2));
  console.log(`\n${checks.length} browser checks passed. Screenshots and accessibility reports: test-results/`);
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();server.kill();});
