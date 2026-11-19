"""Dr. Farm · Tutorial"""
from farm import plot, water, harvest, sleep


def tend(plot):
    # Try watering first. Then decide what to do when the radish is ready.
    pass


def main():  # supplied, don't change
    for day in range(10):
        tend(plot)
        sleep()


main()

