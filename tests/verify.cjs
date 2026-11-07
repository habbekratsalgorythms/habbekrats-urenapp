
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path');const root=path.resolve(__dirname,'..');const pages=Object.fromEntries(['index.html','offertecalculator/index.html','studio/index.html','microservices/index.html','klyptiq/index.html','affiliate/index.html','uren/index.html'].map(p=>[p,fs.readFileSync(path.join(root,p),'utf8')]));
let checks=[];
for(const [path,html] of Object.entries(pages)){
 assert(html.startsWith('<!doctype html>'),path);
 for(const match of html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)){
  let script=match[1].replace(/^import .*;$/m,'');
  new vm.Script(script,{filename:path});checks.push(path+' syntax OK');
 }
}
function dom(){const elements={};return {elements,getElementById(id){return elements[id]||=( {value:'',textContent:'',disabled:false,hidden:true,children:[],addEventListener(type,fn){this[type]=fn},checkValidity(){return true},replaceChildren(){this.children=[]},append(...c){this.children.push(...c)}})},createElement(){return {textContent:'',children:[],append(...c){this.children.push(...c)}}}}}
const script=pages['offertecalculator/index.html'].match(/<script>([\s\S]*?)<\/script>/)[1];
const d=dom();const vals={hours:'2',visits:'1',labor:'24',travel:'1.95',material:'2',margin:'25',vat:'21'};
for(const [id,v] of Object.entries(vals))d.getElementById(id).value=v;
const c=vm.createContext({document:d});vm.runInContext(script,c);
assert(d.getElementById('price').textContent.includes('69,27'));
assert(d.getElementById('incl').textContent.includes('83,81'));
d.getElementById('labor').value='';vm.runInContext('recalc()',c);assert(d.getElementById('printQuote').disabled);
d.getElementById('labor').value='24';d.getElementById('margin').value='100';vm.runInContext('recalc()',c);assert(d.getElementById('printQuote').disabled);
d.getElementById('margin').value='25';d.getElementById('hours').value='0';vm.runInContext('recalc()',c);assert(d.getElementById('printQuote').disabled);
checks.push('Calculator: reference amounts, blank, 100% margin, zero hours OK');
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
