const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const dirs=['.','studio','uren','offertecalculator','microservices','affiliate','klyptiq'];
let checked=0, links=0;
for(const dir of dirs){
 const fullDir=path.join(root,dir);
 if(!fs.existsSync(fullDir))continue;
 for(const file of fs.readdirSync(fullDir).filter(x=>x.endsWith('.html'))){
  const page=path.join(fullDir,file),html=fs.readFileSync(page,'utf8');checked++;
  assert(/^<!doctype html>/i.test(html),page+': missing doctype');
  assert(/<html[^>]+lang="nl"/i.test(html),page+': missing Dutch locale');
  assert(/<meta[^>]+name="viewport"/i.test(html),page+': missing mobile viewport');
  for(const match of html.matchAll(/(?:href|src)="([^"]*)"/g)){
   const link=match[1].trim();
   if(!link||link==='#')continue;
   if(/^(?:https?:|mailto:|tel:|data:|blob:|#)/i.test(link))continue;
   assert(!/^(?:javascript:|file:)/i.test(link),page+': disallowed URL');
   const without=decodeURIComponent(link.split(/[?#]/)[0]);
   if(!without)continue;
   const destination=path.resolve(path.dirname(page),without);
   assert(destination===root||destination.startsWith(root+path.sep),'Link leaves project root: '+link);
   const target=fs.existsSync(destination)&&fs.statSync(destination).isDirectory()?path.join(destination,'index.html'):destination;
   assert(fs.existsSync(target),path.relative(root,page)+' has broken link or image: '+link);
   links++;
  }
 }
}
assert(checked>=9,'Expected all five business areas, including sample and policy');
console.log('Checked '+checked+' pages and '+links+' local links or assets');
