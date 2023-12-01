from functools import reduce


def parse(lines):
    """Parse the input"""

    return lines


def part1(data):
    """Part 1 solution implementation"""

    sum = 0

    for line in data:
        num = 0

        # Get first digit
        for char in line:
            if char.isnumeric():
                num += int(char) * 10
                break

        # Get last digit
        for i in range(len(line) - 1, -1, -1):
            if line[i].isnumeric():
                num += int(line[i])
                break

        sum += num

    return sum


def part2(data):
    """Part 2 solution implementation"""

    nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    sum = 0

    for l in data:
        digits = []

        for i in range(len(l)):
            line = l[i:]

            if line[0].isnumeric():
                digits.append(int(line[0]))

            for num in nums:
                if line.startswith(num):
                    index = nums.index(num)
                    digits.append(index + 1)
                    line = line[len(num) :]
                    break

        sum += digits[0] * 10 + digits[-1]

    return sum


def main():
    # Read file into lines
    f = open("input.txt", "r")
    input_lines = f.readlines()
    f.close()

    # Strip the newline character
    input_lines = [line.strip() for line in input_lines]

    # Parse the input
    data = parse(input_lines)

    # Print the solutions
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == "__main__":
    main()
