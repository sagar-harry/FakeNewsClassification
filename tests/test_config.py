import pytest


class NotANews(Exception):
    def __init__(self, message="Not a news"):
        self.message = message
        super().__init__(self.message)


def test_generic():
    a = "123"
    with pytest.raises(NotANews):
        if (a.isnumeric()):
            raise NotANews