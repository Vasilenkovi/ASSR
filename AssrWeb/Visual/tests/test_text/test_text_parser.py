from pathlib import Path
from unittest import TestCase
from Visual.results import Text_Parser


class Test_Text_Parser(TestCase):

    BASE_DIR = Path(__file__).resolve().parent

    def test_parser_init(self):
        "Tests parser's ability to construct and manage samples coherently"

        with open(self.BASE_DIR / "text_example.json", "r", encoding="UTF-8") as f:
            parser = Text_Parser(
                f.read()
            )

            self.assertEqual(
                len(parser.sample_list),
                696
            )
            self.assertEqual(
                len(parser.sample_label_lookup),
                7
            )

            valid_id = 0
            lookup_list = parser.sample_label_lookup
            for sample in parser.sample_list:
                self.assertEqual(
                    sample.monotonous_id,
                    valid_id
                )
                valid_id += 1

                self.assertListEqual(
                    sample.label_lookup,
                    lookup_list
                )
