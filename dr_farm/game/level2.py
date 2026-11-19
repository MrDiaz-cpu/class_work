"""Dr. Farm · Level 2 · Plant"""
from farm import field, water, harvest, plant, seeds, grow_days, prices, sleep


def tend(plot):
    # Use the seed bag when you reach empty soil.
    pass


def work_day(field):
    # Visit the plots in the field you receive.
    pass


def main():  # supplied, don't change
    for day in range(10):
        work_day(field)
        sleep()


main()

