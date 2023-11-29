import pytest
from scraper import QuittAPI, Product


@pytest.fixture
def api():
    return QuittAPI()


def test_search_product(api):
    products = api.search_product("Avengers")
    assert isinstance(products, list)
    assert len(products) > 0
    assert isinstance(products[0], Product)


def test_get_product_by_name(api):
    product = api.get_product_by_name("Avengers")
    assert product[1] == "application/json"


def test_update_product_price(api):
    response = api.update_product_price("Avengers", 15.99)
    assert response.status_code == 200


def test_delete_product(api):
    response = api.delete_product("Avengers")
    assert response.status_code == 200
