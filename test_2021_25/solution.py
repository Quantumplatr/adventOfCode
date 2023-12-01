from functools import reduce


def parse(lines):
    """Parse the input"""

    # Build 2D array of structure
    # Map .,>,v to 0,1,2 respectively

    return [
        [0 if char == "." else 1 if char == ">" else 2 for char in line]
        for line in lines
    ]


def part1(data, should_print = False):
    """Part 1 solution implementation"""
    
    if should_print:
        print("Initial state:")
        print_data(data)
        print()

    moves = -1
    steps = 0
    while moves != 0:# and steps < 4:
        moves = 0

        # Check east movements
        for i in range(len(data)):
            j = 0
            new_row = [0]*len(data[i])
            while j < len(data[i]):
                
                # Check if something to the right
                if data[i][j] == 1 and data[i][(j + 1) % len(data[i])] == 0:
                    moves += 1
                    new_row[j] = 0
                    new_row[(j + 1) % len(data[i])] = data[i][j]
                    j += 1
                else:
                    new_row[j] = data[i][j]
                    
                j += 1
            data[i] = new_row

        # Check south movements
        j = 0
        while j < len(data[0]):
            i = 0
            new_col = [0]*len(data)
            while i < len(data):
                
                # Check if something below
                if data[i][j] == 2 and data[(i + 1) % len(data)][j] == 0:
                    moves += 1
                    new_col[i] = 0
                    new_col[(i + 1) % len(data)] = data[i][j]
                    i += 1
                else:
                    new_col[i] = data[i][j]
            
                i += 1
                
            i = 0
            while i < len(data):
                data[i][j] = new_col[i]
                i += 1
            j += 1
                    
        steps += 1
        
        if should_print:
            print("After", steps, f"step{'s' if steps != 1 else ''}:")
            print_data(data)
            print()

    return steps


def part2(data):
    """Part 2 solution implementation"""
    return "Incomplete"


def print_data(data):
    """Pretty print"""

    for row in data:
        print("".join(["." if d == 0 else ">" if d == 1 else "v" for d in row]))


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
