class Order():
    def __init__(self,request):
        self.session = request.session

        order = self.session.get('order')

        if 'order' not in request.session:
            order = self.session["order"] = {} 

        self.order = order


    def add(self,product):
        product_id = str(product.id)
        
        if product_id in self.order:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True