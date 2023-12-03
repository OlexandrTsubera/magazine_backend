import redis
from django.conf import settings
from .models import Product


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def submit_products_for(self, products, max_results=6):
        products_ids = [p.id for p in products]
        if len(products) == 1:
            # only one product
            suggestion = r.zrange(self.get_product_key(products_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # Generate a temporary key
            flat_ids = ''.join([str(id) for id in products_ids])
            tmp_key = f'tmp_{flat_ids}'
            # several products, combine the points of all products
            # save a sorted set in a temporary key
            keys = [self.get_product_key(id) for id in products_ids]
            r.zunionstore(tmp_key, keys)
            # remove identifiers of products for which a recommendation is given
            r.zrem(tmp_key, *products_ids)
            # get product IDs by their quantity sorted in descending order
            suggestion = r.zrange(tmp_key, 0, -1, desc=True,)[:max_results]
            # Delete temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestion]
        # get suggested products and sort them in the order they appear
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
