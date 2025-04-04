from enum import Enum
import numpy as np
from ..base_sample import Base_Sample


class Text_Sample(Base_Sample):
    "Works on samples from results, produced by a text classification model"

    class Similarity_Measure(Enum):
        COSINE = 0
        EUCLID = 1
    
    label_lookup: list[str] | None

    @staticmethod
    def get_implemetned_methods() -> tuple:
        return (
            "get_similarity",
            "get_values"
        )

    def get_similarity(
        self,
        rhs: "Base_Sample",
        measure: Similarity_Measure = Similarity_Measure.COSINE
    ) -> float:
        self._check_initialized()

        match measure:
            case self.Similarity_Measure.COSINE:
                return self._cosine_similarity(rhs)
            
            case self.Similarity_Measure.EUCLID:
                return self._euclid_similarity(rhs)
            
            case _:
                raise NotImplementedError(
                    f"{measure} is not a supported "
                    "Text_Sample.Similarity_Measure"
                )

    def get_values(self) -> list[float]:
        self._check_initialized()
        
        entries: list[dict] = self.sample_object.get("output")
        if not entries:
            return []
        
        combined_dict = {}
        for e in entries:
            k = e.get("label")
            v = e.get("score")
            combined_dict[k] = v

        out = []
        for l in self.label_lookup:
            current_value = combined_dict.get(l)
            if current_value:
                out.append(current_value)
            else:
                out.append(0)

        return out

    def get_labels(self) -> list[str]:
        entries: list[dict] = self.sample_object.get("output")
        if not entries:
            return []
        
        out = []
        for e in entries:
            label = e.get("label")
            if not label:
                continue
            out.append(label)

        return out

    def _check_initialized(self) -> None:
        if not self.label_lookup:
            raise AttributeError(
                "label_lookup field must be set to ensure same order"
                " of values across multiple samples"
            )

    def _cosine_similarity(self, rhs: "Base_Sample") -> float:
        lhs_vector = self.get_values()
        rhs_vector = rhs.get_values()

        lhs_length = np.linalg.norm(lhs_vector)
        rhs_length = np.linalg.norm(rhs_vector)

        return 1 - np.dot(lhs_vector, rhs_vector) / (lhs_length * rhs_length)

    def _euclid_similarity(self, rhs: "Base_Sample") -> float:
        lhs_vector = self.get_values()
        rhs_vector = rhs.get_values()

        distance = np.subtract(lhs_vector, rhs_vector)

        return np.linalg.norm(distance)
