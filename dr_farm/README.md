# Dr. Farm

Give a farmer ten days of Python instructions. First, bring one radish from seed to basket. Then run a whole field, spend a limited seed bag, and plan your last harvest.

## Download and play

Open cs50.dev. In a terminal, start in a folder that has no `dr_farm/` folder yet. **Do not unzip over saved work.** One download has all four levels.

```bash
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/dr_farm/dr_farm.zip
unzip dr_farm.zip
cd dr_farm
python play.py
```

Open **Ports → 8080 → Open in Browser**. Keep the port **Private**. Look for **Connected · your Python**. Pick a level and a field. Edit the matching file in your editor. Save it and click **Run saved Python** in the game. Each run starts on day 1 with a fresh field.

| Pick | Edit | Goal on Challenge / Remix |
|---|---|---|
| Tutorial | `tutorial.py` | Harvest one radish with your teacher |
| Level 1 · Harvest | `level1.py` | Fill the basket with 10 / 14 crops |
| Level 2 · Plant | `level2.py` | Earn 15 / 20 coins |
| Level 3 · Timing | `level3.py` | Earn 15 / 20 coins and waste zero seeds |

**Pause** stops the animation. **Next action** shows one more event and highlights its Python line. **Replay** plays the same run again. To see an edit, save the file and click **Run saved Python**. Read [the student mission](STUDENT_INSTRUCTIONS.md) for the rules.

## Check and turn in your level

Keep the game running. Open a **second terminal** in the folder containing `level1.py`, `level2.py` and `level3.py`. Run the pair for your level. **check50** checks your work. Read the first red check and its hint. **submit50** turns in your saved file. The tutorial is class practice.

```bash
check50 MrDiaz-cpu/class_work/main/dr_farm/level1
submit50 MrDiaz-cpu/class_work/main/dr_farm/level1
```

```bash
check50 MrDiaz-cpu/class_work/main/dr_farm/level2
submit50 MrDiaz-cpu/class_work/main/dr_farm/level2
```

```bash
check50 MrDiaz-cpu/class_work/main/dr_farm/level3
submit50 MrDiaz-cpu/class_work/main/dr_farm/level3
```

## When something looks wrong

| What you see | What to try |
|---|---|
| The farm runs ten days and scores zero | The starter does this. Edit the function marked `pass`, save, and run again. |
| The browser shows old moves | Check the level and filename. Use **Run saved Python**. |
| You see a line number | Find the highlighted line in **Saved Python**. Read the message and check your spelling and spaces. |
| No browser tab opens | Find **Ports** in cs50.dev and open port **8080**. Keep the terminal with the server open. |
| Port 8080 is busy | Stop your old server with Ctrl+C, or run `python play.py --port 8081` and open port 8081. |
| A command cannot find your file | Type `pwd` and `ls`. Open the terminal in the extracted `dr_farm` folder. |
| A picture has a text label | Keep playing. The label stands in for the picture. |

For a quick text score, run `python level1.py` in the game folder. You can do the same with the other level files. The game uses Python 3.9 or newer and a modern browser.
