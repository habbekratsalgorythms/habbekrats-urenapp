const assert=require('assert'),fs=require('fs'),http=require('http'),path=require('path'),{spawnSync}=require('child_process');
const {chromium}=require('playwright-core');
const root=path.resolve(__dirname,'..');
const shots=path.join(root,'qa-screenshots');fs.mkdirSync(shots,{recursive:true});
const chrome=['google-chrome','google-chrome-stable','chromium','chromium-browser']
 .map(name=>spawnSync('which',[name],{encoding:'utf8'})).find(r=>r.status===0)?.stdout.trim();
assert(chrome,'Chrome/Chromium missing from CI runner');
const mimes={'.html':'text/html; charset=utf-8','.svg':'image/svg+xml','.js':'text/javascript','.css':'text/css'};
const server=http.createServer((req,res)=>{
 const requestPath=decodeURIComponent((req.url||'/').split('?')[0]);
 const target=path.resolve(root,'.'+requestPath);
 if(!target.startsWith(root+path.sep)&&target!==root){res.writeHead(403).end();return;}
 const file=fs.existsSync(target)&&fs.statSync(target).isDirectory()?path.join(target,'index.html'):target;
 if(!fs.existsSync(file)){res.writeHead(404).end();return;}
 res.writeHead(200,{'Content-Type':mimes[path.extname(file)]||'application/octet-stream'});
 fs.createReadStream(file).pipe(res);
});
const pages=['studio/index.html','offertecalculator/index.html','microservices/index.html',
'microservices/voorbeeldpakket.html','affiliate/index.html','affiliate/redactiebeleid.html',
'uren/index.html','klyptiq/index.html'];
async function run(){
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin='http://127.0.0.1:'+server.address().port+'/';
 const browser=await chromium.launch({executablePath:chrome,headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 for(const [size,width,height] of [['desktop',1366,900],['mobile',390,844]]){
  const context=await browser.newContext({viewport:{width,height},acceptDownloads:true});
  const page=await context.newPage();
  const pageErrors=[];page.on('pageerror',e=>pageErrors.push(String(e)));
  for(const pagePath of pages){
   pageErrors.length=0;
   await page.goto(origin+pagePath,{waitUntil:'domcontentloaded'});
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+5);
   assert(!overflow,'Horizontal overflow on '+size+' '+pagePath);
   assert(!pageErrors.length,'JavaScript error on '+pagePath+': '+pageErrors.join(' '));
   if(['offertecalculator/index.html','microservices/index.html','affiliate/index.html'].includes(pagePath)){
    await page.screenshot({path:path.join(shots,pagePath.replaceAll('/','_')+'_'+size+'.png'),fullPage:true});
   }
  }
  await page.goto(origin+'offertecalculator/index.html');
  assert((await page.locator('#price').innerText()).includes('69,27'),'Reference quote amount');
  await page.locator('#currentPrice').fill('75');
  assert((await page.locator('#actualMargin').innerText()).includes('30,73'),'Actual margin');
  const dlPromise=page.waitForEvent('download');
  await page.locator('#exportQuote').click();
  const download=await dlPromise;
  await download.saveAs(path.join(shots,'quote-'+size+'.csv'));
  assert(fs.readFileSync(path.join(shots,'quote-'+size+'.csv')).subarray(0,3).equals(Buffer.from([0xef,0xbb,0xbf])),'CSV BOM');
  await page.locator('#hours').fill('0');
  assert(await page.locator('#printQuote').isDisabled(),'Invalid quote print must be disabled');
  assert(await page.locator('#exportQuote').isDisabled(),'Invalid CSV must be disabled');
  await page.goto(origin+'microservices/index.html');
  await page.locator('#business').fill('Fictieve fietsenmaker');
  await page.locator('#audience').fill('Forenzen');
  await page.locator('#facts').fill('Geen garanties of ongecontroleerde claims');
  await page.locator('#brief button').click();
  assert((await page.locator('#result').innerText()).includes('Fictieve fietsenmaker'));
  assert((await page.locator('#mail').getAttribute('href')).startsWith('mailto:'));
  await page.goto(origin+'affiliate/index.html');
  await page.locator('#budget').fill('0');
  await page.locator('#check button').click();
  assert((await page.locator('#advice').innerText()).includes('gratis optie'));
  await context.close();
  console.log(size+' PASS: 8 pages, no overflow/JS errors, calculator and intake interactions');
 }
 }finally{await browser.close();}
}
run().then(()=>server.close()).catch(e=>{console.error(e);process.exitCode=1;server.close();});
