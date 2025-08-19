from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "kasperl.reader",
            "adc.reader",
            "adc.reader.classification",
            "adc.reader.speech",
        ],
        "seppl.io.Filter": [
            "kasperl.filter",
            "adc.filter",
            "adc.filter.classification",
            "adc.filter.speech",
        ],
        "seppl.io.Writer": [
            "kasperl.writer",
            "adc.writer",
            "adc.writer.classification",
            "adc.writer.speech",
        ],
        "kasperl.api.Generator": [
            "kasperl.generator",
        ],
    }
