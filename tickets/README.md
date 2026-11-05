# Ticket Booth

## Your task

A school event uses alternating ticket colors to divide guests into two groups.
Odd-numbered tickets are GOLD. Even-numbered tickets are BLUE.

Complete `tickets.py`. Your program must:

1. Ask for a quantity with the exact prompt `Tickets: ` (including the space).
2. Accept an integer from **1 through 10**, including both endpoints.
3. Ask again with the same prompt whenever the integer is outside that range.
4. Print exactly that many tickets, numbered from 1 through the quantity.
5. Label odd-numbered tickets GOLD and even-numbered tickets BLUE.
6. Print each ticket on its own line, matching the examples below, then stop.

Assume the user enters integers. You do not need to handle words or decimals.
Do not print extra headings, error messages, totals, or debugging output.

Use a loop to repeat the input prompt and a loop to print the tickets. You may
use the class example as a reference. Complete `get_count` and `print_tickets`;
the `main` function is already provided. Replace each `pass` with your code.

## Get started

Download and extract [tickets_starter.zip](tickets_starter.zip), or use the
two Python files in [starter](starter/). The files run independently.

After your teacher has published this assignment, these commands also download
a new copy in cs50.dev. Run them only once so you do not overwrite your work:

```bash
wget https://raw.githubusercontent.com/MrDiaz-cpu/class_work/main/tickets/tickets_starter.zip
unzip tickets_starter.zip
cd tickets
code printer.py
code tickets.py
```

- `printer.py`: build this example with your teacher.
- `tickets.py`: finish this assignment and submit it by the end of class.

Run your assignment from the folder containing `tickets.py`:

```bash
python tickets.py
```

The starter has empty functions, so it produces no output until you implement them.

## Examples

Valid quantity:

```text
Tickets: 4
Ticket 1: GOLD
Ticket 2: BLUE
Ticket 3: GOLD
Ticket 4: BLUE
```

Invalid quantities followed by a valid quantity:

```text
Tickets: 0
Tickets: 11
Tickets: 3
Ticket 1: GOLD
Ticket 2: BLUE
Ticket 3: GOLD
```

The numbers after `Tickets: ` are typed by the user. Your program does not print
those input numbers itself.

## Checkpoints

1. **Quantity:** Accept a valid quantity and ask again for an invalid quantity.
2. **Numbering:** Print exactly the requested number of tickets, beginning with 1.
3. **Colors:** Alternate GOLD and BLUE, beginning with GOLD.

Before running the checker, try 1, 4, 5, and 10. Then try -2, 0, and 12 before
entering a valid quantity. Predict the result before each run. If a loop will
not stop, press Ctrl+C in the terminal.

## How to check

Once your teacher confirms that the assignment is live, run:

```bash
check50 MrDiaz-cpu/class_work/main/tickets
```

Read the first failed check. Compare its expected output with your actual output,
make one change, and run the checks again. The checks assess program behavior;
your teacher will also review your loops and your explanation.

## How to submit

Run this from the folder containing your completed `tickets.py`:

```bash
submit50 MrDiaz-cpu/class_work/main/tickets
```

Review the listed file before confirming. Only `tickets.py` should be included.
Submit your current work before the end of class, even if some checks still fail.
Check the submission link returned by submit50 to confirm that it was received.
Running check50 alone does not submit the assignment.

## Reflection

Be ready to explain:

- Why might the input loop repeat an unknown number of times?
- How does the printing loop know when to stop?
- Why is the conditional for a ticket's color inside the printing loop?

## Are You Ready for More?

Predict the number of GOLD tickets for any allowed quantity. Explain your rule.
If you write code for an extension, use a separate file so that `tickets.py`
continues to produce the required output.
