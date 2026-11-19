import {loadSprites, icon} from "./sprites.js";
import {draw} from "./scene.js";

const $ = id => document.getElementById(id);
const titles=["Tutorial","Level 1 · Harvest","Level 2 · Plant","Level 3 · Timing"];
const goals=["Care for one radish over ten days.","Fill your basket. Visit every plot each day.",
  "Grow crops for coins. Choose which seeds to try first.","Earn coins and finish with zero wasted seeds."];
let catalog, run, frames=[], index=0, progress=1, playing=false, tick=0, raf=0, revision=0, from=0;
let busy=false, connected=false;
const selected=()=>Number($("level").value);
const key=()=>selected()+"/"+$("field").value;
const speed=()=>Number($("speed").value);
const unit=()=>selected()<2?"harvested":"coins";

function controls() {
  $("run").disabled=busy || !connected;
  $("pause").textContent=playing?"Pause":"Resume";
  $("pause").disabled=!run || index===frames.length-1 && progress===1;
  $("next").disabled=!run || index===frames.length-1 && progress===1;
  $("replay").disabled=!run;
}
function stop() {playing=false; cancelAnimationFrame(raf);controls();}
function render() {
  if(!frames.length)return;
  draw(frames[index],frames[index-1],progress,{grow:catalog.grow,level:selected(),from,won:!!run?.stars});
}
function badge(ok) {
  connected=ok;$("badge").textContent=ok?"Connected · your Python":"Disconnected";
  $("badge").classList.toggle("connected",ok);controls();
}
function hud() {
  const s=frames[index].state, setting=catalog.fields[key()];
  $("day").textContent="Day "+s.day+" of 10";
  $("left").hidden=selected()!==3;$("left").textContent=s.days_left+" days left";
  const score=selected()<2?s.basket:s.coins;
  $("score").replaceChildren(icon(selected()<2?"basket":"coin",30),score+" / "+setting.target+" "+unit());
  const eligible=selected()!==3 || !s.wasted;
  const count=eligible && score>=setting.target ? (score>=setting.best?3:2*score>=setting.target+setting.best?2:1):0;
  $("stars").replaceChildren(...Array.from({length:count},()=>icon("star",24)), "☆".repeat(3-count));
  $("stars").setAttribute("aria-label",count+" of 3 stars");
  $("bag").hidden=selected()<2;
  if(selected()>=2) {
    const parts=Object.entries(s.seeds).map(([crop,n])=>{
      const span=document.createElement("span");span.className="stat";
      span.append(icon("packet_"+crop,32,"seed"),crop+" × "+n);
      return span;
    });
    const waste=document.createElement("strong");waste.className="waste";waste.textContent="Wasted seeds · "+s.wasted;
    $("bag").replaceChildren(...parts,waste);
  }
  $("scene").setAttribute("aria-label",s.plots.map((p,i)=>`Plot ${i+1}: ${p.crop}, stage ${p.stage}${p.wet?", wet":""}`).join(". "));
}
function highlight(n) {
  const box=$("source");box.querySelector(".active")?.classList.remove("active");
  const line=n && box.children[n-1];
  if(line){line.classList.add("active");box.scrollTop=line.offsetTop-box.children[0].offsetTop-box.clientHeight/2;}
}
function describe(e){
  if(e.action==="sleep")return "Day "+e.day+" · sleep → "+(e.state.finished?"season complete":"watered crops grow");
  const p=e.state.plots[e.plot];
  const detail=e.message || (e.action==="water"?p.crop+" "+p.stage+"/"+catalog.grow[p.crop]+" · watered":
    e.action==="harvest"?e.crop+(selected()<2?" → basket":" → +"+run.prices[e.crop]+" coins"):e.crop+" seed");
  return "Day "+e.day+" · Plot "+(e.plot+1)+" · "+e.action+" → "+detail;
}
function finish() {
  stop();
  const s=frames[index].state;
  if(run.error) {showResult((run.error.line?"Line "+run.error.line+" · ":"")+run.error.message);highlight(run.error.line);}
  else showResult("Season complete · "+run.stars+" / 3 stars · "+(selected()<2?s.basket:s.coins)+" "+unit()+
      (selected()>=2?" · "+s.wasted+" wasted seeds":""));
}
function showResult(message){$("result").textContent=message;$("result").hidden=false;}
function advance() {
  if(index>=frames.length-1){progress=1;render();finish();return;}
  if(frames[index].plot!=null)from=frames[index].plot;
  index++;progress=0;const e=frames[index];
  const li=document.createElement("li");li.textContent=describe(e);$("log").append(li);
  $("log").scrollTop=$("log").scrollHeight;$("count").textContent=index+" actions";
  highlight(e.line);hud();render();controls();
}
function animate(now) {
  if(!playing)return;
  const ms=(frames[index].action==="sleep"?950:680)*speed();
  progress=Math.min(1,progress+(now-tick)/ms);tick=now;render();
  if(progress===1){if(index===frames.length-1){finish();return;}advance();}
  raf=requestAnimationFrame(animate);
}
function play(){if(!run)return;playing=true;tick=performance.now();controls();raf=requestAnimationFrame(animate);}
function resetTimeline(){
  stop();index=from=0;progress=1;$("log").replaceChildren();$("count").textContent="0 actions";
  $("result").hidden=true;highlight(null);hud();render();controls();
}
function choose(){
  revision++;busy=false;stop();run=null;
  if(selected()===0)$("field").value="challenge";$("field").disabled=selected()===0;
  const setting=catalog.fields[key()];
  frames=[{action:"start",state:setting.state}];
  $("title").textContent=titles[selected()];$("goal").textContent=goals[selected()];$("filename").textContent=setting.filename;
  $("source").textContent="  Save "+setting.filename+" and run your Python.";
  $("prints").textContent="Run your code to see its print output.";resetTimeline();
}
function source(text){
  const lines=text.split("\n").map((s,i)=>{
    const el=document.createElement("div");el.className="line";
    const num=document.createElement("b");num.textContent=i+1;el.append(num,s);return el;
  });$("source").replaceChildren(...lines);
}
async function execute(){
  const token=++revision;stop();busy=true;run=null;controls();
  try {
    const response=await fetch("api/run",{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({level:selected(),field:$("field").value})});
    if(!response.ok)throw Error();
    const data=await response.json();if(token!==revision)return;
    if(!data.events){showResult(data.error?.message||"Save your file and try again.");return;}
    run=data;frames=run.events;source(run.source);$("prints").textContent=run.prints||"(No prints this run.)";
    resetTimeline();
    if(frames.length>1){advance();play();}else finish();
  } catch {if(token===revision)showResult("Could not reach Python. Check the terminal, then reload this page.");}
  finally{if(token===revision){busy=false;controls();}}
}
$("level").onchange=$("field").onchange=choose;$("run").onclick=execute;
$("replay").onclick=()=>{resetTimeline();if(frames.length>1){advance();play();}else finish();};
$("pause").onclick=()=>playing?stop():play();
$("next").onclick=()=>{stop();advance();progress=1;render();if(index===frames.length-1)finish();};
new ResizeObserver(render).observe($("scene").parentElement);
try {
  catalog=await (await fetch("api/levels")).json();
  await loadSprites(catalog.sprites);badge(true);choose();
} catch {badge(false);showResult("Start python play.py and open its forwarded port.");}

