"""FASTA sequence format parser for AlignX."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Union, TextIO
import io


@dataclass
class FastaRecord:
    """Represents a single FASTA record."""
    header: str
    id: str
    sequence: str

    def __len__(self) -> int:
        return len(self.sequence)

    def to_fasta_string(self, line_width: int = 80) -> str:
        """Format record as standard FASTA string."""
        lines = [f">{self.header}"]
        for i in range(0, len(self.sequence), line_width):
            lines.append(self.sequence[i:i + line_width])
        return "\n".join(lines)


def parse_fasta_string(content: str) -> List[FastaRecord]:
    """
    Parse a FASTA format string into a list of FastaRecord objects.
    
    Handles:
    - Multiple records
    - Multiline sequences
    - Whitespace trimming
    - Uppercasing sequence characters
    """
    records: List[FastaRecord] = []
    current_header = None
    current_seq_parts: List[str] = []

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            # Empty line or comment line
            continue

        if line.startswith(">"):
            if current_header is not None:
                seq = "".join(current_seq_parts).upper()
                rec_id = current_header.split()[0] if current_header else "unknown"
                records.append(FastaRecord(header=current_header, id=rec_id, sequence=seq))
                current_seq_parts = []
            current_header = line[1:].strip()
        else:
            current_seq_parts.append(line)

    if current_header is not None:
        seq = "".join(current_seq_parts).upper()
        rec_id = current_header.split()[0] if current_header else "unknown"
        records.append(FastaRecord(header=current_header, id=rec_id, sequence=seq))

    return records


def parse_fasta_file(filepath: Union[str, Path]) -> List[FastaRecord]:
    """Parse a FASTA file from a filesystem path."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"FASTA file not found: {filepath}")
    with open(path, "r", encoding="utf-8") as f:
        return parse_fasta_string(f.read())


def parse_fasta(source: Union[str, Path, TextIO]) -> List[FastaRecord]:
    """
    Flexible FASTA parser that accepts a file path, file-like object, or raw FASTA string.
    """
    if hasattr(source, "read"):
        return parse_fasta_string(source.read())
    
    if isinstance(source, Path) or (isinstance(source, str) and not source.startswith(">") and "\n" not in source):
        # Check if it looks like a path and exists
        try:
            path = Path(source)
            if path.is_file():
                return parse_fasta_file(path)
        except (OSError, ValueError):
            pass

    return parse_fasta_string(str(source))


def write_fasta(records: List[FastaRecord], filepath: Union[str, Path], line_width: int = 80) -> None:
    """Write a list of FastaRecord objects to a FASTA file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for i, rec in enumerate(records):
            if i > 0:
                f.write("\n")
            f.write(rec.to_fasta_string(line_width=line_width))
            f.write("\n")
