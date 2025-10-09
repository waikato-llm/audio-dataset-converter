from typing import Optional

from adc.api import AudioData
from kasperl.writer import MetaDataWriter as KMetaDataWriter


class MetaDataWriter(KMetaDataWriter):

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
