import {sprite, walkFrames} from "./sprites.js";

const canvas = document.querySelector("#scene");
const ctx = canvas.getContext("2d");
const H = 278;
const soilTop = 151;
const ground = soilTop + 28;
const gripAt = .32;
const pullAt = .47;
const freeAt = .69;
const throwAt = .77;
export const rewardAt = .96;

function ease(p, start, end) {
  const t = Math.max(0, Math.min(1, (p - start) / (end - start)));
  return t * t * (3 - 2 * t);
}

export function isHarvest(frame) {
  return frame.action === "harvest" && frame.ok && frame.plot != null;
}

// The extended boots mark opposite footfalls. The three similar knee lifts
// pass quickly so the advancing foot doesn't hang in the air.
const walkPoseEnds = [.10, .21, .34, .40, .46, .50, .72, 1];
function drawWalk(start, end, fraction) {
  const distance = end - start;
  const steps = Math.max(1, Math.round(Math.abs(distance) / 38));
  const phase = (.055 + fraction * steps / 2) % 1;
  const pose = walkFrames[walkPoseEnds.findIndex(limit => phase < limit)];
  sprite(ctx, pose, start + distance * fraction - 45, 58, 90, "walk", distance < 0);
}

// Hold one boot against the bed. The produce follows the same transform as
// the hands until release, so it cannot drift away when the farmer leans back.
function drawHarvest(crop, x, width, level, progress) {
  const pull = ease(progress, pullAt, freeAt);
  const crouch = ease(progress, gripAt, pullAt) * (1 - pull);
  const flight = ease(progress, throwAt, rewardAt);
  const recover = ease(progress, throwAt, 1);
  const picked = ease(progress, freeAt - .035, freeAt);
  const tilt = -.58 * pull;
  const stretch = 1 - .20 * crouch;
  const size = 108;
  const footX = x - 42, footY = ground + 2;
  const reach = 42, rise = -27 * stretch;
  const handX = footX + reach * Math.cos(tilt) - rise * Math.sin(tilt);
  const handY = footY + reach * Math.sin(tilt) + rise * Math.cos(tilt);
  const endX = Math.min(x + 76, width - 26), endY = ground - 14;
  const itemSize = 52 - 21 * flight;
  const itemX = handX + (endX - handX) * flight;
  const itemY = handY + (endY - handY) * flight - 42 * Math.sin(Math.PI * flight);
  const sold = level >= 2;
  if (!sold) sprite(ctx, "basket", endX - 23, endY - 17, 46);

  // The root starts partially buried. Drawing only above the soil line
  // reveals it naturally as the hands pull it out.
  ctx.save();
  ctx.beginPath(); ctx.rect(0, 0, width, ground - 7); ctx.clip();
  if (progress < freeAt) {
    ctx.globalAlpha = 1 - picked;
    const lift = pull > 0 ? handY - (footY - 27 * .8) : 0;
    sprite(ctx, crop + "_ready", handX - 37, ground - 74 + lift, 74);
  }
  ctx.globalAlpha = picked * (sold ? 1 - ease(progress, throwAt, throwAt + .06) : 1);
  if (ctx.globalAlpha > 0 && flight < 1)
    sprite(ctx, crop + "_item", itemX - itemSize / 2, itemY - .40 * itemSize, itemSize);
  ctx.restore();

  if (recover < .72) {
    ctx.save();
    ctx.translate(footX + 30 * recover, footY - 35 * recover);
    ctx.rotate(tilt * (1 - recover));
    const scale = 1 - .16 * recover;
    ctx.scale(scale, stretch * scale);
    sprite(ctx, "farmer_harvest", -.31 * size, -.94 * size, size);
    ctx.restore();
  } else {
    sprite(ctx, "farmer_idle", x - 45 - 30 * (1 - recover), 58 + 35 * (1 - recover), 90);
  }

  if (pull > 0 && pull < 1) {
    ctx.fillStyle = "#5e3d2d";
    for (const offset of [-11, 8, 15]) {
      ctx.fillRect(x + offset * pull, ground - 9 * Math.sin(Math.PI * pull), 3, 3);
    }
  }
  if (sold && progress > throwAt && flight < 1) {
    ctx.save();
    ctx.globalAlpha = ease(progress, throwAt, throwAt + .06);
    sprite(ctx, "coin", itemX - 15, itemY - 15, 30);
    ctx.restore();
  }
}

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
  const {grow,level,from,won,walkFraction=1}=context;
  const walking=walkFraction<1;
  const sleep=frame.action==="sleep";
  const state=previous && (walking || sleep && progress<.5) ? previous.state : frame.state;
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
  const harvesting = isHarvest(frame);
  plots.forEach((after,i)=>{
    const active = harvesting && !walking && i === frame.plot;
    const p = active && progress < freeAt && previous ? previous.state.plots[i] : after;
    const x=pos(i), top=soilTop, t=p.crop==="empty"?0:grow[p.crop], ready=t && p.stage===t;
    ctx.save();ctx.beginPath();ctx.roundRect(x-tile/2,top,tile,49,6);ctx.clip();
    sprite(ctx,p.wet?"soil_wet":"soil_dry",x-tile/2,top,tile);
    ctx.restore();ctx.beginPath();ctx.roundRect(x-tile/2,top,tile,49,6);ctx.lineWidth=2;ctx.strokeStyle="#223c2a";ctx.stroke();
    if(t && !(active && progress >= gripAt && progress < freeAt)){
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
  const x=pos(idx);
  if (walking) {
    drawWalk(pos(from), x, walkFraction);
    return;
  }
  let pose="idle";
  if(state.finished)pose=won?"cheer":"sad";
  else if(frame.plot!=null)pose=frame.ok?frame.action:"sad";
  if (harvesting && progress >= gripAt && progress < 1) {
    drawHarvest(frame.crop, pos(idx), W, level, progress);
  } else if (harvesting && progress < gripAt) {
    const approach = ease(progress, 0, gripAt);
    sprite(ctx, "farmer_idle", x - 45 - 25 * approach, 58 + 24 * approach, 90);
  } else {
    sprite(ctx, "farmer_"+(harvesting ? "idle" : pose),x-45,58,90);
  }
  if(frame.ok && frame.plot!=null && progress>=.4 && progress<1) {
    const t=(progress-.4)/.6;
    if(frame.action==="water")sprite(ctx,"water_splash",x+12,136+8*t,34);
    if(frame.action==="plant")sprite(ctx,"packet_"+frame.crop,x-14,116+40*t,32,"seed");
  }
  if(frame.message && progress>=.4){
    ctx.font="bold 16px system-ui";
    const w=Math.min(W-8,ctx.measureText(frame.message).width+24);
    const left=Math.max(4,Math.min(W-w-4,x-w/2));
    box(left,15,w,33,"#fff4d1","#443825");label(frame.message,left+w/2,32,16);
  }
}

