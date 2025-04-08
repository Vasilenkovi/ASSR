from pathlib import Path
from unittest import TestCase
from Visual.results import Token_Parser, Token_Sample


class Test_Token_Sample(TestCase):

    BASE_DIR = Path(__file__).resolve().parent
    
    def test_sample_standalone(self):
        sample_1 = Token_Sample(
            {
                "sentence": 0,
                "input": "example 1",
                "output": [
                    {
                      "entity": "B-MISC",
                      "score": 0.5914095640182495,
                      "index": 1,
                      "word": "1",
                      "start": 0,
                      "end": 1
                    },
                    {
                      "entity": "B-MISC",
                      "score": 0.9812078475952148,
                      "index": 2,
                      "word": "Le",
                      "start": 3,
                      "end": 5
                    }
                ]
            },
            0
        )
        sample_2 = Token_Sample(
            {
                "sentence": 1,
                "input": "example 2",
                "output": [
                    {
                        "entity": "I-ORG",
                        "score": 0.45951151847839355,
                        "index": 8,
                        "word": "H",
                        "start": 9,
                        "end": 10
                    },
                    {
                        "entity": "I-ORG",
                        "score": 0.4702574610710144,
                        "index": 9,
                        "word": "AAA",
                        "start": 10,
                        "end": 11
                    }
                ]
            },
            1
        )

        self.assertCountEqual(
            sample_1.get_tokens(),
            ("1", "Le")
        )
        self.assertCountEqual(
            sample_2.get_tokens(),
            ("H", "AAA")
        )
        self.assertAlmostEqual(
            sample_1.get_similarity(sample_2),
            0.0
        )
        with self.assertRaises(NotImplementedError):
            sample_1.get_values()
        with self.assertRaises(NotImplementedError):
            sample_2.get_values()

    def test_sample_from_parser(self):
        with open(self.BASE_DIR / "token_example.json", "r", encoding="UTF-8") as f:
            parser = Token_Parser(
                f.read()
            )

            # Two orthogonal samples
            sample_1: Token_Sample = parser.sample_list[37]
            sample_2: Token_Sample = parser.sample_list[94]

            self.assertCountEqual(
                sample_1.get_tokens(),
                ("об", "##ъ", "##еди", "##нен", "##ный", "список")
            )
            self.assertCountEqual(
                sample_2.get_tokens(),
                ("список",)
            )
            self.assertAlmostEqual(
                sample_1.get_similarity(sample_2),
                0.16666,
                places=4
            )
            with self.assertRaises(NotImplementedError):
                sample_1.get_values()
            with self.assertRaises(NotImplementedError):
                sample_2.get_values()
