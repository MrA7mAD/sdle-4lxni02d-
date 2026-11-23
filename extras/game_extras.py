# Game mode: a full-screen arcade-style quiz played with a game controller (or keyboard/touch).
# Uses the app's own bank, progress (record/save → also synced) and history. Idempotent.
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*GAME-MODE*/" in s:
    print("game mode already present"); sys.exit(0)

def sub1(old, new):
    global s
    assert s.count(old) == 1, "anchor not found once: " + old[:70]
    s = s.replace(old, new, 1)

# Button on the bank home, next to "Start a custom set"
sub1('<button class="btn pri" id="mix">Start a custom set</button>',
     '<button class="btn" id="gameBtn" onclick="window.openGame&&openGame()">🎮 Game mode</button><button class="btn pri" id="mix">Start a custom set</button>')

css = r"""
<style>/*GAME-CSS*/
#game{position:fixed;inset:0;z-index:9000;background:radial-gradient(120% 90% at 50% 0%,#1b2550 0%,#0b1020 55%,#070a14 100%);color:#eef2ff;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;overflow:auto;-webkit-user-select:none;user-select:none;display:none}
#game.on{display:block}
#game *{box-sizing:border-box}
#game .gw{max-width:1100px;margin:0 auto;padding:max(18px,env(safe-area-inset-top)) 22px 28px;min-height:100%;display:flex;flex-direction:column}
#game h1{font-size:clamp(34px,5.4vw,64px);margin:4vh 0 4px;letter-spacing:.02em;font-weight:900;background:linear-gradient(90deg,#7dd3fc,#c084fc,#f472b6);-webkit-background-clip:text;background-clip:text;color:transparent;text-align:center}
#game .gtag{text-align:center;color:#a5b4fc;font-size:clamp(15px,1.7vw,19px);margin-bottom:3vh}
#game .gmenu{display:flex;flex-direction:column;gap:12px;max-width:620px;width:100%;margin:0 auto}
#game .mi{display:flex;align-items:center;gap:14px;padding:16px 20px;border-radius:16px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.08);font-size:clamp(17px,2vw,22px);font-weight:650;cursor:pointer;transition:transform .12s,background .12s,border-color .12s}
#game .mi .gv{margin-left:auto;color:#c7d2fe;font-weight:600;font-size:.9em;display:flex;gap:10px;align-items:center}
#game .mi .ar{opacity:.55}
#game .mi.sel{background:rgba(125,211,252,.16);border-color:#7dd3fc;transform:scale(1.025);box-shadow:0 0 0 4px rgba(125,211,252,.12),0 10px 30px rgba(0,0,0,.35)}
#game .mi small{display:block;font-weight:500;color:#a5b4fc;font-size:.72em;margin-top:2px}
#game .stats{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin:0 0 3vh}
#game .gchip{background:rgba(255,255,255,.07);border-radius:999px;padding:7px 14px;font-size:15px;color:#dbe4ff}
#game .ghint{margin-top:auto;padding-top:22px;text-align:center;color:#94a3b8;font-size:15px;display:flex;gap:18px;justify-content:center;flex-wrap:wrap}
#game .b{display:inline-flex;align-items:center;justify-content:center;width:1.7em;height:1.7em;border-radius:50%;font-weight:900;color:#0b1020;font-size:.95em;flex:none}
#game .bA{background:#4ade80}#game .bB{background:#f87171}#game .bX{background:#60a5fa}#game .bY{background:#facc15}
#game .bD{background:#cbd5e1;border-radius:8px;width:auto;padding:0 .45em}
#game .ghud{display:flex;align-items:center;gap:14px;font-weight:800;font-size:clamp(16px,1.9vw,21px)}
#game .ghud .sp{flex:1}
#game .gbar{height:8px;border-radius:9px;background:rgba(255,255,255,.1);overflow:hidden;margin:12px 0 18px}
#game .gbar i{display:block;height:100%;background:linear-gradient(90deg,#7dd3fc,#c084fc);transition:width .3s}
#game .combo{padding:5px 12px;border-radius:999px;background:linear-gradient(90deg,#f59e0b,#ef4444);color:#fff;font-size:.85em}
#game .gmeta{color:#a5b4fc;font-size:14px;margin-bottom:8px;font-weight:600}
#game .gqt{font-size:clamp(21px,2.5vw,30px);line-height:1.38;font-weight:650;margin:0 0 18px}
#game .gimg img{max-width:100%;max-height:34vh;border-radius:12px;display:block;margin:0 auto 16px;background:#fff}
#game .gopts{display:grid;gap:12px}
#game .gop{display:flex;align-items:center;gap:16px;padding:16px 18px;border-radius:16px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.08);font-size:clamp(18px,2.1vw,24px);line-height:1.3;cursor:pointer;transition:transform .12s,background .15s,border-color .15s}
#game .gop .b{width:2em;height:2em;font-size:.9em}
#game .gop.sel{border-color:#7dd3fc;background:rgba(125,211,252,.12)}
#game .gop.ok{background:rgba(74,222,128,.2);border-color:#4ade80}
#game .gop.bad{background:rgba(248,113,113,.2);border-color:#f87171;animation:gshake .35s}
#game .gop.dim{opacity:.45}
@keyframes gshake{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
#game .gfb{margin-top:18px;padding:16px 18px;border-radius:16px;background:rgba(255,255,255,.07);font-size:clamp(16px,1.8vw,20px);line-height:1.5}
#game .gfb b.t{font-size:1.15em}
#game .pop{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%);font-size:clamp(40px,7vw,84px);font-weight:900;pointer-events:none;animation:gpop .9s forwards;text-shadow:0 6px 30px rgba(0,0,0,.5)}
@keyframes gpop{0%{opacity:0;transform:translate(-50%,-30%) scale(.6)}20%{opacity:1;transform:translate(-50%,-50%) scale(1.1)}100%{opacity:0;transform:translate(-50%,-90%) scale(1)}}
#game .gbig{text-align:center;font-size:clamp(44px,7vw,88px);font-weight:900;margin:4vh 0 6px}
#game .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:620px;margin:10px auto 26px}
#game .grid3 div{background:rgba(255,255,255,.06);border-radius:14px;padding:14px;text-align:center;font-size:14px;color:#a5b4fc}
#game .grid3 b{display:block;font-size:26px;color:#eef2ff}
#game .pad{position:fixed;right:18px;bottom:16px;font-size:13px;color:#94a3b8}
#gametoast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:9500;background:#1e293b;color:#fff;padding:12px 18px;border-radius:12px;font:600 15px system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.4)}
</style>
"""
sub1("</head>", css + "</head>")

