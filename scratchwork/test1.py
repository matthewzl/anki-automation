import re


# def process_string(s):
#     # Replace individual backslashes, ensuring not to replace consecutive backslashes
#     s = re.sub(r'(?<!\\)\\(?!\\)', '', s)
#     # Replace multiple backslashes with half their number
#     s = re.sub(r'(\\\\)+', lambda m: '\\' * (len(m.group(0)) // 2), s)
#     return s


def process_string(s):
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    s = s.strip()
    s = re.sub(r'(?<!\\)\\(?!\\)', '', s)  # Replace individual backslashes
    s = re.sub(r'(\\\\)+', lambda m: '\\' * (len(m.group(0)) // 2), s)  # Reduce multiple backslashes by half
    return s


# Test string
test_string = "/Users/matthewliu/Desktop/AD1\\ (\\\\\\\\Attacks\\ and\\ Defenses)"
# test_string = input("Enter string: ")
processed_string = process_string(test_string)
print(processed_string)
