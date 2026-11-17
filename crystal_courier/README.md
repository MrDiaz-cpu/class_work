# Crystal Courier

A visual Python game for the bridge between CS50P Weeks 2 and 3. Program a robot to collect crystals and reach the exit.

## Start in cs50.dev

For your first download:

```bash
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/crystal_courier/crystal_courier.zip
unzip crystal_courier.zip
cd crystal_courier
python play.py
```

Open **Ports → 8080 → Open in Browser**. If necessary, add/forward port `8080` first. Keep the port **Private** and leave the terminal server running.

If you already have a folder with your work, open it and run `python play.py`; do not unzip over your saved Python. If port 8080 is occupied, use `python play.py --port 8081` and open port 8081.

## Tutorial, challenge, remix

1. Code along with your teacher in `tutorial.py` and select **Tutorial**.
2. Complete `mission.py` to collect every crystal and reach the exit in **Challenge**.
3. Run **Remix** with the same saved code and new crystal positions.

Edit Python in cs50.dev, save, then click **Run saved Python** in the game tab. Every run starts fresh. **Replay** replays the previous result. The page highlights the Python line behind each move; use **Pause** and **Next action** to trace it.

[Read the full student instructions](STUDENT_INSTRUCTIONS.md).

![Game board rendered from the game drawing code](preview.png)

## Commands

| Command | Result |
|---|---|
| `move("right")` | Move one square; also accepts `"left"`, `"up"`, `"down"` |
| `on_crystal()` | Return whether a crystal is under the robot |
| `collect()` | Pick up the crystal on the current square |
| `can_move("right")` | Return whether the adjacent square is clear |
| `at_exit()` | Return whether the robot is on the exit |

Student work uses functions, arguments, loops, and conditionals. The import line, Python engine, and browser graphics are supplied. No package installation is needed (Python 3.9+ and a modern browser).

## Check with check50

Save `mission.py`. Open a **second terminal** in the `crystal_courier` folder, leaving the game running in the first terminal:

```bash
check50 MrDiaz-cpu/class_work/main/crystal_courier
```

The 12 checks cover Python syntax, the `walk` and `main` functions, all four directions, the number of steps (including zero), collection after every step, repeated calls, and completing Challenge and Remix. Only `mission.py` is sent; the checker supplies its own game engine. Read the first red check, fix the code, save, and run check50 again. The unfinished starter is expected to fail behavior checks.

## Submit with submit50

From the same folder:

```bash
submit50 MrDiaz-cpu/class_work/main/crystal_courier
```

Sign in with **your own** CS50/GitHub account if prompted. Review the file list: it should contain **only `mission.py`**. Confirm the submission and keep the returned confirmation link. `check50` checks your work; `submit50` turns it in. Submit your current work before the deadline even if some checks still fail.

If you downloaded the game earlier, you do not need to download it again: both commands fetch the configuration from GitHub. Do not overwrite your completed `mission.py` with the starter.

### Troubleshooting

- **mission.py missing:** use `ls` and `pwd`; change into the folder containing your saved `mission.py`.
- **Login problem:** follow the tool's sign-in instructions using your own account. Tell your teacher if you cannot complete sign-in before the deadline.
- **Online check50 unavailable:** try `check50 --local MrDiaz-cpu/class_work/main/crystal_courier`. This still downloads the checks from GitHub but runs them in your codespace. It does not submit your work.
- **command not found:** use the cs50.dev terminal. On another Python environment, install with `python -m pip install check50 submit50`.

The game's quick completion checks are also available:

```bash
python play.py --check challenge
python play.py --check remix
```

Your teacher reviews the use of loops and your explanations separately from these behavior checks.

## Validation

Python game tests and browserless playback-controller checks passed. The 12 check50 checks accept three correct implementations and reject thirteen broken implementations. The submit50 file-selection configuration was verified to collect only mission.py; final submission requires the student’s own authenticated account. Full browser layout and the signed-in cs50.dev workflow still need a check on a school device. The preview is a render from the canvas code, not a full browser screenshot.

Original classroom extension; not an official CS50 problem set.
