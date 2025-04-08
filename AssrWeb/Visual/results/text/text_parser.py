from ..base_parser import Base_Parser
from .text_sample import Text_Sample


class Text_Parser(Base_Parser):
    "Parses results of a text classification model"

    sample_class = Text_Sample
    sample_label_lookup: list[str]

    def parse_json(self, in_json: dict) -> list[Text_Sample]:
        if in_json.get("error_message"):
            return []
        
        out = []
        monotonous_id_id = 0
        label_lookup = set()
        for file in in_json.get("files"):
            for sample in file.get("samples"):
                sample_obj = Text_Sample(
                    sample,
                    monotonous_id_id
                )
                out.append(sample_obj)
                monotonous_id_id += 1

                label_lookup.update(
                    sample_obj.get_labels()
                )

        label_lookup = list(label_lookup)
        self.sample_label_lookup = label_lookup

        # Make further sample logic independent from parser
        for sample in out:
            sample.label_lookup = label_lookup

        return out
    