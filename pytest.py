import pytest
from QuittAPI import QuittAPI, Media


@pytest.fixture
def api():
    return QuittAPI()


def test_search_media(api):
    media = api.search_media("Avengers")
    assert isinstance(media, list)
    assert len(media) > 0
    assert isinstance(media[0], Media)


def test_get_media_by_name(api):
    media = api.get_media_by_name("Avengers")
    assert media[1] == "application/json"


def test_delete_media(api):
    response = api.delete_media("Avengers")
    assert response.status_code == 200
