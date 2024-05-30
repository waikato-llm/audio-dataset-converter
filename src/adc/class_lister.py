from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "adc.reader",
            "adc.reader.speech",
        ],
        "seppl.io.Filter": [
            "adc.filter",
            "adc.filter.speech",
        ],
        "seppl.io.Writer": [
            "adc.writer",
            "adc.writer.speech",
        ],
        "adc.api.Generator": [
            "adc.generator",
        ],
    }
