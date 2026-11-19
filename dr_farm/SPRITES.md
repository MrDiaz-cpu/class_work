# Dr. Farm sprite manifest

Use square PNG files. Put the files in `dr_farm/game/web/sprites/`. The browser loads these exact base names with a `.png` extension.

| Group | File names |
|---|---|
| Farmer | `farmer_idle`, `farmer_walk_1`, `farmer_walk_2`, `farmer_water`, `farmer_harvest`, `farmer_plant`, `farmer_cheer`, `farmer_sad` |
| Tiles | `soil_dry`, `soil_wet`, `grass` |
| Radish | `radish_seed`, `radish_growing`, `radish_ready`, `radish_item` |
| Carrot | `carrot_seed`, `carrot_growing`, `carrot_ready`, `carrot_item` |
| Corn | `corn_seed`, `corn_growing`, `corn_ready`, `corn_item` |
| Pumpkin | `pumpkin_seed`, `pumpkin_growing`, `pumpkin_ready`, `pumpkin_item` |
| Seed packets | `packet_radish`, `packet_carrot`, `packet_corn`, `packet_pumpkin` |
| Other | `withered`, `basket`, `coin`, `water_splash`, `star`, `sun`, `moon` |

Align the farmer’s feet in the same place in each square. The game scales every frame around the same anchor. Crops sit on top of soil. Stage zero uses the seed image. Middle stages share the growing image. Full pips select the ready image. The item image represents picked produce.

Transparent PNGs retain their alpha channel. For an opaque sprite, use a solid background, preferably `#FF00FF`. The loader samples the corners and removes matching pixels with a tolerance. Full-bleed grass and soil keep their natural backgrounds. Missing images get labeled placeholders. To change smooth scaling to sharp pixels, set `PIXEL_ART` to `true` in `game/web/sprites.js`.

This edition includes 31 supplied images. The second walk frame, harvest pose, radish item and four seed packets use placeholders until matching PNGs are added. The supplied art was resized for the web. The growing and ready stages share the same pip scale even when their drawings differ in size.

From the repository’s `dr_farm/` directory:

```bash
python tools/build.py
```

Commit the added PNGs and rebuilt `dr_farm.zip` together. The same build refreshes trusted Python files in each check folder. Grading uses Python alone.
