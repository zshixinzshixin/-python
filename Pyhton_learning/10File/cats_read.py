from pathlib import Path

path = Path('cats.txt')
content = path.read_text()
content = content.replace('cat', 'dog')
print(content)