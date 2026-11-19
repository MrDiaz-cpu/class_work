# Your ten-day farm

Can the same Python function take care of one radish and a field of eight crops? Start with the tutorial. Keep the imports and the supplied `main()` in every file. Write your decisions inside the functions above `main()`.

## Read a plot

A plot is a dictionary. For example, `{"crop": "corn", "ready": False}` means corn is growing. Read `plot["crop"]` to get its name. Read `plot["ready"]` to find out if you can harvest. A field is a list of these plots. The farm updates the values after each action. Changing a dictionary yourself earns nothing.

| Action | What it does |
|---|---|
| `water(plot)` | Marks a growing plant as wet. It gains one pip tonight. |
| `harvest(plot)` | Picks a ripe crop. Look for the check mark. |
| `plant(plot, crop)` | Uses one seed in an empty plot in Levels 2 and 3. |
| `sleep()` | Ends the day. The day loop already calls it. |

Each plot gets one turn per day. Even a failed action uses its turn. A dry plant stays at the same stage. A ripe plant can wait. A new seed starts with zero pips.

| Crop | Waterings to ripen | Coins per harvest in Levels 2 and 3 |
|---|---:|---:|
| radish | 2 | 1 |
| carrot | 3 | 2 |
| corn | 4 | 4 |
| pumpkin | 5 | 7 |

## Tutorial · One radish

Open `tutorial.py`. With your teacher, change `tend(plot)` so it waters the radish. Predict what the basket will show after ten days. Run it and watch nights 1 and 2. A full row of pips means the radish is ready.

Now make a decision. When the radish is ready, which action puts it in the basket? What should the farmer do on other days? Try the change and look for the first harvest in the log. One harvest earns a star. Three fills the star meter.

## Level 1 · Harvest

Open `level1.py`. Each plot starts planted. Harvesting adds one crop to your basket and puts a new seed of the same kind in that spot.

1. Write `tend(plot)`. Choose one action for the plot you receive.
2. Write `work_day(field)`. Use a `for` loop to visit every plot in the list and call `tend` once for each one.
3. Run Challenge. Then switch to Remix. What did your loop do with the two extra plots?

| Field | Starting crops, left to right | Basket target |
|---|---|---:|
| Challenge | radish, carrot, corn, radish, pumpkin, carrot | 10 |
| Remix | corn, radish, radish, pumpkin, carrot, radish, corn, carrot | 14 |

## Level 2 · Plant

Open `level2.py`. Every plot starts empty. A harvest now earns coins and leaves an open plot. Keep your growing and ready branches. Add a branch for `"empty"`.

The seed bag is a dictionary. For example, `seeds["corn"]` tells you how many corn seeds remain. Inside your visit to an empty plot, loop through the crop names. Check each count. When you plant one seed, `break` out of the seed loop. If all counts are zero, leave that plot alone. The next plot still gets its turn.

You can visit names in bag order with `for crop in seeds:` or make your own ordered list of the four crop names. Try two orders and compare their scores. You can meet the target with either order.

| Field | Plots | Radish | Carrot | Corn | Pumpkin | Coin target |
|---|---:|---:|---:|---:|---:|---:|
| Challenge | 6 | 3 | 3 | 2 | 1 | 15 |
| Remix | 8 | 4 | 4 | 3 | 1 | 20 |

## Level 3 · Timing

Open `level3.py`. The supplied loop sends `days_left` into `work_day(field, days_left)`. Pass that number to `tend(plot, days_left)` on each visit. It counts full days **after today**. It is 9 on day 1 and 0 on day 10.

`grow_days[crop]` tells you how many watering days a new crop needs. It also needs a separate harvest day. If your first seed takes too long, keep looking in the bag. A late seed counts as wasted the moment you plant it.

| Plant a radish today | What happens |
|---|---|
| Day 7, three days left | Water on days 8 and 9. Harvest on day 10. |
| Day 8, two days left | Water on days 9 and 10. The season ends before harvest. |

| Field | Plots | Radish | Carrot | Corn | Pumpkin | Goal |
|---|---:|---:|---:|---:|---:|---|
| Challenge | 6 | 4 | 3 | 3 | 3 | 15 coins, zero waste |
| Remix | 8 | 6 | 4 | 4 | 3 | 20 coins, zero waste |

## Read a run

Use **Next action** to match a log entry to its Python line. A droplet marks wet soil. During sleep the moon comes out, the wet crop grows one pip, and the next day begins. To inspect a value, try `print(plot)` inside your function. Your output appears in **Your prints**.

One star means you hit the target. Two means you are at least halfway from the target to the best score. Three means you reached the best score. In Level 3 you also need zero waste. For grading, check50 tries individual decisions and a new field too. Use the exact commands for your level in [the README](README.md).
