from ..base_parser import Base_Parser
from .token_sample import Token_Sample


class Token_Parser(Base_Parser):
    "Parses results of a text classification model"

    sample_class = Token_Sample

    def parse_json(self, in_json: dict) -> list[Token_Sample]:
        if in_json.get("error_message"):
            return []
        
        out = []
        monotonous_id_id = 0
        for file in in_json.get("files"):
            for sample in file.get("samples"):
                sample_obj = Token_Sample(
                    sample,
                    monotonous_id_id
                )
                out.append(sample_obj)
                monotonous_id_id += 1

        return out
    