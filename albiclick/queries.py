
from products.models import Product
from django.db.models import Count, F, Subquery, Sum,OuterRef
from store.models import Cart,CartItem
from orders.models import Order






#this function returns a queryset of products with the number of sells
def get_products():
    queryset=Product.objects.annotate(
            num_sells=Subquery(CartItem.objects.filter(
                cart__in=Cart.objects.filter(id__in=list(Order.objects.all().values_list('cart', flat=True)))).filter(
                    product=OuterRef('id')).values("product_id").annotate(sum_of_sells=Sum('quantity')).values('sum_of_sells')))
    return queryset