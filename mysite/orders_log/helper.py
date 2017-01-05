from rest_framework.renderers import JSONRenderer
from django.utils import timezone


class Confirmation:
    def __init__(self, data):
        self.idorder = data.get('order', 0)
        self.iditem = data.get('item', 0)
        self.ship = data.get('shipping', 0)
        self.entity = ()

    def update_entry(self, idvalue):
        # 0 - received, 1 - shipped
        exst = entity.objects.get(pk=idvalue)
        if self.ship == 0:
            exst.received = datetime.now()
        else:
            exst.shipped = datetime.now()
        #exst.save()
        return exst


def get_json(objects, serializer, many=False):
    return JSONRenderer().render(serializer(objects, many=many).data)


def update_entry(entity, idvalue, tip):
        # 0 - received, 1 - shipped
        exst = entity.objects.get(pk=idvalue)
        if tip == 0:
            exst.received = timezone.now()
        else:
            exst.shipped = timezone.now()
        exst.save()
        return exst


