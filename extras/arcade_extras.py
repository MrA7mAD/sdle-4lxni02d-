# Arcade feel for the normal study screens: 8-bit background music, sound effects, streak/combo pops,
# XP level pill, and game-controller navigation everywhere (not just Game mode). Settings row to turn
# music/effects on or off and to see whether a controller is detected. Idempotent.
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "/*ARCADE-JS*/" in s:
    print("arcade already present"); sys.exit(0)

def sub1(old, new):
    global s
    assert s.count(old) == 1, "anchor not found once: " + old[:70]
    s = s.replace(old, new, 1)

row_anchor = "<button class=\"btn\" data-xfer>Export / import</button></div>'+"
sub1(row_anchor, row_anchor + "\n   (window.arcRow?arcRow():'')+")

css = r"""
<style>/*ARCADE-CSS*/
#arcpop{position:fixed;left:50%;top:30%;transform:translate(-50%,-50%);z-index:8000;pointer-events:none;font:900 clamp(30px,5vw,60px)/1.1 system-ui,sans-serif;text-align:center;animation:arcpop 1s forwards;text-shadow:0 4px 24px rgba(0,0,0,.35)}
@keyframes arcpop{0%{opacity:0;transform:translate(-50%,-30%) scale(.6)}18%{opacity:1;transform:translate(-50%,-50%) scale(1.12)}100%{opacity:0;transform:translate(-50%,-95%) scale(1)}}
#archud{position:fixed;right:14px;bottom:14px;z-index:7000;display:none;gap:8px;align-items:center;background:rgba(15,23,42,.88);color:#fff;border-radius:999px;padding:8px 14px;font:700 14px system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3)}
body.quizmode #archud.on{display:flex}
#archud button{all:unset;cursor:pointer;font-size:16px;padding:0 2px}
#archud .xp{width:60px;height:6px;border-radius:6px;background:rgba(255,255,255,.2);overflow:hidden}
#archud .xp i{display:block;height:100%;background:linear-gradient(90deg,#7dd3fc,#c084fc)}
html.pad :focus{outline:3px solid #38bdf8!important;outline-offset:3px;border-radius:10px}
.arc-flash-ok{animation:arcok .5s}.arc-flash-bad{animation:arcbad .4s}
@keyframes arcok{0%{box-shadow:inset 0 0 0 0 rgba(74,222,128,0)}40%{box-shadow:inset 0 0 0 9999px rgba(74,222,128,.10)}100%{box-shadow:inset 0 0 0 0 rgba(74,222,128,0)}}
@keyframes arcbad{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
</style>
"""
sub1("</head>", css + "</head>")

