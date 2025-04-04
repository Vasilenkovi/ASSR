from pathlib import Path
from unittest import TestCase
from Visual.results import Text_Parser, Text_Sample


class Test_Text_Sample(TestCase):

    BASE_DIR = Path(__file__).resolve().parent
    
    def test_sample_standalone(self):
        sample_1 = Text_Sample(
            {
                "sentence": 0,
                "input": "example 1",
                "output": [
                    {
                        "label": "label 1",
                        "score": 0.1
                    }
                ]
            },
            0
        )
        sample_2 = Text_Sample(
            {
                "sentence": 1,
                "input": "example 2",
                "output": [
                    {
                        "label": "label 2",
                        "score": 0.1
                    }
                ]
            },
            1
        )
        with self.assertRaises(AttributeError):
            sample_1.get_similarity(sample_1, sample_2)

    def test_sample_from_parser(self):
        with open(self.BASE_DIR / "text_example.json", "r", encoding="UTF-8") as f:
            parser = Text_Parser(
                f.read()
            )

            # Two orthogonal samples
            sample_1: Text_Sample = parser.sample_list[0]
            sample_2: Text_Sample = parser.sample_list[14]

            self.assertTrue(
                sample_1.get_values()
            )
            self.assertTrue(
                sample_2.get_values()
            )
            self.assertAlmostEqual(
                sample_1.get_similarity(
                    sample_2,
                    Text_Sample.Similarity_Measure.COSINE
                ).item(),
                1.0
            )
            self.assertAlmostEqual(
                sample_1.get_similarity(
                    sample_2,
                    Text_Sample.Similarity_Measure.EUCLID
                ).item(),
                0.77438,
                places=4
            )
            with self.assertRaises(NotImplementedError):
                sample_1.get_similarity(
                    sample_2,
                    99
                )
