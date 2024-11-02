from DjangoAssr.websockets import TagConsumer
from CreateDatasetApp.models import DatasetTags


class DatasetConsumer(TagConsumer):
    tag_class = DatasetTags
