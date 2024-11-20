from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import ProductSerializer


class TestProductSerializer(TestCase):
    def setUp(self) -> None:
        # Criando uma categoria usando a fábrica
        self.category = CategoryFactory(title="technology")

        # Criando um produto com a categoria associada
        self.product_1 = ProductFactory(
            title="mouse", price=100
        )
        self.product_1.categories.set([self.category])

        # Serializando o produto criado
        self.product_serializer = ProductSerializer(self.product_1)

    def test_product_serializer(self):
        # Pegando os dados do serializer
        serializer_data = self.product_serializer.data

        # Verificando se os dados serializados estão corretos
        self.assertEqual(serializer_data["price"], 100)
        self.assertEqual(serializer_data["title"], "mouse")

        # Corrigindo o nome do campo de 'category' para 'categories'
        self.assertEqual(
            serializer_data["categories"][0]["title"], "technology")
