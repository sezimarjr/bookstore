import pytest

from product.models import Product


@pytest.mark.django_db
def test_product():
    product = Product.objects.create(
        title='Test Product', description='Test Description', price=100)
    assert product.title == 'Test Product'
    assert product.description == 'Test Description'
    assert product.price == 100
    assert product.id is not None
