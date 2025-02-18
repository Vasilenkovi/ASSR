from pathlib import Path
from unittest import TestCase
from ..models import File_reader


class Test_File_Reader(TestCase):

    BASE_DIR = Path(__file__).resolve().parent

    def test_pdf_reading(self):
        file = open(self.BASE_DIR / "pdf_1.pdf", "rb")
        file_bytes: bytes = file.read()
        reader = File_reader(file_bytes)
        file.close()

        # Limitations of PDF parsing and sentence tokenization
        sentences = ["This is a first sentence.", "And this is a nonsense C.A.T.", "acronym."]
        produced_sentences = list(reader.get_sample())

        for converter, desired_sentence in zip(produced_sentences, sentences):
            self.assertEqual(
                converter.input_str,
                desired_sentence
            )

    def test_csv_reading(self):
        file = open(self.BASE_DIR / "csv_1.csv", "rb")
        file_bytes: bytes = file.read()
        reader = File_reader(file_bytes, [1, 2])
        file.close()

        sentences = [
            "Actual sentence 1.",
            "Actual sentence 2.",
            "Actual sentence 3.",
            "Actual sentence 4."
        ]
        produced_sentences = list(reader.get_sample())

        for converter, desired_sentence in zip(produced_sentences, sentences):
            self.assertEqual(
                converter.input_str,
                desired_sentence
            )

    def test_garbage_file(self):
        with self.assertRaises(AttributeError):
            File_reader(b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00")
