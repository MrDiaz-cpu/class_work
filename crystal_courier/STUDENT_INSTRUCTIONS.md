# Crystal Courier — student mission

**Goal:** Use a function, loops, and decisions to collect every crystal and reach the green exit.

## 1. Get ready

Open cs50.dev. For your first download, run these commands in the terminal:

```bash
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/crystal_courier/crystal_courier.zip
unzip crystal_courier.zip
cd crystal_courier
python play.py
```

If you already have a `crystal_courier` folder with your work, open that folder and run `python play.py`; do not unzip over your saved work.

Open **Ports → 8080 → Open in Browser**. If 8080 is not listed, add/forward port 8080 first. Keep the port **Private**. Leave the terminal running. You will use the cs50.dev editor for Python and the game tab for visuals.

The badge should say **Connected · your Python**. The teacher reference mode is for demonstrations.

## 2. Build the tutorial with your teacher

Open `tutorial.py`. Keep the supplied import line. The first working command is:

```python
move("right")
```

It moves one square, not all the way to the wall. Follow the live example. Save your file, select **Tutorial**, and click **Run saved Python**. Use **Pause** and **Next action** to trace the program. Keep your completed tutorial open as a reference.

| Command | What it does |
|---|---|
| `move("right")` | Move one square right; also accepts `"left"`, `"up"`, `"down"` |
| `on_crystal()` | Return `True` when a crystal is under the robot; otherwise `False` |
| `collect()` | Pick up a crystal on the current square |
| `can_move("right")` | Return whether the adjacent square in that direction is clear |
| `at_exit()` | Return whether the robot is on the exit |

Directions refer to the screen. Right always means right. Sensor functions report information; they do not move or collect anything.

## 3. Complete your mission

Select **Challenge** and open `mission.py`. The starter deliberately does nothing yet. Complete these two functions:

1. `walk(direction, steps)`: Repeat `steps` times. On each repetition, move one square in `direction`. Then check whether you are on a crystal and collect it only if you are.
2. `main()`: Use your `walk` function to complete the staircase. Find the repeated section and use a loop to repeat it. Finish the route to the exit.

Keep the supplied `main()` call at the bottom. Edit only `mission.py` for your independent assignment. Do not change the maps or engine.

**Success criteria**

- Collect all three crystals and finish at the exit in at most 30 moves.
- Use a loop for repeated movement.
- Use your function instead of writing every movement separately.
- Check for a crystal after each move, not only at the end of a corridor.
- Use a loop for the staircase's repeated sections.
- Run **Remix** with the same saved `mission.py`; it must work when the crystals move.

Plan before typing: count squares, identify where direction changes, and circle the section that repeats. You can return over floor, but a short route leaves more room in your move budget. You do not need a pathfinding algorithm.

## 4. Save, run, and debug

1. Save `mission.py` in cs50.dev.
2. Return to the game tab and select **Challenge**.
3. Click **Run saved Python**.
4. Pause or replay to identify the first action that differs from your plan.
5. Change one part of your code, save, and run again.
6. Try **Remix** without editing your route.

Every new run starts fresh. **Replay** repeats the previous run; it does not reread your file. The highlighted Python line caused the action you are watching. The movement log lists the actions so far. Open **Python output** to see any `print` messages.

| If you see… | Check… |
|---|---|
| Robot stays at the start | Did you replace `pass`? Did you call your function? Did you save? |
| A wall error | Did you count moves rather than squares including the starting square? |
| “No crystal here” | Is `collect()` inside `if on_crystal():`? |
| Crystal left behind | Is the check inside the movement loop, immediately after the move? |
| A Python syntax or indentation error | Inspect the indicated line, its colon, and the surrounding indentation. |
| A loop limit | What changes each iteration? When should the condition become false? |

If the browser cannot connect, ask your teacher to check the running terminal and forwarded port. Running `python mission.py` alone does not start the visual player.

## 5. Check with check50

Save `mission.py`. Open a second terminal and enter the folder containing it. Leave the game running in the first terminal.

```bash
check50 MrDiaz-cpu/class_work/main/crystal_courier
```

Read the first red check. Fix your Python, save, and run check50 again. The checks test your functions and both levels. For `walk(direction, 0)`, no movement or collection should occur. A passing checker does not replace explaining your loops and decisions.

## 6. Turn in with submit50

Run this from the same folder:

```bash
submit50 MrDiaz-cpu/class_work/main/crystal_courier
```

Use your own CS50/GitHub sign-in if prompted. Review the files: **only `mission.py` should be listed**. Confirm and keep the returned submission link. Submit your current work before the deadline, even if some checks fail. Tell your teacher if sign-in prevents submission.

`check50` checks your work. `submit50` turns it in. Turn in the exit ticket separately as your teacher directs.

If online check50 is unavailable, try:

```bash
check50 --local MrDiaz-cpu/class_work/main/crystal_courier
```

This runs the GitHub checks in your codespace; it does not submit your work. If you already downloaded the game, you can use these commands immediately without downloading again or overwriting your saved Python.

## Hints — use one at a time

1. How did the tutorial use `range` to repeat one move?
2. The function has two parameters. Which one belongs inside `range`? Which belongs inside `move`?
3. Indentation determines what repeats. Does your crystal check repeat after every move?
4. Read the map as short horizontal and vertical sections. Which pair of sections keeps appearing?

## Stretch

Write a separate function `walk_to_wall(direction)` that moves while the next square is clear and checks for crystals after each move. Try it in your tutorial. Explain why the loop stops. Check what changes if you forget the movement inside it.

## Exit ticket

1. In `walk("right", 3)`, what values do `direction` and `steps` receive?
2. Why should `if on_crystal():` be inside the movement loop?
3. How is `print('move("right")')` different from `move("right")`?
4. What evidence did Remix give you about your program?
