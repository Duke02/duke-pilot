from pathlib import Path
from time import sleep

import nltk

from duke_pilot.utils.path_helper import get_base_directory

p: Path = get_base_directory() / '.venv' / 'share' / 'nltk_data'
p.mkdir(parents=True, exist_ok=True)
print(f'Putting NLTK data in {p}')

out_path: Path = p / 'tokenizers' / 'punkt_tab'
nltk.download('punkt_tab', download_dir=str(p))

assert out_path.exists(), 'Cannot find punkt_tab.'

