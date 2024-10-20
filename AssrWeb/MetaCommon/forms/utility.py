from django.db.models.manager import BaseManager
from MetaCommon.models import Tags


def _get_options(object_list: BaseManager[Tags]) -> list[tuple[int, str]]:
    return [(i, tag.name) for i, tag in enumerate(object_list)]