/* Render actual local pages in an isolated headless Chrome profile; no site mutation. */
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..'),out=path.join(__dirname,'browser');fs.mkdirSync(out,{recursive:true});
const chrome='C:/Program Files/Google/Chrome/Application/chrome.exe';
const profile=path.join(require('node:os').tmpdir(),'ac-en-e3-browser-profile-20261117');
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{
 let name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(name.endsWith('/'))name+='index.html';
 const file=path.resolve(root,'.'+name);
 if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
 fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(data);});
});
let child,ws;
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 child=cp.spawn(chrome,['--headless=new','--disable-gpu','--disable-extensions','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:['ignore','ignore','pipe']});
 const endpoint=await new Promise((resolve,reject)=>{let log='';const timeout=setTimeout(()=>reject(new Error('Chrome endpoint timeout')),30000);child.on('error',reject);child.stderr.on('data',chunk=>{log+=chunk;const hit=log.match(/DevTools listening on (ws:\/\/\S+)/);if(hit){clearTimeout(timeout);resolve(hit[1]);}});});
 ws=new WebSocket(endpoint);await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
 let next=0;const pending=new Map();
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(!m.id)return;const p=pending.get(m.id);if(!p)return;pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);};
 const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}));});
 const {targetId}=await send('Target.createTarget',{url:'about:blank'});
 const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
 await send('Page.enable',{},sessionId);await send('Runtime.enable',{},sessionId);
 const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'navigation_plan.json'),'utf8'));
 const results=[];
 for(const row of plan)for(const width of [1280,390]){
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width===390},sessionId);
  await send('Page.navigate',{url:'http://127.0.0.1:'+server.address().port+'/'+row.source},sessionId);
  const deadline=Date.now()+30000;
  while(Date.now()<deadline){const r=await send('Runtime.evaluate',{expression:'document.readyState',returnByValue:true},sessionId);if(r.result.value==='complete')break;await new Promise(r=>setTimeout(r,250));}
  await send('Runtime.evaluate',{expression:'(async()=>{await document.fonts.ready;const choice=[...document.querySelectorAll("button")].find(b=>b.textContent.trim()==="Necessary only");if(choice)choice.click();await new Promise(r=>setTimeout(r,500));const n=document.querySelector(\'[data-en-link-fix="E3"]\');window.scrollTo({top:n.getBoundingClientRect().top+scrollY-90,behavior:"instant"});await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));})()',awaitPromise:true},sessionId);
  const r=await send('Runtime.evaluate',{expression:'JSON.stringify({lang:document.documentElement.lang,viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,addedCards:document.querySelectorAll(\'[data-en-link-fix="E3"] a.hub-card\').length,totalCards:document.querySelectorAll("a.hub-card").length,canonical:document.querySelector(\'link[rel="canonical"]\').href,bodyText:document.body.innerText.length})',returnByValue:true},sessionId);
  const metrics=JSON.parse(r.result.value);
  if(metrics.scrollWidth>metrics.viewport||metrics.addedCards!==row.missing||metrics.lang!=='en')throw new Error(JSON.stringify({source:row.source,width,metrics}));
  const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false},sessionId);
  const name=path.basename(row.source,'.html')+'-'+width+'.png';fs.writeFileSync(path.join(out,name),Buffer.from(shot.data,'base64'));
  results.push({source:row.source,width,...metrics,screenshot:name});console.log(row.source,width,'PASS',metrics.addedCards);
 }
 fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2)+'\n');
 await send('Browser.close');ws.close();server.close();console.log('All 18 rendered views pass.');
})().catch(err=>{console.error(err);if(ws)ws.close();if(child)child.kill();server.close();process.exitCode=1;});
