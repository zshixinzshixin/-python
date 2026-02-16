from pathlib import Path
import json

numbers = [2, 3, 5, 7, 11, 13]

path = Path('number.json')
contentes = json.dumps(numbers)
path.write_text(contentes)