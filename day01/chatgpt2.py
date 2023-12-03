import re

def sum_calibration_values_final_corrected(lines):
    """
    Final corrected version to sum the calibration values for part two of the problem.
    This version considers the order of occurrence of the spelled-out digits in the string,
    not just the dictionary order.
    """
    digit_map = {
        "one": "1", "two": "2", "three": "3", "four": "4", 
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
    }

    def extract_digits(line):
        # Create a list to hold pairs of (index, digit)
        digit_positions = []

        # Find all occurrences of spelled-out digits and their start indices
        for word, digit in digit_map.items():
            for match in re.finditer(word, line):
                start_index = match.start()
                digit_positions.append((start_index, digit))

        # Add numeric digits and their indices
        digit_positions.extend((m.start(), m.group()) for m in re.finditer(r'\d', line))

        # Sort by index
        digit_positions.sort(key=lambda x: x[0])

        # Extract the first and last digits
        if digit_positions:
            first_digit = digit_positions[0][1]
            last_digit = digit_positions[-1][1]
            return first_digit, last_digit
        else:
            return "0", "0"

    # Calculate the sum of calibration values
    total = 0
    for line in lines:
        first_digit, last_digit = extract_digits(line)
        print(first_digit, last_digit)
        total += int(first_digit) * 10 + int(last_digit)
    
    return total

# Example data for testing
# example_lines_final_corrected_test = [
#     "two1nine",
#     "eightwothree",
#     "abcone2threexyz",
#     "xtwone3four",
#     "4nineeightseven2",
#     "zoneight234",
#     "7pqrstsixteen"
# ]

example_lines_final_corrected_test = [s.strip() for s in open("input-1.txt", "r").readlines()]

# Calculate the sum of calibration values for the example data
print(sum_calibration_values_final_corrected(example_lines_final_corrected_test))
