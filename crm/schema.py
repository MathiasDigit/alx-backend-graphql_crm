import graphene
from graphene_django.types import DjangoObjectType
from crm.models import Product  

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock") 


class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    message = graphene.String()

    class Arguments:
        pass  

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock_products:
            product.stock += 10  
            product.save()
            updated.append(product)

        return UpdateLowStockProducts(
            updated_products=updated,
            message=f"{len(updated)} produit(s) réapprovisionné(s)."
        )


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info):
        return Product.objects.all()

# Déclaration du schéma GraphQL
schema = graphene.Schema(query=Query, mutation=Mutation)
