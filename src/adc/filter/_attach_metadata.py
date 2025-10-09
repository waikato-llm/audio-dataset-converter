from typing import Optional

from kasperl.filter import AttachMetaData as KAttachMetaData
from adc.api import AudioData


class AttachMetaData(KAttachMetaData):

    def _get_name(self, item) -> Optional[str]:
        """
        Returns the name of the item.

        :param item: the item to get the name for
        :return: the name or None if not available
        :rtype: str or None
        """
        if isinstance(item, AudioData):
            return item.audio_name
        return None
