# Game Score Recap

**Due: submit `recap.py` before the end of class.**

**Learning target:** I can use a loop to process a list and keep a count that changes as the loop runs.

You played several rounds of a game. Your program will print a recap and count your wins. A score of **10 or more** is a **WIN**. A score below 10 is a **LOSS**.

## 1. Get the two starter files

In your cs50.dev terminal, run these commands once. If you already have a folder named `recap`, use a different folder name so you keep your earlier work.

```bash
mkdir recap
cd recap
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/recap/starter/scores_demo.py
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/recap/starter/recap.py
code scores_demo.py
```

- `scores_demo.py`: build this with your teacher. It adds the scores to find the total points.
- `recap.py`: finish this yourself. It prints the rounds and counts the wins. This is the only file you submit.

## 2. Predict before coding

For the scores `[8, 15, 4, 12]`:

1. Which rounds are wins?
2. What should the win counter contain after each round?
3. Why does the counter need to remember its previous value?

## 3. Finish `recap.py`

Open the assignment:

```bash
code recap.py
```

The provided `main()` calls `show_results(scores)`. Complete **the body of `show_results`**.

Your function must:

1. Use a `for` loop to visit every score in the supplied list, in order.
2. Number the rounds beginning with 1. Increase the round number after every round.
3. Label a score of 10 or more `WIN`; label every other score `LOSS`.
4. Print one line for each round in this exact format: `Round 1: 8 points - LOSS`.
5. Count each winning round once, including repeated winning scores.
6. After the loop, print `Wins: ` followed by the total number of wins.

Each call starts a new recap: start counting wins from 0 and rounds from 1 every time. Use the list passed into the function. It may contain a different number of rounds and different scores. You may assume it contains at least one score and that every score is a nonnegative integer. You do not need `input()`, exception handling, or an empty-list case.

Keep the function name and parameter, the sample in `main()`, and the last two supplied lines. You can temporarily change the sample to test your work; restore `[8, 15, 4, 12]` before submitting. The last two lines let you run the program normally while also letting check50 try your function with other lists.

## 4. Run and compare

```bash
python recap.py
```

The sample output must be:

```text
Round 1: 8 points - LOSS
Round 2: 15 points - WIN
Round 3: 4 points - LOSS
Round 4: 12 points - WIN
Wins: 2
```

Use uppercase `WIN` and `LOSS`. Use the word `points` for every score, including 1. Match the spaces and punctuation, and print no extra headings, debugging messages, or blank lines.

Try these additional lists. Check every round's label and number, as well as the final total.

| Scores | Final line | What it checks |
| --- | --- | --- |
| `[10]` | `Wins: 1` | Exactly 10 is a win. |
| `[0, 9]` | `Wins: 0` | A recap can have no wins. |
| `[10, 11, 20]` | `Wins: 3` | More than one win must be counted. |
| `[12, 12, 4]` | `Wins: 2` | Repeated scores are separate rounds. |

Stuck? Trace these columns on paper: **round number / score / win or loss / wins so far**. Decide which variables are set once before the loop, which change every round, and which change only after a win.

## 5. Check and submit before the bell

In the folder containing your completed `recap.py`, run:

```bash
check50 MrDiaz-cpu/class_work/main/recap
```

Read the first red check, revise your code, and run check50 again. Then submit:

```bash
submit50 MrDiaz-cpu/class_work/main/recap
```

Confirm that the listed file is `recap.py`. Follow the sign-in and confirmation prompts. Wait for the submission to finish and keep the confirmation link. A successful check50 run alone is not a submission. If you still have red checks at the bell, submit your current attempt and identify one issue you still need to fix.

## Cool-down

A student places `wins = 0` as the first line **inside** the loop. Explain what goes wrong for `[12, 15, 4]`. Where should that line go?

## Finished early?

In a separate file named `recap_extension.py`, count losses too. Explain why `wins + losses` should equal the number of rounds. Submit the original required output in `recap.py`.
