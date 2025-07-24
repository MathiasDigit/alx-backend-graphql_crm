import graphene
from graphene_django.types import DjangoObjectType
from crm.models import Product  # Modèle des produits

# Type GraphQL pour le modèle Product
class ProductType(DjangoObjectType):
    class Meta:
        model = Product

# Mutation : met à jour les produits avec un stock < 10
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # Pas d'arguments nécessaires

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock_products:
            product.stock += 10  # Simule un réapprovisionnement
            product.save()
            updated.append(product)

        return UpdateLowStockProducts(
            updated_products=updated,
            message=f"{len(updated)} produit(s) réapprovisionné(s)."
        )

# On ajoute la mutation à la classe Mutation globale
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
