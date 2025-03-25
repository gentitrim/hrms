class Order(object):
    def __init__(self, request):
        self.session = request.session
        order = self.session.get('order')
        if 'order' not in order:
            # save an empty order in the session
            order = self.session['order'] = {}
        self.order = order

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.order:
            self.order[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if override_quantity:
            self.order[product_id]['quantity'] = quantity
        else:
            self.order[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.order:
            del self.order[product_id]
        self.save()

    def get_sub_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item
                    in self.order.values())
    

    def clear(self):
        """
        Remove all items from the order.
        """
        for key in list(self.order.keys()):  # Use list() to create a copy of keys
            del self.order[key]
        self.save()