js = r"""
/*ARCADE-JS*/
{
const KS="sdle-arcade-v1";let A;try{A=JSON.parse(localStorage.getItem(KS)||"{}")}catch(e){A={}}
if(A.music===undefined)A.music=true;if(A.sfx===undefined)A.sfx=true;
const asave=()=>{try{localStorage.setItem(KS,JSON.stringify(A))}catch(e){}};
// ---------- audio ----------
let AC=null,MG=null,SG=null;
function ac(){if(!AC){try{if(navigator.audioSession)navigator.audioSession.type="playback"}catch(e){}
  AC=new (window.AudioContext||window.webkitAudioContext)();MG=AC.createGain();MG.gain.value=.07;MG.connect(AC.destination);SG=AC.createGain();SG.gain.value=.11;SG.connect(AC.destination)}
  if(AC.state==="suspended")AC.resume();return AC}
["pointerdown","keydown","touchend"].forEach(t=>document.addEventListener(t,()=>{if(A.music||A.sfx)ac()},{capture:true,passive:true}));
function note(dst,f,t,d,type,v){const o=AC.createOscillator(),g=AC.createGain();o.type=type;o.frequency.setValueAtTime(f,t);g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.0008,t+d*.95);o.connect(g);g.connect(dst);o.start(t);o.stop(t+d)}
let NB=null;function noise(t,d,v){if(!NB){NB=AC.createBuffer(1,AC.sampleRate*.2,AC.sampleRate);const c=NB.getChannelData(0);for(let i=0;i<c.length;i++)c[i]=Math.random()*2-1}
  const s=AC.createBufferSource(),g=AC.createGain(),f=AC.createBiquadFilter();f.type="highpass";f.frequency.value=6000;s.buffer=NB;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);s.connect(f);f.connect(g);g.connect(MG);s.start(t);s.stop(t+d)}
function kick(t){const o=AC.createOscillator(),g=AC.createGain();o.frequency.setValueAtTime(140,t);o.frequency.exponentialRampToValueAtTime(40,t+.12);g.gain.setValueAtTime(.9,t);g.gain.exponentialRampToValueAtTime(.001,t+.14);o.connect(g);g.connect(MG);o.start(t);o.stop(t+.15)}
const NF=n=>{const m=n.match(/^([A-G])(#?)(\d)$/);const st={C:0,D:2,E:4,F:5,G:7,A:9,B:11}[m[1]]+(m[2]?1:0)+12*(+m[3]+1);return 440*Math.pow(2,(st-69)/12)};
// Original melancholic trip-hop / ambient piece ("Fog" mood). D minor, 68 bpm. Returns loop length (s).
function buildTune(ctx,out,t0){
  const BPM=68,BEAT=60/BPM,BAR=BEAT*4,BARS=16;
  const N=n=>{const m=n.match(/^([A-G])([b#]?)(\d)$/);const st={C:0,D:2,E:4,F:5,G:7,A:9,B:11}[m[1]]+(m[2]==="#"?1:m[2]==="b"?-1:0)+12*(+m[3]+1);return 440*Math.pow(2,(st-69)/12)};
  // reverb
  let ir=buildTune.ir;if(!ir||ir.sampleRate!==ctx.sampleRate){ir=buildTune.ir=ctx.createBuffer(2,ctx.sampleRate*3.2,ctx.sampleRate);
  for(let c=0;c<2;c++){const d=ir.getChannelData(c);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/d.length,2.6)}}
  const rev=ctx.createConvolver();rev.buffer=ir;const revG=ctx.createGain();revG.gain.value=.55;rev.connect(revG);revG.connect(out);
  const dry=ctx.createGain();dry.gain.value=.8;dry.connect(out);
  const send=(node,amt)=>{const g=ctx.createGain();g.gain.value=amt;node.connect(g);g.connect(rev)};
  // tape-ish echo for the guitar
  const dl=ctx.createDelay(2);dl.delayTime.value=BEAT*.75;const fb=ctx.createGain();fb.gain.value=.38;const dlf=ctx.createBiquadFilter();dlf.type="lowpass";dlf.frequency.value=2200;
  dl.connect(dlf);dlf.connect(fb);fb.connect(dl);const echoOut=ctx.createGain();echoOut.gain.value=.45;dlf.connect(echoOut);echoOut.connect(dry);send(echoOut,.5);
  const CH=[["D2",["D3","A3","E4","F4"]],["Bb1",["Bb2","F3","A3","D4"]],["G1",["G2","D3","F3","Bb3"]],["A1",["A2","E3","G3","C#4"]],
            ["D2",["D3","A3","C4","F4"]],["F1",["F2","C3","E3","A3"]],["G1",["G2","D3","Bb3","D4"]],["A1",["A2","E3","A3","C#4"]]];
  const MEL=[[8,0,"A4",2],[8,2,"F4",1],[8,3,"E4",3],[9,2,"D4",1],[9,3,"F4",2.5],[10,0,"G4",1.5],[10,1.5,"F4",.5],[10,2,"D4",2],
             [11,0,"E4",3],[11,3,"C#4",1],[12,0,"D4",2],[12,2,"A4",2],[13,0,"C5",1.5],[13,1.5,"A4",.5],[13,2,"G4",2],
             [14,0,"F4",1.5],[14,1.5,"G4",.5],[14,2,"Bb4",2],[15,0,"A4",4]];
  function pad(f,t,d,v){for(const det of[-7,6]){const o=ctx.createOscillator(),fl=ctx.createBiquadFilter(),g=ctx.createGain();o.type="sawtooth";o.frequency.value=f;o.detune.value=det;
    fl.type="lowpass";fl.frequency.setValueAtTime(500,t);fl.frequency.linearRampToValueAtTime(900,t+d*.5);fl.frequency.linearRampToValueAtTime(500,t+d);
    g.gain.setValueAtTime(.0001,t);g.gain.linearRampToValueAtTime(v,t+d*.4);g.gain.linearRampToValueAtTime(.0001,t+d+.4);o.connect(fl);fl.connect(g);g.connect(dry);send(g,.8);o.start(t);o.stop(t+d+.5)}}
  function pluck(f,t,v){const o=ctx.createOscillator(),o2=ctx.createOscillator(),fl=ctx.createBiquadFilter(),g=ctx.createGain();o.type="triangle";o2.type="sawtooth";o.frequency.value=f;o2.frequency.value=f*1.002;
    fl.type="lowpass";fl.frequency.setValueAtTime(3200,t);fl.frequency.exponentialRampToValueAtTime(700,t+.6);const g2=ctx.createGain();g2.gain.value=.25;
    g.gain.setValueAtTime(.0001,t);g.gain.linearRampToValueAtTime(v,t+.006);g.gain.exponentialRampToValueAtTime(.0005,t+1.6);
    o.connect(fl);o2.connect(g2);g2.connect(fl);fl.connect(g);g.connect(dry);g.connect(dl);send(g,.35);o.start(t);o2.start(t);o.stop(t+1.7);o2.stop(t+1.7)}
  function bass(f,t,d,v){const o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.value=f;g.gain.setValueAtTime(.0001,t);g.gain.linearRampToValueAtTime(v,t+.04);g.gain.setValueAtTime(v,t+d*.7);g.gain.linearRampToValueAtTime(.0001,t+d);o.connect(g);g.connect(dry);o.start(t);o.stop(t+d+.05)}
  function lead(f,t,d,v){const o=ctx.createOscillator(),lfo=ctx.createOscillator(),lg=ctx.createGain(),fl=ctx.createBiquadFilter(),g=ctx.createGain();o.type="square";o.frequency.value=f;
    lfo.frequency.value=5.2;lg.gain.setValueAtTime(0,t);lg.gain.linearRampToValueAtTime(f*.012,t+.35);lfo.connect(lg);lg.connect(o.frequency);
    fl.type="lowpass";fl.frequency.value=1500;g.gain.setValueAtTime(.0001,t);g.gain.linearRampToValueAtTime(v,t+.08);g.gain.setValueAtTime(v,t+d*.75);g.gain.linearRampToValueAtTime(.0001,t+d+.25);
    o.connect(fl);fl.connect(g);g.connect(dry);g.connect(dl);send(g,.9);o.start(t);lfo.start(t);o.stop(t+d+.3);lfo.stop(t+d+.3)}
  let NB=buildTune.nb;if(!NB||NB.sampleRate!==ctx.sampleRate){NB=buildTune.nb=ctx.createBuffer(1,ctx.sampleRate*.5,ctx.sampleRate);const c=NB.getChannelData(0);for(let i=0;i<c.length;i++)c[i]=Math.random()*2-1}
  function kick(t,v){const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.setValueAtTime(110,t);o.frequency.exponentialRampToValueAtTime(42,t+.18);g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+.35);o.connect(g);g.connect(dry);o.start(t);o.stop(t+.4)}
  function snare(t,v){const s=ctx.createBufferSource(),f=ctx.createBiquadFilter(),g=ctx.createGain();s.buffer=NB;f.type="bandpass";f.frequency.value=1600;f.Q.value=.7;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+.32);s.connect(f);f.connect(g);g.connect(dry);send(g,1.2);s.start(t);s.stop(t+.35)}
  function hat(t,v){const s=ctx.createBufferSource(),f=ctx.createBiquadFilter(),g=ctx.createGain();s.buffer=NB;f.type="highpass";f.frequency.value=7000;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+.07);s.connect(f);f.connect(g);g.connect(dry);s.start(t);s.stop(t+.08)}
  const ARP=[0,1,2,3,2,1,2,1];
  for(let bar=0;bar<BARS;bar++){const tb=t0+bar*BAR,[root,ch]=CH[bar%8];
    pad(N(ch[0]),tb,BAR,.035);pad(N(ch[2]),tb,BAR,.03);pad(N(ch[3]),tb,BAR,.025);
    bass(N(root),tb,BEAT*2.6,.32);bass(N(root),tb+BEAT*3,BEAT*.9,.2);
    for(let e=0;e<8;e++){const sw=e%2?BEAT*.06:0;pluck(N(ch[ARP[e]])*2,tb+e*BEAT/2+sw,e%2?.05:.08)}
    if(bar>=2){kick(tb,.55);kick(tb+BEAT*1.75,.35);kick(tb+BEAT*2.5,.4);snare(tb+BEAT,.22);snare(tb+BEAT*3,.22);for(let h=0;h<8;h++)hat(tb+h*BEAT/2+(h%2?BEAT*.06:0),h%2?.03:.05)}}
  for(const[bar,beat,n,d]of MEL)lead(N(n),t0+bar*BAR+beat*BEAT,d*BEAT,.05);
  return BARS*BAR}
let mus=null;
function musicOn(){ac();if(mus)return;const g=AC.createGain();g.gain.setValueAtTime(0,AC.currentTime);g.gain.linearRampToValueAtTime(1.3,AC.currentTime+2);g.connect(MG);
  mus={g,next:AC.currentTime+.1,timer:0};const sch=()=>{if(!mus)return;while(mus.next<AC.currentTime+3)mus.next+=buildTune(AC,mus.g,mus.next)};sch();mus.timer=setInterval(sch,1000)}
function musicOff(){if(!mus)return;const m=mus;mus=null;clearInterval(m.timer);try{m.g.gain.cancelScheduledValues(AC.currentTime);m.g.gain.setTargetAtTime(0,AC.currentTime,.25)}catch(e){}setTimeout(()=>{try{m.g.disconnect()}catch(e){}},1500)}
function wantMusic(){if(!A.music||document.visibilityState!=="visible")return false;const g=document.getElementById("game");return !!(g&&g.classList.contains("on"))}
setInterval(()=>{if(wantMusic()){if(AC&&AC.state==="running")musicOn()}else musicOff()},400);
const fx={ok:()=>{note(SG,660,AC.currentTime,.1,"square",.5);note(SG,990,AC.currentTime+.08,.18,"square",.5)},
  bad:()=>{note(SG,180,AC.currentTime,.12,"sawtooth",.45);note(SG,120,AC.currentTime+.1,.25,"sawtooth",.45)},
  tick:()=>note(SG,880,AC.currentTime,.04,"square",.18),
  combo:()=>[660,880,1100,1320].forEach((f,i)=>note(SG,f,AC.currentTime+i*.06,.09,"square",.4)),
  win:()=>[523,659,784,1046,784,1046].forEach((f,i)=>note(SG,f,AC.currentTime+i*.11,.14,"triangle",.6))};
function sfx(k){if(!A.sfx)return;try{ac();fx[k]()}catch(e){}}
function rumble(ms,m){try{for(const gp of navigator.getGamepads?navigator.getGamepads():[]){const a=gp&&gp.vibrationActuator;if(a&&a.playEffect)a.playEffect("dual-rumble",{duration:ms,strongMagnitude:m,weakMagnitude:m})}}catch(e){}}
// ---------- streak, XP, pops ----------
let GS;const GK="sdle-game-v1";const gget=()=>{try{GS=JSON.parse(localStorage.getItem(GK)||"{}")}catch(e){GS={}}GS.xp=GS.xp||0};gget();
const lvl=xp=>Math.floor(Math.sqrt(xp/400))+1;let streak=0;
function hud(){let h=document.getElementById("archud");if(!h){h=document.createElement("div");h.id="archud";document.body.appendChild(h);
  h.addEventListener("click",e=>{if(e.target.closest("[data-mu]")){A.music=!A.music;asave();if(A.music)ac();hud()}})}
  gget();const L=lvl(GS.xp),lo=400*(L-1)*(L-1),hi=400*L*L;h.classList.toggle("on",A.sfx||A.music);
  h.innerHTML='<span>🔥 '+streak+'</span><span>⭐ Lv '+L+'</span><span class="xp"><i style="width:'+Math.round(100*(GS.xp-lo)/(hi-lo))+'%"></i></span><button data-mu title="Music">'+(A.music?'🎵':'🔇')+'</button>'}
function pop(t,c){if(!A.sfx)return;const o=document.getElementById("arcpop");if(o)o.remove();const d=document.createElement("div");d.id="arcpop";d.style.color=c;d.innerHTML=t;document.body.appendChild(d);setTimeout(()=>d.remove(),1000)}
const _choose=choose;choose=function(oi){const qi=S&&S.ids?S.ids[S.idx]:null,before=qi!=null?S.picks[qi]:undefined;_choose(oi);
  if(qi==null||S.mode!=="practice"||before!==undefined||S.picks[qi]===undefined){if(S&&S.mode==="exam")sfx("tick");return}
  const ok=okOf(qi,oi);gget();
  if(ok){streak++;GS.xp+=10+Math.min(streak,10)*2;
    if(streak>0&&streak%5===0){sfx("combo");rumble(200,.6);pop("🔥 "+streak+" in a row!","#f59e0b")}else{sfx("ok");rumble(60,.25);if(streak>=3)pop("+"+(10+Math.min(streak,10)*2)+" XP","#22c55e")}}
  else{if(streak>=5)pop("Streak lost 💔","#ef4444");streak=0;sfx("bad");rumble(240,.9);const m=document.querySelector("main");if(m){m.classList.remove("arc-flash-bad");void m.offsetWidth;m.classList.add("arc-flash-bad")}}
  const before_l=lvl(GS.xp-(ok?10+Math.min(streak,10)*2:0));try{localStorage.setItem(GK,JSON.stringify(Object.assign(JSON.parse(localStorage.getItem(GK)||"{}"),{xp:GS.xp})))}catch(e){}
  if(ok&&lvl(GS.xp)>before_l){setTimeout(()=>{pop("⭐ Level "+lvl(GS.xp)+"!","#a855f7");sfx("win")},500)}hud()};
const _move=move;move=function(d){_move(d);sfx("tick")};
const _finish=finish;finish=function(){_finish();sfx("win")};
setInterval(()=>{if(document.body.classList.contains("quizmode"))hud()},1500);
// ---------- controller ----------
let raf=0;const held={},rep={};const MAP={0:"A",1:"B",2:"X",3:"Y",4:"LB",5:"RB",8:"select",9:"start",12:"up",13:"down",14:"left",15:"right"};
const key=k=>document.dispatchEvent(new KeyboardEvent("keydown",{key:k,bubbles:true,cancelable:true}));
function focusables(){return [...document.querySelectorAll('#layer button,#layer [data-i],#layer input,#layer a[href]')].length?
  [...document.querySelectorAll('#layer button,#layer input,#layer a[href],#layer [tabindex]')]:
  [...document.querySelectorAll('#pick button,#app button,#app a[href],#app input,#app select,#app [tabindex]:not([tabindex="-1"])')]}
function visible(e){const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=="hidden"&&!e.closest("[hidden]")}
function spatial(dir){const els=focusables().filter(visible);if(!els.length)return;let cur=document.activeElement;
  if(!els.includes(cur)){const v=els.find(e=>{const r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight})||els[0];v.focus({preventScroll:false});v.scrollIntoView({block:"nearest"});return}
  const c=cur.getBoundingClientRect(),cx=c.left+c.width/2,cy=c.top+c.height/2;let best=null,bd=1e9;
  for(const e of els){if(e===cur)continue;const r=e.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2,dx=x-cx,dy=y-cy;
    const ok=dir==="down"?dy>4:dir==="up"?dy<-4:dir==="right"?dx>4:dx<-4;if(!ok)continue;
    const main=dir==="down"||dir==="up"?Math.abs(dy):Math.abs(dx),side=dir==="down"||dir==="up"?Math.abs(dx):Math.abs(dy);const d=main+side*2.2;if(d<bd){bd=d;best=e}}
  if(best){best.focus();best.scrollIntoView({block:"nearest",behavior:"smooth"});sfx("tick")}else if(dir==="down"||dir==="up")window.scrollBy({top:dir==="down"?240:-240,behavior:"smooth"})}
function inQuiz(){return typeof V!=="undefined"&&V.name==="quiz"&&!$("#app").hidden&&!$("#layer").innerHTML&&S&&S.ids}
function act(b){document.documentElement.classList.add("pad");
  if(b==="start"){if(window.openGame)openGame();return}
  if(inQuiz()){const qi=S.ids[S.idx],q=Q[qi],answered=S.picks[qi]!==undefined&&S.mode!=="exam";
    if(q.k==="card"){if(b==="A")key(" ");else if(b==="X")key("y");else if(b==="Y")key("n");else if(b==="right"||b==="RB")key("ArrowRight");else if(b==="left"||b==="LB")key("ArrowLeft");else if(b==="select"||b==="B")go("home");return}
    if(answered&&b==="A"){if(S.idx<S.ids.length-1)key("ArrowRight");else{const f=[...document.querySelectorAll("#app button")].find(x=>/Finish/.test(x.textContent));f&&f.click()}return}
    if(answered&&b==="Y"){key("s");return}
    const pos={A:0,B:1,X:2,Y:3}[b];if(pos!==undefined){key("abcd"[pos]);return}
    if(b==="right"||b==="RB")return key("ArrowRight");if(b==="left"||b==="LB")return key("ArrowLeft");
    if(b==="down"||b==="up")return window.scrollBy({top:b==="down"?260:-260,behavior:"smooth"});
    if(b==="select"){go("home");return}return}
  if(["up","down","left","right"].includes(b))return spatial(b);
  if(b==="A"){const e=document.activeElement;if(e&&e!==document.body&&focusables().includes(e)){e.click();sfx("tick")}else spatial("down");return}
  if(b==="B"||b==="select"){if($("#layer").innerHTML){key("Escape");const x=document.querySelector("#layer [id$=close],#layer .x");x&&x.click();return}
    if(!$("#app").hidden&&typeof V!=="undefined"&&V.name!=="home"){go("home");return}return}
  if(b==="LB"||b==="RB")window.scrollBy({top:b==="RB"?500:-500,behavior:"smooth"})}
function poll(){raf=requestAnimationFrame(poll);const g=document.getElementById("game");const gameOn=g&&g.classList.contains("on");
  const pads=navigator.getGamepads?navigator.getGamepads():[];const now=performance.now(),down={};
  for(const gp of pads){if(!gp)continue;gp.buttons.forEach((bt,i)=>{if(MAP[i]&&(bt.pressed||bt.value>.6))down[MAP[i]]=1});const ax=gp.axes||[];
    if(ax[1]<-.6)down.up=1;if(ax[1]>.6)down.down=1;if(ax[0]<-.6)down.left=1;if(ax[0]>.6)down.right=1;
    if(gp.mapping!=="standard"&&ax.length>9){const h=ax[9];if(h>-1.1&&h<1.1){if(h<-.8||h>.9)down.up=1;if(h>-.75&&h<-.1)down.right=1;if(h>-.2&&h<.45)down.down=1;if(h>.4&&h<1.05)down.left=1}}
    gp.buttons.forEach((bt,i)=>{if(bt.pressed&&!window.__arcLast)window.__arcLast={i,t:now}})}
  if(window.__arcLast){const L=window.__arcLast;window.__arcLast=null;const t=document.getElementById("arctest");if(t)t.textContent="Last button: #"+L.i+(MAP[L.i]?" ("+MAP[L.i]+")":" (not mapped)")}
  for(const k in down){if(!held[k]){held[k]=now;rep[k]=now+380;if(!gameOn)act(k)}else if(["up","down","left","right"].includes(k)&&now>rep[k]){rep[k]=now+150;if(!gameOn)act(k)}}
  for(const k in held)if(!down[k])delete held[k]}
function pads(){return [...(navigator.getGamepads?navigator.getGamepads():[])].filter(Boolean)}
window.addEventListener("gamepadconnected",e=>{if(!raf)poll();const t=document.createElement("div");t.id="gametoast";t.textContent="🎮 "+(e.gamepad.id||"Controller")+" connected";document.body.appendChild(t);setTimeout(()=>t.remove(),3000);const r=document.getElementById("arcrow");if(r)r.outerHTML=arcRow()});
window.addEventListener("gamepaddisconnected",()=>{const r=document.getElementById("arcrow");if(r)r.outerHTML=arcRow()});
if(pads().length)poll();
setInterval(()=>{try{if(!raf&&pads().length){poll();const r=document.getElementById("arcrow");if(r)r.outerHTML=arcRow()}}catch(e){}},700);
document.addEventListener("pointerdown",()=>document.documentElement.classList.remove("pad"),true);
// ---------- settings row ----------
window.arcRow=function(){const p=pads(),seg=(k,on)=>'<span class="seg" style="display:inline-flex;gap:0"><button class="btn sm'+(on?' pri':'')+'" data-arc="'+k+'1">On</button><button class="btn sm'+(!on?' pri':'')+'" data-arc="'+k+'0">Off</button></span>';
  return '<div class="set-row" id="arcrow"><div><b>Arcade mode</b><p>Atmospheric background music in Game mode, sound effects, streaks and XP. Controller: '+
  (p.length?'<span style="color:var(--ok,#3fb37f)">'+esc(p[0].id)+' detected</span> ('+(p[0].mapping==="standard"?"standard layout":"non-standard layout")+') · <b id="arctest">press a button to test</b> — A/B/X/Y answer, D-pad ◀ ▶ previous/next, A next after answering, Y bookmark, ☰ Game mode. Outside questions the D-pad moves and A selects.':'<span style="color:var(--bad)">not detected.</span> <i>('+(navigator.getGamepads?"browser controller support on":"this browser has controller support turned off")+')</i> Turn it on in Xbox (or iOS) mode and pair it with this device (Bluetooth, USB cable or its dongle), click once on this page, then press any button on the controller.')+
  '</p></div><div style="display:flex;flex-direction:column;gap:6px;align-items:flex-end"><span>Music '+seg("m",A.music)+'</span><span>Effects '+seg("s",A.sfx)+'</span></div></div>'};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-arc]");if(!b)return;const k=b.dataset.arc;
  if(k[0]==="m")A.music=k[1]==="1";else A.sfx=k[1]==="1";asave();if(A.music||A.sfx){ac();if(k==="s1")sfx("ok")}
  const r=document.getElementById("arcrow");if(r)r.outerHTML=arcRow();hud()});
}
"""
anchor = "showPicker();\ndbHandles();\n"
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + js, 1)
open(p, "w", encoding="utf-8").write(s)
print("arcade added")
