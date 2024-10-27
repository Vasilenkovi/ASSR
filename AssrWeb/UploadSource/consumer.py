from DjangoAssr.websockets import TagConsumer
from UploadSource.models.source_file_tag import SourceTags


class UploadConsumer(TagConsumer):
    tag_class = SourceTags
