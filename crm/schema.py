import graphene
from graphene_django.types import DjangoObjectType
from crm.models import Customer, Product, Order
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from graphql import GraphQLError
from crm.utils import validate_phone_format  # You will define this helper
from graphene_django.filter import DjangoFilterConnectionField
from crm.filters import CustomerFilter, ProductFilter, OrderFilter
from crm.models import Customer, Product, Order
from graphene_django.types import DjangoObjectType

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        # Email validation
        try:
            validate_email(input.email)
        except ValidationError:
            raise GraphQLError("Invalid email format.")

        if Customer.objects.filter(email=input.email).exists():
            raise GraphQLError("Email already exists.")

        # Optional phone validation
        if input.phone and not validate_phone_format(input.phone):
            raise GraphQLError("Invalid phone format. Use +1234567890 or 123-456-7890.")

        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone
        )
        return CreateCustomer(customer=customer, message="Customer created successfully.")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CreateCustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created_customers = []
        errors = []

        with transaction.atomic():
            for index, entry in enumerate(input):
                try:
                    validate_email(entry.email)
                    if Customer.objects.filter(email=entry.email).exists():
                        raise ValueError(f"Customer at index {index}: Email already exists.")
                    if entry.phone and not validate_phone_format(entry.phone):
                        raise ValueError(f"Customer at index {index}: Invalid phone format.")

                    customer = Customer.objects.create(
                        name=entry.name,
                        email=entry.email,
                        phone=entry.phone
                    )
                    created_customers.append(customer)

                except Exception as e:
                    errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(default_value=0)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise GraphQLError("Price must be positive.")
        if input.stock < 0:
            raise GraphQLError("Stock cannot be negative.")

        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock
        )
        return CreateProduct(product=product)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        if not input.product_ids:
            raise GraphQLError("At least one product must be selected.")

        try:
            customer = Customer.objects.get(id=input.customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID.")

        products = []
        total = 0

        for pid in input.product_ids:
            try:
                product = Product.objects.get(id=pid)
                products.append(product)
                total += product.price
            except Product.DoesNotExist:
                raise GraphQLError(f"Invalid product ID: {pid}")

        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            order_date=input.order_date or timezone.now()
        )
        order.products.set(products)
        return CreateOrder(order=order)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)

    def resolve_customers(self, info):
        return Customer.objects.all()

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node, )
        fields = "__all__"

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node, )
        fields = "__all__"

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node, )
        fields = "__all__"

class Query(ObjectType):
    customer = relay.Node.Field(CustomerNode)
    all_customers = DjangoFilterConnectionField(CustomerNode, filterset_class=CustomerFilter, order_by=graphene.List(of_type=graphene.String))

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode, filterset_class=ProductFilter, order_by=graphene.List(of_type=graphene.String))

    order = relay.Node.Field(OrderNode)
    all_orders = DjangoFilterConnectionField(OrderNode, filterset_class=OrderFilter, order_by=graphene.List(of_type=graphene.String))
