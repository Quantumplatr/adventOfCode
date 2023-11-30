from functools import reduce

def parse(lines):
    """Parse the input"""
    return "Incomplete"


def part1(numbers):
    """Part 1 solution implementation"""
    return "Incomplete"


def part2(numbers):
    """Part 2 solution implementation"""
    return "Incomplete"

def main():
    # Read file into lines
    f = open("input.txt", "r")
    input_lines = f.readlines()
    f.close()

    # Strip the newline character
    input_lines = [line.strip() for line in input_lines]

    # Parse the input
    numbers = parse(input_lines)

    # Print the solutions
    print("Part 1:", part1(numbers))
    print("Part 2:", part2(numbers))

if __name__ == "__main__":
    main()
