import json


class Event(dict):
    """
    Used to represents an message.
    """

    def __init__(self, **kwargs):
        super(Event, self).__init__()
        self.update(kwargs)

    def to_json(self) -> str:
        return json.dumps(self)
