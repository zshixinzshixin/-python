from pathlib import Path

path = Path('pi_digits.txt')
contents = path.read_text()

lines = contents.splitlines()
pi_string = ''
for line in lines:
    pi_string += line.strip()

print(pi_string)
print(len(pi_string))

path2 = Path('pi_million_digits.txt')
contents2 = path2.read_text()

pi_string2 = ''
for line in contents2.splitlines():
    pi_string2 += line.lstrip()

print(f"{pi_string[:52]}...")
print(len(pi_string2))