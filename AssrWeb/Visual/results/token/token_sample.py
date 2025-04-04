from enum import Enum
import numpy as np
from ..base_sample import Base_Sample


class Token_Sample(Base_Sample):
    "Works on samples from results, produced by a text classification model"

    class Similarity_Measure(Enum):
        JACCARD = 0

    @staticmethod
    def get_implemetned_methods() -> tuple:
        return (
            "get_similarity",
        )

    def get_similarity(
        self,
        rhs: "Token_Sample",
        measure: Similarity_Measure = Similarity_Measure.JACCARD
    ) -> float:

        match measure:
            case self.Similarity_Measure.JACCARD:
                return self._jaccard_similarity(rhs)
            
            case _:
                raise NotImplementedError(
                    f"{measure} is not a supported "
                    "Token_Sample.Similarity_Measure"
                )

    def get_values(self) -> list[float]:
        raise NotImplementedError(
            "Numerical sequences are not defined for token classification"
        )

    def get_tokens(self) -> list[str]:
        entries: list[dict] = self.sample_object.get("output")
        if not entries:
            return []
        
        out = []
        for e in entries:
            token = e.get("word")
            if not token:
                continue
            out.append(token)

        return out

    def _jaccard_similarity(self, rhs: "Token_Sample") -> float:
        lhs_tokens = set(self.get_tokens())
        rhs_tokens = set(rhs.get_tokens())

        return len(lhs_tokens & rhs_tokens) / len(lhs_tokens | rhs_tokens)
