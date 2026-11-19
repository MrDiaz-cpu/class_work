import {sprite} from "./sprites.js";

const canvas = document.querySelector("#scene");
const ctx = canvas.getContext("2d");
const H = 278;
function box(x,y,w,h,fill,stroke,r=8) {
  ctx.beginPath(); ctx.roundRect(x,y,w,h,r); ctx.fillStyle=fill; ctx.fill();
  if (stroke) {ctx.strokeStyle=stroke; ctx.lineWidth=2; ctx.stroke();}
}
function label(text,x,y,size=15,color="#1a392b") {
  ctx.font="bold "+size+"px system-ui"; ctx.fillStyle=color;
  ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(text,x,y);
}
function cloud(x,y) {
  ctx.fillStyle="#fff9df";
  for (const [dx,dy,r] of [[0,0,12],[15,-6,16],[32,0,12]]) {
    ctx.beginPath();ctx.arc(x+dx,y+dy,r,0,2*Math.PI);ctx.fill();
  }
  ctx.fillRect(x-7,y,48,8);
}
export function draw(frame, previous, progress, context) {
  const {grow,level,from,won}=context;
  const sleep=frame.action==="sleep";
  const state=sleep && progress<.5 && previous ? previous.state : frame.state;
  const plots=state.plots, n=plots.length;
  const W=Math.max(canvas.parentElement.clientWidth, n*104+32,350);
  const d=Math.min(devicePixelRatio||1,2);
  if(canvas.width!==Math.round(W*d)||canvas.height!==Math.round(H*d)) {
    canvas.width=Math.round(W*d);canvas.height=Math.round(H*d);canvas.style.width=W+"px";
  }
  ctx.setTransform(d,0,0,d,0,0);
  ctx.fillStyle="#bce5e4";ctx.fillRect(0,0,W,H);
  cloud(W*.23,33);cloud(W*.62,46);cloud(W*.78,24);
  // Farms on the horizon behind the playable row.
  ctx.fillStyle="#83ad80";ctx.beginPath();ctx.moveTo(0,112);
  for(let x=0;x<=W+10;x+=10)ctx.lineTo(x,98+Math.sin(x/80)*14);
  ctx.lineTo(W,131);ctx.lineTo(0,131);ctx.fill();
  ctx.fillStyle="#76573d";ctx.fillRect(0,119,W,4);ctx.fillRect(0,126,W,3);
  for(let x=10;x<W;x+=42)ctx.fillRect(x,113,5,23);
  ctx.fillStyle="#71ae55";ctx.fillRect(0,133,W,H-133);
  ctx.save();ctx.beginPath();ctx.rect(0,133,W,H-133);ctx.clip();
  for(let x=0;x<W;x+=128)for(let y=133;y<H;y+=128)sprite(ctx,"grass",x,y,128);
  ctx.restore();
  const night=sleep?Math.sin(progress*Math.PI):0;
  if(night>.02){ctx.fillStyle="rgba(20,31,75,"+(night*.82)+")";ctx.fillRect(0,0,W,H);}
  sprite(ctx,night>.35?"moon":"sun",W-70,8,50);
  const span=Math.min(W-30,Math.max(n*124,270));
  const spacing=span/n, pos=i=>(W-span)/2+spacing*(i+.5);
  const tile=Math.min(spacing-10,88);
  plots.forEach((p,i)=>{
    const x=pos(i), top=151, t=p.crop==="empty"?0:grow[p.crop], ready=t && p.stage===t;
    ctx.save();ctx.beginPath();ctx.roundRect(x-tile/2,top,tile,49,6);ctx.clip();
    sprite(ctx,p.wet?"soil_wet":"soil_dry",x-tile/2,top,tile);
    ctx.restore();ctx.beginPath();ctx.roundRect(x-tile/2,top,tile,49,6);ctx.lineWidth=2;ctx.strokeStyle="#223c2a";ctx.stroke();
    if(t){
      const deceased=level===3 && state.finished && p.wasted;
      const kind=ready?"ready":p.stage?"growing":"seed", size=kind==="seed"?34:kind==="ready"?74:54;
      sprite(ctx,deceased?"withered":p.crop+"_"+kind,x-size/2,top+28-size,size);
      if(ready && !deceased){box(x+tile/2-19,top,24,23,"#fff3b0","#26382a");label("✓",x+tile/2-7,top+12);}
    }
    if(p.wet){box(x-tile/2,top+23,24,23,"#fffaf0","#26382a");label("💧",x-tile/2+12,top+35);}
    box(x-tile/2-4,205,tile+8,61,"#fff6dc","#243a28");
    label((i+1)+" · "+p.crop,x,220);
    if(t) {
      for(let k=0;k<t;k++)box(x-t*5+10*k,236,7,8,k<p.stage?"#235d3e":"#fffaf0","#315842",2);
      label(p.stage+" / "+t,x,255,13);
    } else label("open",x,246,14);
  });
  const idx=frame.plot==null ? from : frame.plot;
  const walking=frame.plot!=null && idx!==from && progress<.4;
  const fraction=walking?Math.min(1,progress/.4):1;
  const x=pos(from)+(pos(idx)-pos(from))*fraction;
  let pose="idle";
  if(state.finished)pose=won?"cheer":"sad";
  else if(walking)pose=progress<.2?"walk_1":"walk_2";
  else if(frame.plot!=null)pose=frame.ok?frame.action:"sad";
  sprite(ctx,"farmer_"+pose,x-45,58,90);
  if(frame.ok && frame.plot!=null && progress>=.4 && progress<1) {
    const t=(progress-.4)/.6;
    if(frame.action==="water")sprite(ctx,"water_splash",x+12,136+8*t,34);
    if(frame.action==="plant")sprite(ctx,"packet_"+frame.crop,x-14,116+40*t,32,"seed");
    if(frame.action==="harvest"){
      const end=W-45;
      sprite(ctx,level<2?frame.crop+"_item":"coin",x+(end-x)*t-15,145-90*Math.sin(t*2),31);
      if(level<2)sprite(ctx,"basket",end-24,40,48);
    }
  }
  if(frame.message && progress>=.4){
    ctx.font="bold 16px system-ui";
    const w=Math.min(W-8,ctx.measureText(frame.message).width+24);
    const left=Math.max(4,Math.min(W-w-4,x-w/2));
    box(left,15,w,33,"#fff4d1","#443825");label(frame.message,left+w/2,32,16);
  }
}

