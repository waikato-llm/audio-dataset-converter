from email.mime.multipart import MIMEMultipart

from kasperl.writer import SendEmail as KSendEmail

from adc.api import AudioData, FORMAT_MP3


class SendEmail(KSendEmail):

    def _attach_item(self, message: MIMEMultipart, item) -> bool:
        """
        Attaches the item to the message.

        :param message: the message to attach to
        :type message: MIMEMultipart
        :param item: the item to attach
        :return: whether data type has handled
        :rtype: bool
        """
        if isinstance(item, AudioData):
            if item.audio_format == FORMAT_MP3:
                subtype = "mpeg"
            else:
                subtype = item.audio_format.lower()
            self._attach_data(message, item.audio_bytes, item.audio_name,
                              mime_main="audio", mime_sub=subtype)
            return True
        else:
            return False
