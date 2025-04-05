from pathlib import Path
from unittest import TestCase
from Visual.results import Token_Parser


class Test_Token_Parser(TestCase):

    BASE_DIR = Path(__file__).resolve().parent

    def test_parser_init(self):
        "Tests parser's ability to construct and manage samples coherently"

        with open(self.BASE_DIR / "token_example.json", "r", encoding="UTF-8") as f:
            parser = Token_Parser(
                f.read()
            )

            self.assertEqual(
                len(parser.sample_list),
                697
            )

            valid_id = 0
            for sample in parser.sample_list:
                self.assertEqual(
                    sample.monotonous_id,
                    valid_id
                )
                valid_id += 1