js = r"""
/*GAME-MODE*/
{
const G={on:false,scr:"menu",sel:0,mode:"quick",topic:-1,run:null,prev:[],held:{},rep:{},raf:0};
const LS="sdle-game-v1";
let GS;try{GS=JSON.parse(localStorage.getItem(LS)||"{}")}catch(e){GS={}}
GS.xp=GS.xp||0;GS.best=GS.best||0;GS.bestStreak=GS.bestStreak||0;
function gsave(){try{localStorage.setItem(LS,JSON.stringify(GS))}catch(e){}}
const lvl=xp=>Math.floor(Math.sqrt(xp/400))+1;
const BTN=["A","B","X","Y"];
const el=()=>document.getElementById("game");
function root(){let d=el();if(!d){d=document.createElement("div");d.id="game";document.body.appendChild(d);
  d.addEventListener("click",e=>{const t=e.target.closest("[data-i]");if(!t)return;const i=+t.dataset.i;
    if(G.scr==="q"){if(G.run.ans==null)answer(i);else next()}else{G.sel=i;act("A")}})}return d}
// ---- sound ----
let AC=null;function tone(f,d,type,v){try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.type=type||"sine";o.frequency.value=f;g.gain.value=v||.08;o.connect(g);g.connect(AC.destination);const t=AC.currentTime;g.gain.setValueAtTime(v||.08,t);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.start(t);o.stop(t+d)}catch(e){}}
const sfx={move:()=>tone(520,.05,"square",.03),ok:()=>{tone(660,.1,"triangle",.12);setTimeout(()=>tone(990,.16,"triangle",.12),90)},bad:()=>tone(160,.28,"sawtooth",.07),
  combo:()=>[660,880,1100].forEach((f,i)=>setTimeout(()=>tone(f,.09,"square",.05),i*70)),end:()=>[523,659,784,1046].forEach((f,i)=>setTimeout(()=>tone(f,.14,"triangle",.1),i*110))};
function rumble(ms,str){try{for(const gp of navigator.getGamepads?navigator.getGamepads():[]){const a=gp&&gp.vibrationActuator;if(a&&a.playEffect)a.playEffect("dual-rumble",{duration:ms,strongMagnitude:str,weakMagnitude:str})}}catch(e){}}
// ---- pools ----
function playable(i){const q=Q[i];return q.k==="mcq"&&q.o.length>=2&&q.o.length<=4&&q.a.length}
function pool(){let ids=[];for(let i=0;i<Q.length;i++)if(playable(i)&&(G.topic<0||Q[i].s===G.topic))ids.push(i);
  if(G.mode==="fix")ids=ids.filter(i=>stat(i)==="bad");
  const pr=i=>{const t=stat(i);return t==="bad"?2:t==="new"?1:0};
  ids=shuffle(ids);ids.sort((a,b)=>pr(b)-pr(a));return ids}
// ---- screens ----
function menuItems(){const nb=ORDER.length,nt=SECS.length;
  return [
   {k:"quick",t:"▶ Quick run",s:"10 questions — new and missed ones first"},
   {k:"surv",t:"♥ Survival",s:"Keep going until you lose 3 hearts"},
   {k:"fix",t:"✖ Fix my mistakes",s:"Only questions you got wrong ("+mistakes().filter(playable).length+")"},
   {k:"topic",t:"Topic",v:G.topic<0?"All specialties":(SECS[G.topic][1]||SECS[G.topic][0]),lr:1},
   {k:"bank",t:"Bank",v:B.name,lr:1},
   {k:"exit",t:"✕ Exit game mode"}]}
function hint(h){return '<div class="ghint">'+h+'</div>'}
const HB=x=>'<span class="b b'+x+'">'+x+'</span>',HD=x=>'<span class="b bD">'+x+'</span>';
function drawMenu(){const it=menuItems();G.sel=Math.min(G.sel,it.length-1);
  root().innerHTML='<div class="gw"><h1>SDLE Arcade</h1><div class="gtag">'+esc(B.name)+'</div>'+
  '<div class="stats"><span class="gchip">⭐ Level '+lvl(GS.xp)+' · '+GS.xp.toLocaleString()+' XP</span><span class="gchip">🏆 Best score '+GS.best.toLocaleString()+'</span><span class="gchip">🔥 Best streak '+GS.bestStreak+'</span></div>'+
  '<div class="gmenu">'+it.map((m,i)=>'<div class="mi'+(i===G.sel?' sel':'')+'" data-i="'+i+'"><div>'+m.t+(m.s?'<small>'+m.s+'</small>':'')+'</div>'+(m.v?'<span class="gv">'+(m.lr?'<span class="ar">◀</span>':'')+esc(m.v)+(m.lr?'<span class="ar">▶</span>':'')+'</span>':'')+'</div>').join("")+'</div>'+
  hint('<span>'+HD("✚")+' move</span><span>'+HD("◀ ▶")+' change</span><span>'+HB("A")+' select</span><span>'+HB("B")+' exit</span>')+'</div>'}
function startRun(mode){const ids=pool();if(!ids.length){toastG(mode==="fix"?"No mistakes here — nice!":"No playable questions in this topic");return}
  G.mode=mode;G.run={mode,ids:mode==="quick"?ids.slice(0,10):ids,idx:0,score:0,streak:0,best:0,ok:0,n:0,hearts:3,ans:null,perm:null,t0:0,hid:Date.now(),xp:0};
  P.hist.push({id:G.run.hid,ti:"🎮 Game · "+(mode==="quick"?"Quick run":mode==="surv"?"Survival":"Fix mistakes"),m:"p",t1:Date.now(),r:{}});if(P.hist.length>300)P.hist.shift();
  G.scr="q";drawQ()}
function drawQ(){const r=G.run,qi=r.ids[r.idx],q=Q[qi];if(r.ans==null&&!r.perm){r.perm=shuffle(q.o.map((_,k)=>k));r.t0=Date.now();G.sel=0}
  const tot=r.mode==="quick"?r.ids.length:null,mult=Math.min(4,1+Math.floor(r.streak/3));
  const hud='<div class="ghud"><span>'+(r.mode==="surv"?"❤️".repeat(r.hearts)+"🖤".repeat(3-r.hearts):"Q "+(r.idx+1)+(tot?" / "+tot:""))+'</span><span class="sp"></span>'+(r.streak>=3?'<span class="combo">x'+mult+' COMBO</span>':'')+'<span>🔥 '+r.streak+'</span><span>⭐ '+r.score.toLocaleString()+'</span></div>';
  const bar='<div class="gbar"><i style="width:'+(tot?Math.round(100*(r.idx+(r.ans!=null?1:0))/tot):Math.min(100,r.n*5))+'%"></i></div>';
  const done=r.ans!=null;
  const ops=r.perm.map((oi,k)=>{let c="gop";if(done){if(q.a.includes(oi))c+=" ok";else if(oi===r.ans)c+=" bad";else c+=" dim"}else if(k===G.sel)c+=" sel";
    return '<div class="'+c+'" data-i="'+k+'">'+HB(BTN[k])+'<span>'+esc(q.o[oi])+'</span></div>'}).join("");
  let fb="";if(done){const ok=q.a.includes(r.ans);fb='<div class="gfb"><b class="t" style="color:'+(ok?'#4ade80':'#f87171')+'">'+(ok?'Correct!':'Not quite — answer: '+esc(q.o[q.a[0]]))+'</b>'+(q.e?'<div style="margin-top:6px">'+esc(q.e)+'</div>':'')+'</div>'}
  root().innerHTML='<div class="gw">'+hud+bar+'<div class="gmeta">'+esc(q.i)+' · '+esc(SECS[q.s]?SECS[q.s][0]:"")+(q.by?' · '+esc(q.by):'')+'</div>'+
   '<div class="gimg">'+imgs(q.pi)+'</div><div class="gqt">'+esc(q.q)+'</div><div class="gopts">'+ops+'</div>'+fb+
   hint(done?'<span>'+HB("A")+' next</span><span>'+HB("Y")+' '+(P.bm[q.i]?'bookmarked ✓':'bookmark')+'</span><span>'+HD("☰")+' pause</span>':'<span>'+HB("A")+HB("B")+HB("X")+HB("Y")+' answer</span><span>'+HD("✚")+' + '+HB("A")+' also works</span><span>'+HD("☰")+' pause</span>')+'</div>';
  if(done){const f=root().querySelector(".gfb");f&&f.scrollIntoView({block:"nearest",behavior:"smooth"})}else root().scrollTop=0}
function answer(k){const r=G.run;if(r.ans!=null||k>=r.perm.length)return;const qi=r.ids[r.idx],q=Q[qi],oi=r.perm[k],ok=q.a.includes(oi);
  r.ans=oi;r.n++;record(qi,oi);const h=P.hist.find(x=>x.id===r.hid);if(h){h.r[q.i]=ok?1:0;h.t1=Date.now()}save();
  if(ok){r.ok++;r.streak++;r.best=Math.max(r.best,r.streak);const mult=Math.min(4,1+Math.floor((r.streak-1)/3)),sec=(Date.now()-r.t0)/1000,bonus=Math.max(0,Math.round(50*(1-sec/40))),pts=(100+bonus)*mult;r.score+=pts;
    pop("+"+pts,"#4ade80");if(r.streak%3===0){sfx.combo();rumble(160,.5)}else{sfx.ok();rumble(60,.25)}}
  else{r.streak=0;if(r.mode==="surv")r.hearts--;pop(r.mode==="surv"?"💔":"✖","#f87171");sfx.bad();rumble(260,.9)}
  drawQ()}
function next(){const r=G.run;if(r.mode==="surv"&&r.hearts<=0)return end();r.idx++;r.ans=null;r.perm=null;if(r.idx>=r.ids.length)return end();drawQ()}
function end(){const r=G.run;G.scr="end";const acc=r.n?Math.round(100*r.ok/r.n):0;r.xp=r.score+r.ok*20;const before=lvl(GS.xp);GS.xp+=r.xp;
  const nb=r.score>GS.best;if(nb)GS.best=r.score;GS.bestStreak=Math.max(GS.bestStreak,r.best);gsave();sfx.end();G.sel=0;
  root().innerHTML='<div class="gw"><div class="gbig">'+(r.mode==="surv"&&r.hearts<=0?"Game over":"Run complete")+'</div><div class="gtag">'+(nb?"🏆 New best score!":"")+(lvl(GS.xp)>before?" ⭐ Level up! You are now level "+lvl(GS.xp):"")+'</div>'+
  '<div class="grid3"><div><b>'+r.score.toLocaleString()+'</b>score</div><div><b>'+r.ok+'/'+r.n+'</b>correct ('+acc+'%)</div><div><b>🔥 '+r.best+'</b>best streak</div></div>'+
  '<div class="gmenu"><div class="mi sel" data-i="0">▶ Play again</div><div class="mi" data-i="1">☰ Menu</div></div>'+hint('<span>'+HB("A")+' select</span><span>'+HB("B")+' menu</span>')+'</div>'}
function drawPause(){root().insertAdjacentHTML("beforeend",'<div id="gpause" style="position:fixed;inset:0;background:rgba(5,8,18,.82);display:flex;align-items:center;justify-content:center"><div class="gmenu" style="max-width:420px"><div class="gbig" style="font-size:44px;margin:0 0 10px">Paused</div><div class="mi'+(G.sel===0?' sel':'')+'" data-i="0">▶ Resume</div><div class="mi'+(G.sel===1?' sel':'')+'" data-i="1">☰ Quit to menu</div></div></div>')}
function pop(t,c){const d=document.createElement("div");d.className="pop";d.style.color=c;d.textContent=t;root().appendChild(d);setTimeout(()=>d.remove(),900)}
function toastG(m){let t=document.getElementById("gametoast");if(t)t.remove();t=document.createElement("div");t.id="gametoast";t.textContent=m;document.body.appendChild(t);setTimeout(()=>t.remove(),3200)}
function draw(){if(G.scr==="menu")drawMenu();else if(G.scr==="q")drawQ();else if(G.scr==="pause"){drawQ();drawPause()}}
// ---- input ----
function act(b){if(!G.on)return;
  if(G.scr==="menu"){const it=menuItems(),m=it[G.sel];
    if(b==="up"||b==="down"){G.sel=(G.sel+(b==="up"?-1:1)+it.length)%it.length;sfx.move();return drawMenu()}
    if((b==="left"||b==="right")&&m.lr){const d=b==="left"?-1:1;
      if(m.k==="topic"){G.topic=G.topic+d;if(G.topic<-1)G.topic=SECS.length-1;if(G.topic>=SECS.length)G.topic=-1}
      if(m.k==="bank"){const i=(ORDER.indexOf(B.id)+d+ORDER.length)%ORDER.length;useBank(ORDER[i]);G.topic=-1}
      sfx.move();return drawMenu()}
    if(b==="A"){if(m.k==="exit")return closeGame();if(m.lr)return act("right");return startRun(m.k)}
    if(b==="B")return closeGame();return}
  if(G.scr==="q"){const r=G.run;
    if(b==="start"){G.scr="pause";G.sel=0;return draw()}
    if(r.ans==null){const k=BTN.indexOf(b);
      if(b==="up"||b==="down"){G.sel=(G.sel+(b==="up"?-1:1)+r.perm.length)%r.perm.length;sfx.move();return drawQ()}
      if(k>=0)return answer(b==="A"&&G.selMoved?G.sel:k);return}
    if(b==="A")return next();
    if(b==="Y"){toggleBm(r.ids[r.idx]);return drawQ()}
    if(b==="B"){G.scr="pause";G.sel=0;return draw()}
    return}
  if(G.scr==="pause"){if(b==="up"||b==="down"){G.sel=1-G.sel;sfx.move();return draw()}
    if(b==="A"){if(G.sel===0){G.scr="q";return drawQ()}G.scr="menu";G.sel=0;return drawMenu()}
    if(b==="B"||b==="start"){G.scr="q";return drawQ()}return}
  if(G.scr==="end"){if(b==="up"||b==="down"){G.sel=1-G.sel;sfx.move();return end_redraw()}
    if(b==="A"){if(G.sel===0)return startRun(G.mode);G.scr="menu";G.sel=0;return drawMenu()}
    if(b==="B"){G.scr="menu";G.sel=0;return drawMenu()}}}
function end_redraw(){root().querySelectorAll(".gmenu .mi").forEach((m,i)=>m.classList.toggle("sel",i===G.sel))}
// D-pad moves a cursor; once moved, A confirms the highlighted option instead of picking option A.
const _act=act;act=function(b){if(G.scr==="q"&&G.run&&G.run.ans==null){if(b==="up"||b==="down")G.selMoved=true}else G.selMoved=false;_act(b);if(G.scr!=="q"||(G.run&&G.run.ans!=null))G.selMoved=false};
const MAP={0:"A",1:"B",2:"X",3:"Y",12:"up",13:"down",14:"left",15:"right",9:"start",8:"start"};
function poll(){G.raf=requestAnimationFrame(poll);const pads=navigator.getGamepads?navigator.getGamepads():[];const now=performance.now();const down={};
  for(const gp of pads){if(!gp)continue;gp.buttons.forEach((bt,i)=>{if(MAP[i]&&(bt.pressed||bt.value>.6))down[MAP[i]]=1});
    const ax=gp.axes||[];if(ax[1]<-.6)down.up=1;if(ax[1]>.6)down.down=1;if(ax[0]<-.6)down.left=1;if(ax[0]>.6)down.right=1}
  for(const k in down){if(!G.held[k]){G.held[k]=now;G.rep[k]=now+380;if(G.on)act(k);else if(k==="start")openGame()}
    else if(["up","down","left","right"].includes(k)&&now>G.rep[k]&&G.on){G.rep[k]=now+130;act(k)}}
  for(const k in G.held)if(!down[k])delete G.held[k]}
function ensurePoll(){if(!G.raf&&navigator.getGamepads)poll()}
window.addEventListener("gamepadconnected",e=>{ensurePoll();if(!G.on)toastG("🎮 Controller connected — press ☰ (Menu/Start) to open Game mode")});
document.addEventListener("keydown",e=>{if(!G.on)return;const k=e.key,m={ArrowUp:"up",ArrowDown:"down",ArrowLeft:"left",ArrowRight:"right",Enter:"A",Escape:"B",Backspace:"B"," ":"A",p:"start",P:"start"};
  let b=m[k];if(!b&&G.scr==="q"&&G.run&&G.run.ans==null){const n="1234".indexOf(k);if(n>=0)b=BTN[n]}
  if(b){e.preventDefault();act(b)}e.stopPropagation();e.stopImmediatePropagation()},true);
window.openGame=function(){if(typeof B==="undefined"||!B){const last=lsGet(LSB)||ORDER[0];useBank(BANKS[last]?last:ORDER[0]);$("#pick").hidden=true;$("#app").hidden=false;go("home")}
  stopTick();G.on=true;G.scr="menu";G.sel=0;root().classList.add("on");document.documentElement.style.overflow="hidden";drawMenu();ensurePoll()};
function closeGame(){G.on=false;const d=el();if(d){d.classList.remove("on");d.innerHTML=""}document.documentElement.style.overflow="";if(typeof render==="function"&&!$("#app").hidden)go("home")}
}
"""
anchor = "showPicker();\ndbHandles();\n"
assert s.count(anchor) == 1, "app end not found"
s = s.replace(anchor, anchor + js, 1)
open(p, "w", encoding="utf-8").write(s)
print("game mode added")
