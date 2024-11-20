import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100,
        )
        self.product.categories.set([self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)

        # Valida que a resposta é uma lista
        self.assertIsInstance(order_data, list)
        self.assertGreater(len(order_data), 0)

        # Pega o primeiro pedido
        first_order = order_data[0]
        self.assertIn("product", first_order)
        self.assertIsInstance(first_order["product"], list)
        self.assertGreater(len(first_order["product"]), 0)

        # Valida o primeiro produto do pedido
        first_product = first_order["product"][0]
        self.assertEqual(first_product["title"], self.product.title)
        self.assertEqual(first_product["price"], self.product.price)
        self.assertEqual(first_product["active"], self.product.active)

        # Valida a categoria do primeiro produto
        self.assertIn("categories", first_product)
        self.assertIsInstance(first_product["categories"], list)
        self.assertGreater(len(first_product["categories"]), 0)
        self.assertEqual(first_product["categories"]
                         [0]["title"], self.category.title)

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
