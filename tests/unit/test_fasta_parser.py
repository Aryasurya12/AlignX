import pytest
from pathlib import Path
import tempfile
from anchoralign.preprocessing.fasta_parser import (
    FastaRecord,
    parse_fasta,
    parse_fasta_string,
    parse_fasta_file,
    write_fasta,
)


def test_parse_single_record():
    content = ">seq1 Human hemoglobin fragment\nATGCGATCGATC\n"
    records = parse_fasta_string(content)
    assert len(records) == 1
    assert records[0].id == "seq1"
    assert records[0].header == "seq1 Human hemoglobin fragment"
    assert records[0].sequence == "ATGCGATCGATC"
    assert len(records[0]) == 12


def test_parse_multiple_records():
    content = (
        ">geneA first gene\n"
        "ACGT\n"
        "TGCA\n"
        ">geneB second gene\n"
        "GGCCAA\n"
    )
    records = parse_fasta_string(content)
    assert len(records) == 2
    assert records[0].id == "geneA"
    assert records[0].sequence == "ACGTTGCA"
    assert records[1].id == "geneB"
    assert records[1].sequence == "GGCCAA"


def test_parse_comments_and_blank_lines():
    content = (
        "; comment line\n"
        "\n"
        ">sample_1\n"
        "atgc\n"
        "\n"
        "tact\n"
    )
    records = parse_fasta_string(content)
    assert len(records) == 1
    assert records[0].sequence == "ATGCTACT"


def test_round_trip_write_and_read():
    recs = [
        FastaRecord(header="test1 sample sequence 1", id="test1", sequence="A" * 100 + "C" * 50),
        FastaRecord(header="test2 sample sequence 2", id="test2", sequence="G" * 30 + "T" * 70),
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "output.fasta"
        write_fasta(recs, tmp_path, line_width=60)
        assert tmp_path.exists()

        loaded = parse_fasta_file(tmp_path)
        assert len(loaded) == 2
        assert loaded[0].id == "test1"
        assert loaded[0].sequence == recs[0].sequence
        assert loaded[1].id == "test2"
        assert loaded[1].sequence == recs[1].sequence


def test_parse_fasta_polymorphism():
    content = ">seq1 test\nACGT\n"
    # From string
    r1 = parse_fasta(content)
    assert len(r1) == 1
    assert r1[0].sequence == "ACGT"

    # From file path
    with tempfile.NamedTemporaryFile("w", suffix=".fa", delete=False) as f:
        f.write(content)
        f_name = f.name
    try:
        r2 = parse_fasta(f_name)
        assert len(r2) == 1
        assert r2[0].sequence == "ACGT"
    finally:
        Path(f_name).unlink(missing_ok=True)


def test_parse_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        parse_fasta_file("/non/existent/path/dna.fasta")


def test_parse_sample_files():
    repo_root = Path(__file__).resolve().parents[2]
    samples_dir = repo_root / "data" / "samples"
    if samples_dir.exists():
        hbb_file = samples_dir / "human_hbb.fasta"
        if hbb_file.exists():
            records = parse_fasta_file(hbb_file)
            assert len(records) >= 1
            assert len(records[0].sequence) == 444
