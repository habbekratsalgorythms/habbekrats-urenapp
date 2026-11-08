
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path');const root=path.resolve(__dirname,'..');const pages=Object.fromEntries(['index.html','offertecalculator/index.html','studio/index.html','microservices/index.html','klyptiq/index.html','affiliate/index.html','affiliate/redactiebeleid.html','uren/index.html','microservices/voorbeeldpakket.html'].map(p=>[p,fs.readFileSync(path.join(root,p),'utf8')]));
let checks=[];
for(const [path,html] of Object.entries(pages)){
 assert(html.startsWith('<!doctype html>'),path);
 for(const match of html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)){
  let script=match[1].replace(/^import .*;$/m,'');
  new vm.Script(script,{filename:path});checks.push(path+' syntax OK');
 }
}
function dom(){const elements={};return {elements,getElementById(id){return elements[id]||=( {value:'',textContent:'',disabled:false,hidden:true,children:[],addEventListener(type,fn){this[type]=fn},checkValidity(){return true},replaceChildren(){this.children=[]},append(...c){this.children.push(...c)}})},body:{appendChild(){}},createElement(){return {textContent:'',children:[],append(...c){this.children.push(...c)},click(){},remove(){}}}}}
assert(pages['microservices/voorbeeldpakket.html'].match(/POST 0[1-9]|POST 10/g).length===10,'Need 10 actual sample posts');
assert(pages['microservices/index.html'].includes('href="voorbeeldpakket.html"'),'Need public sample link');
assert(pages['affiliate/index.html'].includes('href="redactiebeleid.html"'),'Need editorial policy link');
assert(pages['affiliate/redactiebeleid.html'].includes('geen actieve affiliate-links'),'No fabricated commission claims');
checks.push('Content service: 10 complete distinct sample posts and affiliate disclosure page linked');
const script=pages['offertecalculator/index.html'].match(/<script>([\s\S]*?)<\/script>/)[1];
const d=dom();const vals={hours:'2',visits:'1',labor:'24',travel:'1.95',material:'2',margin:'25',vat:'21'};
for(const [id,v] of Object.entries(vals))d.getElementById(id).value=v;
let exportedBlob;const c=vm.createContext({document:d,URL:{createObjectURL(b){exportedBlob=b;return 'blob:offline-test'},revokeObjectURL(){}},Blob:class{constructor(parts){this.parts=parts}}});vm.runInContext(script,c);
assert(d.getElementById('price').textContent.includes('69,27'));
assert(d.getElementById('incl').textContent.includes('83,81'));
assert(d.getElementById('scenario15').textContent.includes('61,12'));
assert(d.getElementById('scenario35').textContent.includes('79,92'));
assert(d.getElementById('yearProfit').textContent.includes('900,47'));
d.getElementById('currentPrice').value='75';vm.runInContext('recalc()',c);
assert(d.getElementById('actualMargin').textContent.includes('30,73%'));
vm.runInContext('exportQuoteCsv()',c);assert(exportedBlob.parts[0].includes('annualProfit'));assert(exportedBlob.parts[0].startsWith('\uFEFF'));
d.getElementById('currentPrice').value='-1';vm.runInContext('recalc()',c);assert(d.getElementById('exportQuote').disabled);
d.getElementById('currentPrice').value='';vm.runInContext('recalc()',c);
d.getElementById('labor').value='';vm.runInContext('recalc()',c);assert(d.getElementById('printQuote').disabled);
d.getElementById('labor').value='24';d.getElementById('margin').value='100';vm.runInContext('recalc()',c);assert(d.getElementById('printQuote').disabled);
d.getElementById('margin').value='25';d.getElementById('hours').value='0';vm.runInContext('recalc()',c);assert(d.getElementById('printQuote').disabled);
checks.push('Calculator: reference amounts, 3 scenarios, current margin, annual profit, offline CSV, invalid input OK');
// Regression: selecting another customer must change visible records, monthly totals and CSV.
{
 const app=pages['index.html'];
 const statsCode=app.slice(app.indexOf('function selectedEntries(){'),app.indexOf("$('exportCsv').onclick"));
 const listCode=app.slice(app.indexOf('function renderEntries(){'),app.indexOf("$('save').onclick=async()=>{"));
 const csvCode=app.slice(app.indexOf("$('exportCsv').onclick"),app.indexOf("async function loadReviews(){"));
 assert(statsCode.includes("x.client_id===client"),"Per-client totals must explicitly filter client_id");
 assert(listCode.includes("entry.client_id===chosenClient"),"Per-client records must filter client_id");
 let csvBlob;const nodes={};
 const element=()=>({value:'',textContent:'',children:[],selectedOptions:[],append(...children){this.children.push(...children)},replaceChildren(){this.children=[]},querySelector(){return {textContent:'Client '+nodes.client.value}},click(){},remove(){}});
 for(const id of ['client','month','monthTotal','entries','exportCsv'])nodes[id]=element();
 nodes.client.value='a';nodes.client.selectedOptions=[{textContent:'Alpha'}];nodes.month.value='2026-11';
 const records=[
  {id:'row-a',client_id:'a',work_date:'2026-11-05',start_time:'09:00',end_time:'10:00',person_count:1,total_person_minutes:60,status:'approved'},
  {id:'row-b',client_id:'b',work_date:'2026-11-06',start_time:'13:00',end_time:'15:00',person_count:1,total_person_minutes:120,status:'approved'}
 ];
 const testDoc={createElement:()=>element(),body:{appendChild(){}}};
 const sandbox=vm.createContext({entryCache:records,$:id=>nodes[id],document:testDoc,
  statusLabels:{approved:'Goedgekeurd'},URL:{createObjectURL(b){csvBlob=b;return 'blob:test'},revokeObjectURL(){}},
  Blob:class{constructor(parts){this.parts=parts}}});
 vm.runInContext(statsCode+'\n'+listCode+'\n'+csvCode,sandbox);
 vm.runInContext('updateStats();renderEntries();',sandbox);
 assert.equal(nodes.entries.children.length,1);
 assert(nodes.entries.children[0].children[0].textContent.includes('Client a'));
 assert(nodes.monthTotal.textContent.startsWith('1'));
 vm.runInContext("$('exportCsv').onclick()",sandbox);
 assert(csvBlob.parts[0].includes('Alpha')&&!csvBlob.parts[0].includes('Beta'));
 nodes.client.value='b';nodes.client.selectedOptions=[{textContent:'Beta'}];
 vm.runInContext('updateStats();renderEntries();',sandbox);
 assert.equal(nodes.entries.children.length,1);
 assert(nodes.entries.children[0].children[0].textContent.includes('Client b'));
 assert(nodes.monthTotal.textContent.startsWith('2'));
 vm.runInContext("$('exportCsv').onclick()",sandbox);
 assert(csvBlob.parts[0].includes('Beta')&&!csvBlob.parts[0].includes('Alpha'));
 checks.push('Hours: per-customer tabs isolate records, monthly totals and CSV exports');
}
for(const path of ['microservices/index.html','affiliate/index.html']){
 const d=dom();const ctx=vm.createContext({document:d,encodeURIComponent});
 vm.runInContext(pages[path].match(/<script>([\s\S]*?)<\/script>/)[1],ctx);
 if(path.startsWith('microservices')){
  for(const id of ['business','audience','facts'])d.getElementById(id).value='<script>example</script>';
  d.getElementById('goal').value='Offertes';d.getElementById('tone').value='Helder';
  d.getElementById('brief').submit({preventDefault(){}});
  assert(d.getElementById('result').textContent.includes('<script>example</script>'));
  assert(d.getElementById('mail').href.startsWith('mailto:habbekratsalgorythms@gmail.com?'));
 }else{
  d.getElementById('budget').value='0';d.getElementById('data').selectedIndex=1;d.getElementById('task').value='Video';
  d.getElementById('check').submit({preventDefault(){}});
  const text=d.getElementById('advice').children[1].children.map(x=>x.textContent).join(' ');
  assert(text.includes('gratis optie'));assert(text.includes('bewaart'));
 }
 checks.push(path+' interaction OK');
}
const app=pages['index.html'];
const pager=app.slice(app.indexOf('async function loadEntries(){'),app.indexOf('entryCache=all;')+'entryCache=all;'.length)+'return entryCache;}';
const rows=Array.from({length:1001},(_,i)=>({id:i}));let requested=[],filters=[];
const chain={select(){return this},eq(k,v){filters.push([k,v]);return this},order(){return this},async range(a,b){requested.push([a,b]);return {data:rows.slice(a,b+1),error:null}}};
const context=vm.createContext({db:{from(){return chain}},org:{id:'org'},user:{id:'person'},$:()=>({disabled:false}),err:e=>{throw e}});
vm.runInContext(pager,context);context.loadEntries().then(result=>{
 assert.equal(result.length,1001);assert.equal(requested.length,3);
 assert(filters.some(([k,v])=>k==='user_id'&&v==='person'));
 checks.push('Hours: 1001 rows across 3 pages, personal filter OK');
 console.log(JSON.stringify(checks,null,2));
}).catch(e=>{console.error(e);process.exitCode=1});
