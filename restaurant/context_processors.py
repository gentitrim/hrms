from .order import Order


def order(request):
    return {'order':Order(request)}