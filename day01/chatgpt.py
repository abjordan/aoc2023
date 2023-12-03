import re

def sum_calibration_values_part_two(lines):
    """
    Sums the calibration values for part two of the problem, where the first and last digits
    on each line can be actual digits or spelled out numbers.
    """
    digit_map = {
        "one": "1", "two": "2", "three": "3", "four": "4", 
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
    }

    def extract_digits(line):
        # Replace spelled out digits with their numeric counterparts
        for word, digit in digit_map.items():
            line = line.replace(word, digit)
        # Extract all digits from the line
        digits = re.findall(r'\d', line)
        return digits[0], digits[-1] if digits else (0, 0)

    # Calculate the sum of calibration values
    total = 0
    for line in lines:
        first_digit, last_digit = extract_digits(line)
        print(first_digit, last_digit)
        total += int(first_digit) * 10 + int(last_digit)
    
    return total

# Test the function with the example data
example_lines_part_two = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen"
]

# Calculate the sum of calibration values for the example data
print(sum_calibration_values_part_two(example_lines_part_two))