"""Dr. Farm · Level 3 · Timing"""
from farm import field, water, harvest, plant, seeds, grow_days, prices, sleep


def tend(plot, days_left):
    # Use the seed bag and the days left to pick one action.
    pass


def work_day(field, days_left):
    # Visit the plots in the field you receive.
    pass


def main():  # supplied, don't change
    for days_left in range(9, -1, -1):
        work_day(field, days_left)
        sleep()


main()

