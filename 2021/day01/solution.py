from functools import reduce


def parse(lines):
    """Parse the input"""
    return [int(line) for line in lines]


def part1(numbers):
    """Part 1 solution implementation"""

    # Get num of increases from last num
    count = 0
    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i - 1]:
            count += 1

    return count


def part2(numbers):
    """Part 2 solution implementation"""

    # Get num of increases from last group of 3
    # E.g. indexes 0,1,2 are group A, indexes 1,2,3 are group B
    #   Compare sum of group A and B

    count = 0
    for i in range(3, len(numbers)):
        group1 = numbers[i - 3 : i]
        group2 = numbers[i - 2 : i + 1]

        sum1 = reduce(lambda a, b: a + b, group1)
        sum2 = reduce(lambda a, b: a + b, group2)

        if sum2 > sum1:
            count += 1

    return count


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
