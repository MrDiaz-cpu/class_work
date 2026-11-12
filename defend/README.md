# Defend the Base

**Learning target:** I can use a loop inside a function to update and return a value.

Your base is under attack. The animation is ready, but the towers need your Python function to calculate their damage.

## Download the starter

In a cs50.dev terminal, run these commands once:

```bash
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/defend/defend.zip
unzip defend.zip
cd defend
code tower_demo.py
```

If you already have this lesson's folder, open it instead of downloading over your work.

## First: code together

Follow the class demonstration in **tower_demo.py**. Start with two towers, then write a loop that totals a list of tower damages. Finally, put that loop inside `total_damage(damages)` and return the total. Run your example with:

```bash
python tower_demo.py
```

For `[2, 1]`, the output should be `Damage this turn: 3`. For `[1, 2, 1]`, it should be `Damage this turn: 4`.

Keep this file open as your reference. Your independent work will be in **defenders.py**, a separate file.

## Then: launch your game

1. In the same folder, run `python game.py`.
2. If no browser tab opens, use **Ports → 8080 → Open in Browser**.
3. In the game, check that the badge says **Connected · your Python**.
4. Choose **Raider** and launch the starter. Notice what happens to its health.

Keep the terminal running. Use **Ctrl+C** when you are finished.

## Your task

Complete `attack(health, damages)` in **defenders.py**.

- `health` is a nonnegative integer: the enemy's health before the attack.
- `damages` is a list of nonnegative integers. Each number belongs to one tower.
- Use a **for loop** to subtract every tower's damage from health.
- Return the remaining health as an integer.
- If the result would be negative, return `0` instead.
- An empty list means no towers fire, so health stays the same.
- Return the answer; do not print it. Do not use `sum` or hard-code the sample answers.

Keep the function name and its two parameters. You do not need imports, classes, recursion, or any changes to the server or animation.

| Function call | Return value |
|---|---:|
| `attack(8, [2, 1])` | 5 |
| `attack(2, [2, 1])` | 0 |
| `attack(9, [4])` | 5 |
| `attack(7, [])` | 7 |

## Test, explain, revise

Save **defenders.py**, then click **Launch wave** again. The game reloads your saved function each time.

1. Uncheck **Autoplay**. Predict each return value before selecting **Next turn**.
2. Test **Scout** and **Raider**. Do the battle logs match your predictions?
3. Test **Three towers**. Does your function use all three entries in the list?
4. Predict and test **Tank**. A correct function does not guarantee a victory: explain why this wave reaches the base.

Read the **Battle log** to see the actual values returned by your Python. The animation is showing those results.

## Check and turn in

Open a second terminal in the same folder:

```bash
check50 MrDiaz-cpu/class_work/main/defend
```

Fix any failing checks, then submit from the folder containing **defenders.py**:

```bash
submit50 MrDiaz-cpu/class_work/main/defend
```

Only **defenders.py** is submitted. Keep the submission confirmation link and give your exit-ticket answers to your teacher by the end of class. Do not submit `tower_demo.py`, the server, or the graphics.

If sign-in prevents submission, tell your teacher before the bell. The bundled checks can also run locally with `check50 --dev checks/defend`.

## Exit ticket

1. What is the return value of `attack(10, [3, 0, 2])`? Show health after each loop iteration.
2. In our game, what does the `while` loop repeat, and what does your `for` loop repeat?
3. Why must the function return a number instead of only printing it?

**Finished early?** Find the greatest starting health that `[2, 1]` can defeat in three turns. Explain your reasoning, then predict the answer for `[1, 2, 1]`.
