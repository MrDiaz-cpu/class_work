# Game Score Recap: finish show_results, then submit this file.


def main():
    scores = [8, 15, 4, 12]
    show_results(scores)


def show_results(scores):
    wins = 0
    round_number = 1

    # TODO: Use a for loop to visit every score in scores.
    # A score of 10 or more is a WIN. Every other score is a LOSS.
    # Print each round using the format shown in the instructions.
    # Count each win, and advance the round number after every round.

    print(f"Wins: {wins}")


# Leave these two lines in place. They start main when you run this file.
if __name__ == "__main__":
    main()
