"""Dr. Farm · Level 1 · Harvest"""
from farm import field, water, harvest, sleep


def tend(plot):
    # Choose one action for this crop.
    pass


def work_day(field):
    # Visit the plots in the field you receive.
    pass


def main():  # supplied, don't change
    for day in range(10):
        work_day(field)
        sleep()


main()

