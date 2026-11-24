# Dr. Farm sprite manifest

Use square PNG files. Put the files in `dr_farm/game/web/sprites/`. The browser loads these exact base names with a `.png` extension.

| Group | File names |
|---|---|
| Farmer actions | `farmer_idle`, `farmer_water`, `farmer_harvest`, `farmer_plant`, `farmer_cheer`, `farmer_sad` |
| Farmer walk | `farmer_walk_1`, `farmer_walk_2`, `farmer_walk_3`, `farmer_walk_4`, `farmer_walk_5`, `farmer_walk_6`, `farmer_walk_7`, `farmer_walk_8` |
| Tiles | `soil_dry`, `soil_wet`, `grass` |
| Radish | `radish_seed`, `radish_growing`, `radish_ready`, `radish_item` |
| Carrot | `carrot_seed`, `carrot_growing`, `carrot_ready`, `carrot_item` |
| Corn | `corn_seed`, `corn_growing`, `corn_ready`, `corn_item` |
| Pumpkin | `pumpkin_seed`, `pumpkin_growing`, `pumpkin_ready`, `pumpkin_item` |
| Seed packets | `packet_radish`, `packet_carrot`, `packet_corn`, `packet_pumpkin` |
| Other | `withered`, `basket`, `coin`, `water_splash`, `star`, `sun`, `moon` |

The eight walk frames face right and are numbered in playback order. Frames 1 and 7 show opposite boots stepping forward. To replace them, use one scale for the whole sheet, keep the waist centered, and align the lowest boot to the same ground line in each square. The supplied frames use row 246 on a 256-pixel square. The game mirrors them for the return trip.

Crops sit on top of soil. Stage zero uses the seed image. Middle stages share the growing image. Full pips select the ready image. The item image represents picked produce. During a harvest the game holds one boot against the bed and lines up the crop with the farmer’s hands. The supplied harvest drawing includes its own root and mound. The `harvestActor` outline in `game/web/sprites.js` isolates the farmer for playback. If you replace that drawing with an empty-handed pose, set the outline to `null`. Place the hands about 70% across and 69% down the square.

Transparent PNGs retain their alpha channel. For an opaque sprite, use a solid background, preferably `#FF00FF`. The loader samples the corners and removes matching pixels with a tolerance. Full-bleed grass and soil keep their natural backgrounds. Missing images get labeled placeholders. To change smooth scaling to sharp pixels, set `PIXEL_ART` to `true` in `game/web/sprites.js`.

This edition includes 40 images. The four seed packets use labeled placeholders. The growing and ready stages share the same pip scale even when their drawings differ in size.

From the repository’s `dr_farm/` directory:

```bash
python tools/build.py
```

Commit the added PNGs and rebuilt `dr_farm.zip` together. The same build refreshes trusted Python files in each check folder. Grading uses Python alone.
