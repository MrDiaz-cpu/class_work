# Dr. Farm

You have ten days to run a farm. On the third morning, your first radish is ripe. If your program tells the farmer to water it again, how many radishes will be in your basket?

In this problem, you'll write a Python function that chooses one action for a plot of land. Then you'll use a loop to apply that decision to a whole field. Work through the **Tutorial** with your teacher. For **Levels 1–3**, write and test your own functions. Each level has its own file and its own submission.

[Watch the farmer harvest a radish.](https://github.com/MrDiaz-cpu/class_work/blob/main/dr_farm/harvest.gif)

## Before you begin

### 1. Get the starter code

1. Open [cs50.dev](https://cs50.dev/) and sign in. When the editor loads, click **Terminal** in the bottom panel. If the panel is closed, use the **Terminal** menu and choose **New Terminal**.
2. Click next to the terminal prompt (usually `$`). Type each command in its own line and press **Enter** after each. Start with these two:

   ```bash
   cd
   ls
   ```

   `cd` takes you to your starting folder. `ls` lists what's inside. **If you already see a folder named `dr_farm`, skip to step 4** so you keep your saved work.
3. Download the starter files and extract them. If you already see `dr_farm.zip` but no `dr_farm` folder, use just the second command.

   ```bash
   wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/dr_farm/dr_farm.zip
   unzip dr_farm.zip
   ```

4. Enter the game folder and check its contents:

   ```bash
   cd dr_farm
   ls
   ```

   Look for `play.py`, `tutorial.py`, `level1.py`, `level2.py`, and `level3.py`. You'll use this same folder for the entire assignment.

### 2. Open the game

1. In that terminal, run:

   ```bash
   code tutorial.py
   python play.py
   ```

   The first command opens your Python file for editing. The second starts the game server. Look for **Dr. Farm is running at http://localhost:8080**. Leave this terminal running while you play.
2. In the bottom panel of cs50.dev, click **Ports**. Find **8080**, right-click its row, and choose **Open in Browser**. Keep the port's visibility set to **Private**.
3. Keep both browser tabs open. Write and save code in the **cs50.dev** tab. In the **Dr. Farm** tab, look for **Connected · your Python** and select **Tutorial** in the **Level** menu.
4. Click **Run saved Python**. The starter runs ten days and finishes with **0 harvested**. Back in the editor, find the word `pass` inside `tend(plot)`. In Python, `pass` means “do nothing.” This is where your first instruction goes.

## Tutorial · Can you harvest one radish?

A **plot** is one patch of soil. Python represents it with a dictionary. For instance, `{"crop": "radish", "ready": False}` means this plot holds a growing radish. When `plot["ready"]` becomes `True`, the farmer can pick it. Each plot gets **one action per day**. Even an unsuccessful action uses its turn.

1. **Try watering.** In `tutorial.py`, replace only `pass` with `water(plot)`. Keep the four spaces at the start of that line. Leave the imports at the top and the supplied `main()` below your function in place. Save with **Ctrl+S** (Mac: **Command+S**).
2. **Predict, then run.** What will be in the basket on day 3? In the game tab, click **Run saved Python**. Click **Pause**, then **Next action** to advance one entry at a time. Read the **Action log** alongside the highlighted line in **Saved Python**. A watered radish grows when the supplied loop calls `sleep()`. After nights 1 and 2 it is ripe. Watering on day 3 gives **Already ripe!** The basket still holds **0**.
3. **Teach the farmer when to pick.** Back in `tend(plot)`, use an `if` to ask whether `plot["ready"]` is true. In that branch, call `harvest(plot)`. Under `else`, call `water(plot)`. Indent each action one level inside its branch.
4. **Test your prediction.** Save and click **Run saved Python** again. Your first harvest should appear on **day 3**. Each harvest automatically replants a radish, so you can harvest again on **days 6 and 9**. The final basket holds **3**. Use **Replay** to watch that same run again. After an edit, use **Run saved Python** to start a fresh season.

The tutorial is practice. Your first submission is Level 1.

## Level 1 · Harvest a whole field

In `level1.py`, implement `tend(plot)` and `work_day(field)`. A **field** is a Python list of plots. The Challenge field has six plots. Remix has eight. The same code must handle both.

1. In the cs50.dev **Explorer** (the file list on the left), expand `dr_farm` and click `level1.py`. Find the two lines that say `pass`. Keep the supplied `main()` and the imports in each level file.
2. In `tend(plot)`, reuse your tutorial decision. A ready crop goes in the basket. A growing crop needs water.
3. In `work_day(field)`, write a `for` loop that visits every plot in the list it receives. Inside the loop, call `tend` once with the plot from that pass. The supplied `main()` already repeats the work for ten days and calls `sleep()` after the whole field has had a turn.
4. **Test it.** Save. In the game, choose **Level 1 · Harvest**, set **Field** to **Challenge**, and click **Run saved Python**. In the log for day 1, you should see all **six** plots watered before the first sleep. Finish with **at least 10 crops**. Switch to **Remix** and run again with the same code. Finish with **at least 14 crops**. Once both fields pass, [check](#how-to-check) and [submit](#how-to-submit) Level 1.

## Level 2 · Plant from a seed bag

In `level2.py`, implement `tend(plot)` and `work_day(field)` for a farm that starts empty. Each harvest now earns coins and leaves behind an empty plot. The farmer must decide what to plant there.

| Crop | Watering days needed | Coins per harvest |
| --- | ---: | ---: |
| Radish | 2 | 1 |
| Carrot | 3 | 2 |
| Corn | 4 | 4 |
| Pumpkin | 5 | 7 |

1. Open `level2.py` in the Explorer. Bring over your Level 1 field loop. In `tend(plot)`, keep the decisions for growing and ready crops and add a case for `plot["crop"] == "empty"`. An empty plot has `"ready": False` too, so check for empty soil before deciding to water.
2. For an empty plot, look through the seed bag. `seeds` is a dictionary. In a loop such as `for crop in seeds:`, `crop` is the name of a crop and `seeds[crop]` is the number of its seeds left. If that count is zero, keep looking.
3. When you find a seed in stock, call `plant(plot, crop)`. The game takes one seed out of the bag. Use `break` to leave the **seed loop** after planting. The **field loop** still has to visit the next plot. If every count is zero, leave the soil empty.
4. **Test it.** Save. Select **Level 2 · Plant** and run **Challenge**. On day 1, you should see one planting action per plot. On day 2, those crops need water. Earn **at least 15 coins** on Challenge and **at least 20 coins** on Remix. Click **Run saved Python** each time you switch fields. Then [check](#how-to-check) and [submit](#how-to-submit) Level 2.

## Level 3 · Make the last planting count

In `level3.py`, implement `tend(plot, days_left)` and `work_day(field, days_left)`. Earn coins while finishing with **zero wasted seeds**. The game counts a seed as wasted if you plant it too late to harvest by day 10.

1. Open `level3.py`. Start with your Level 2 decisions, keeping the Level 3 function headers. The supplied `main()` gives `work_day` the number of full days **after today**. On day 1, `days_left` is 9. On day 10, it is 0.
2. In your field loop, pass both the current plot and `days_left` to `tend` on every visit.
3. In your seed loop, check the stock **and** the time. `grow_days[crop]` tells you how many days you'll need to water after planting. You'll also need one more day to harvest. If a seed takes too long, keep looking. If none fits, leave the plot empty.

   | If you plant a radish on… | Days available after planting | Can you harvest? |
   | --- | ---: | --- |
   | Day 7 | 3 | Yes. Water on days 8 and 9, then harvest on day 10. |
   | Day 8 | 2 | No. The second watering uses day 10. |

4. **Test it.** Save. Select **Level 3 · Timing**. Run **Challenge**, then **Remix**. You need **at least 15 coins** on Challenge and **at least 20 coins** on Remix, with **0 wasted seeds on each**. If the log says **Won't ripen in time!**, inspect the planting day and count forward to the harvest day. Once both fields pass, check and submit Level 3 below.

## How to check

After finishing each numbered level, use `check50` to test your saved file. It also tries a field you haven't seen.

1. Save the file in the editor. In the cs50.dev **Explorer**, right-click the **dr_farm** folder and choose **Open in Integrated Terminal**. This opens a second terminal in the right folder while the game keeps running in the first one.
2. Type `ls` and press **Enter**. You should see `level1.py`, `level2.py`, and `level3.py`. Run **only the command for the level you just finished**.

   | Level | Command |
   | --- | --- |
   | 1 | `check50 MrDiaz-cpu/class_work/main/dr_farm/level1` |
   | 2 | `check50 MrDiaz-cpu/class_work/main/dr_farm/level2` |
   | 3 | `check50 MrDiaz-cpu/class_work/main/dr_farm/level3` |

3. A green `:)` marks a passing check. If you see a red `:(`, read the first one. Open the results link for details, change your Python, save, and run the same command again.

## How to submit

1. In the same second terminal, run the command for the level you're turning in. Each command submits one Python file.

   | File to turn in | Command |
   | --- | --- |
   | `level1.py` | `submit50 MrDiaz-cpu/class_work/main/dr_farm/level1` |
   | `level2.py` | `submit50 MrDiaz-cpu/class_work/main/dr_farm/level2` |
   | `level3.py` | `submit50 MrDiaz-cpu/class_work/main/dr_farm/level3` |

2. Read the filename that `submit50` lists. If it matches your level, follow the prompt to confirm. Wait for the submission result and open the link it prints. A successful submission for Level 1 turns in `level1.py`. Repeat this step when you finish each later level.

## If you get stuck

| What you see | What to do |
| --- | --- |
| You came back another day and the farm tab is disconnected. | In cs50.dev, right-click your existing `dr_farm` folder and choose **Open in Integrated Terminal**. Run `python play.py`, then open **Ports → 8080 → Open in Browser** again. |
| The terminal says it can't open `play.py` or find a level file. | Type `pwd` to see your current folder and `ls` to see its files. Open a terminal from the `dr_farm` folder as described above. |
| Port 8080 is busy. | If your game is already running, open its port under **Ports**. To start a second server, run `python play.py --port 8081` and open port **8081**. |
| The browser keeps showing an old move. | Check the filename above **Saved Python**. Open that same file in cs50.dev, save it, and click **Run saved Python**. |
| You see **Already worked here today!** | Pause and read the two log entries for that plot on that day. Find the line that asks for a second action. In Levels 2 and 3, check where your seed loop stops. |
| You want to see what a function received. | Put `print(plot)` inside `tend`, save, and run. Look under **Your prints** in the game tab. |

For a quick score in the second terminal, run `python level1.py` (or `python level2.py` or `python level3.py`). This prints the result for Challenge. Use the game tab to see the animation and test Remix.

For field layouts and starting seed counts, see [the student field guide](STUDENT_INSTRUCTIONS.md).
