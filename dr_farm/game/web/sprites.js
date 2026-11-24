// Change this one setting for crisp pixels when a square is enlarged.
export const PIXEL_ART = false;
const crops = ["radish", "carrot", "corn", "pumpkin"];
export const walkFrames = Array.from({length: 8}, (_, i) => "farmer_walk_" + (i + 1));
export const manifest = [
  "farmer_idle", ...walkFrames, "farmer_water", "farmer_harvest",
  "farmer_plant", "farmer_cheer", "farmer_sad", "soil_dry", "soil_wet", "grass",
  ...crops.flatMap(c => ["seed", "growing", "ready", "item"].map(s => c + "_" + s)),
  ...crops.map(c => "packet_" + c),
  "withered", "basket", "coin", "water_splash", "star", "sun", "moon"
];
const images = new Map();

// The supplied 256-unit harvest illustration contains a turnip and a mound.
// Isolate its farmer and fingers so each plot can supply the crop being pulled.
// For replacement art with empty hands, set this outline to null.
const harvestActor = new Path2D(
  "M0 0 H166 V146 L171 154 L174 164 L180 173 L179 182 L169 190 " +
  "L158 187 L150 182 L146 184 L151 191 L153 203 L164 209 L164 216 " +
  "L175 225 L175 235 L162 248 H0 Z M182 171 L187 165 L196 162 " +
  "L197 169 L193 180 L190 185 L183 183 Z"
);
const tileNames = new Set(["soil_dry", "soil_wet", "grass"]);
document.documentElement.classList.toggle("pixel-art", PIXEL_ART);

function close(a, b) {
  return Math.max(...a.map((v, i) => Math.abs(v - b[i]))) <= 52;
}

export function keyBackground(canvas, name) {
  const ctx = canvas.getContext("2d", {willReadFrequently: true});
  const w = canvas.width, h = canvas.height;
  const pixels = ctx.getImageData(0, 0, w, h);
  const a = pixels.data;
  for (let i = 3; i < a.length; i += 4) if (a[i] !== 255) return canvas;
  const rgb = p => Array.from(a.slice(p * 4, p * 4 + 3));
  const corners = [0, w - 1, w * (h - 1), w * h - 1].map(rgb);
  const key = corners.find(c => corners.filter(other => close(other, c)).length >= 3);
  // Full-bleed ground tiles have real soil/grass at their corners.
  if (!key || (tileNames.has(name) && !close(key, [255, 0, 255]))) return canvas;
  for (let i = 0; i < a.length; i += 4) {
    if (Math.abs(a[i] - key[0]) <= 52 && Math.abs(a[i + 1] - key[1]) <= 52 &&
        Math.abs(a[i + 2] - key[2]) <= 52) a[i + 3] = 0;
  }
  ctx.putImageData(pixels, 0, 0);
  return canvas;
}

export async function loadSprites(available) {
  await Promise.all(manifest.filter(name => available.includes(name)).map(async name => {
    try {
      const img = new Image();
      img.src = "sprites/" + name + ".png";
      await img.decode();
      const c = document.createElement("canvas");
      // Bound decoded working memory even when the teacher supplies large PNGs.
      c.width = c.height = Math.min(512, img.naturalWidth);
      const ctx = c.getContext("2d", {willReadFrequently: true});
      ctx.imageSmoothingEnabled = !PIXEL_ART;
      ctx.drawImage(img, 0, 0, c.width, c.height);
      keyBackground(c, name);
      if (name === "farmer_harvest" && harvestActor) {
        ctx.save();
        ctx.scale(c.width / 256, c.height / 256);
        ctx.globalCompositeOperation = "destination-in";
        ctx.fill(harvestActor);
        ctx.restore();
      }
      images.set(name, c);
    } catch { /* A missing or unreadable image gets the labeled tile below. */ }
  }));
}

export function sprite(ctx, name, x, y, size, label, mirror = false) {
  ctx.imageSmoothingEnabled = !PIXEL_ART;
  if (images.has(name)) {
    if (mirror) {
      ctx.save();
      ctx.translate(2 * x + size, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(images.get(name), x, y, size, size);
    if (mirror) ctx.restore();
    return;
  }
  ctx.save();
  ctx.fillStyle = "#fff4d6"; ctx.strokeStyle = "#283a2b"; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.roundRect(x+1,y+1,size-2,size-2,Math.min(8,size/5));
  ctx.fill(); ctx.stroke();
  ctx.fillStyle = "#203429"; ctx.textBaseline = "middle"; ctx.textAlign = "center";
  const words = (label || name.replaceAll("_"," ")).split(" ");
  const fs = Math.max(10, Math.min(16, size / 3.5));
  ctx.font = "bold " + fs + "px system-ui";
  words.forEach((w,i) => ctx.fillText(w, x+size/2, y+size/2+(i-(words.length-1)/2)*fs, size-4));
  ctx.restore();
}

export function icon(name, size = 32, label = "") {
  const c = document.createElement("canvas");
  const d = Math.min(devicePixelRatio || 1, 2);
  c.width = c.height = size * d;
  c.style.width = c.style.height = size + "px";
  c.setAttribute("aria-hidden","true");
  const ctx = c.getContext("2d");
  ctx.scale(d,d);
  sprite(ctx, name, 0, 0, size, label);
  return c;
}

