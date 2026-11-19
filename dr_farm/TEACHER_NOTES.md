# Teaching Dr. Farm

**Learning target.** Students can explain what one pass of a loop does, use a second loop to choose from a dictionary, and pass a timing value through two functions.

## Day 1 · One decision, then a field

| Minutes | Teacher move | Evidence to listen for |
|---:|---|---|
| 0–4 | Show a radish with zero pips. Ask students to sketch its first three mornings if watered daily. | Water counts when the day ends. A ripe plant still needs a harvest turn. |
| 4–12 | Live-code the two tutorial runs below. Pause before the third morning in each run. | Students distinguish being ready from being in the basket. |
| 12–16 | Display two plot dictionaries with different ready values. Have partners predict one action for each. | The argument identifies which plot to inspect. |
| 16–30 | Students finish Level 1 independently. Run Challenge and then Remix. | A new list length changes the number of visits without a code edit. |
| 30–40 | Partners trace one plot in the log, run check50, then submit their own file. | Have each partner explain a different line. |

### Tutorial live coding

1. Open `tutorial.py` beside the Private port preview. Ask, “If I water this for ten days, how many radishes will I collect?” Replace `pass` inside `tend` with a call to `water` on its argument. Save and run. Step through the first two nights. Point to the full pips and the “Already ripe!” bubble on day 3. Finish the run. The basket reads **0**.
2. Ask for the question the farmer should answer every morning. In `tend`, write an `if` that reads the argument’s `"ready"` key. Put the harvest call in that branch and move the water call under `else`. Trace day 3 before pressing **Next action**. Harvests occur on days **3, 6 and 9**. Each harvest replants a seed. The basket ends at **3**.
3. Open Level 1. Show the list of six crops and the blank functions. Students decide how to reuse the single-plot decision. Leave both functions for them to write.

## Day 2 · Seed choices and timing

Give students 12 minutes for Level 2. Display a bag with one corn seed and no radish. Ask two partners to act as the plot loop and the seed loop. When a seed is chosen, have the seed partner stop and the plot partner take the next step. Compare two orders. Ask why a higher price can cost more time.

For Level 3, draw boxes labeled 7, 8, 9, 10. Students place a plant, two waterings and one harvest in separate boxes. Slide the plant to day 8 and ask which action falls outside the season. Give 15 minutes to code and test both public fields. Finish with a check50 run from the second terminal.

| Symptom | Question to ask |
|---|---|
| Only the first plot changes | Which object goes into the function on the second pass? |
| “Already worked here today!” | Which line runs after your first successful action? Which loop should stop? |
| “No seeds!” while another crop has seeds | What value did you read before choosing this seed? |
| The last radish withers | Which day was reserved for harvesting? |
| All plots stay empty | Did you save the file selected in the level picker? Which function did the supplied loop call? |
| A print says ready but harvest fails | Did you ask the farm to change the plot or change the snapshot yourself? |

## Exit tickets

- Level 1. Trace one day for a field with a ripe corn plant and a growing carrot. How many times is `tend` called?
- Level 2. A bag holds zero radishes and one pumpkin. Explain when the seed loop should stop and what the plot loop does next.
- Level 3. Can you plant corn on day 6 and sell it by day 10? List the dates. What changes if you plant on day 5?

Look for two visits in the first answer, a stock check and an inner-loop exit in the second, and a separate harvest day in the third. Corn planted on day 6 misses the deadline. Day 5 leaves four watering days and a harvest on day 10.
