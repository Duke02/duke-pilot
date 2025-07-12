"""
Currently parses Word, Excel, Powerpoint, and their open document equivalents.
"""
import os
import tempfile
from pathlib import Path
import subprocess
import typing as tp

from duke_pilot.processors.doc_parser import pdf_parser
from duke_pilot.utils.path_helper import get_data_directory
from duke_pilot.utils.uuid import get_uuid

def _get_path(file_ext: str) -> Path:
    p: Path = get_data_directory() / 'parser'
    p.mkdir(exist_ok=True, parents=True)
    return p / f'{get_uuid()}.{file_ext}'


def _convert_to_pdf(f: tp.BinaryIO, file_ext: str) -> Path:
    out_path: Path = _get_path(file_ext)
    with out_path.open(mode='wb') as of:
        of.write(f.read())
    convert_dir: Path = get_data_directory() / 'converter'
    convert_dir.mkdir(exist_ok=True, parents=True)
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(convert_dir),
        str(out_path)
    ], check=True)
    pdf_path: Path = convert_dir / f'{out_path.stem}.pdf'

    # Remove the temporarily saved file.
    os.remove(out_path)

    if not pdf_path.exists():
        raise FileNotFoundError('Cannot find converted PDF.')

    return pdf_path


def from_file_io(f: tp.BinaryIO, file_ext: str) -> str:
    pdf_path: Path = _convert_to_pdf(f, file_ext)

    with pdf_path.open(mode='rb') as pf:
        out_text: str = pdf_parser.from_file_io(pf, file_ext=file_ext)
    # Remove the PDF now that we're done with it.
    os.remove(pdf_path)
    return out_text

