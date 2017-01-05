from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.http import HttpResponse
from .models import Order, Item, Comment, Store
from rest_framework import viewsets, authentication, permissions
from .serializers import OrderSerializer, CommentSerializer, StoreSerializer, ItemSerializer
from django.contrib.auth import authenticate, login, logout
import logging as log
from django import forms
from rest_framework.decorators import detail_route, list_route
from .helper import *
from rest_framework.request import Request
from django.utils import timezone


FORMAT = '%(asctime)-15s %(message)s'
log.basicConfig(filename='logger1.log', level=log.DEBUG, format=FORMAT)


def index(request):
    if request.user.is_authenticated():
        return render(request, 'front/index.html', None)
    else:
        return loginview(request)


def loginview(request):
    if request.user.is_authenticated():
        return render(request, 'front/index.html', None)

    error_message = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return index(request)
                else:
                    return "<h1>DISABLED</h1>"
            else:
                error_message = "Invalid login"
    else:
        # GET method -> empty form
        form = LoginForm()

    return render(request, 'front/login.html', {'form': form, 'error': error_message})


def logout_view(request):
    logout(request)
    return loginview(request)


def not_received(request):
    orders = Order.objects.all().filter(received=None)
    ctx = RequestContext(request, {'orders_list': orders})
    return render(request, 'orders/index.html', ctx)


def latest_orders(request):
    latest_orders_list = Order.objects.order_by('-ordered')[:10]
    context = RequestContext(request, {'orders_list': latest_orders_list})
    return render(request, 'orders/index.html', context)


def view_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order.html', {'order': order})


def view_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'orders/item.html', {'item': item})


# *********************************************************************

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class DefaultsMixin(object):
    """Default settings for view authentication, permissions,
    filtering and pagination."""
    authentication_classes = (

        #authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-ordered')
    serializer_class = OrderSerializer

    @list_route(methods=['post'])
    def confirm_order(self, request):
        # import pdb; pdb.set_trace()
        # TODO: dodaj se kontrolo za userja (avtentikacija + ali order/item res pripada userju)
        data = request.data
        idorder = data.get('order', 0)
        iditem = data.get('item', 0)
        ship = data.get('shipping', 0)
        serializer = OrderSerializer if idorder != 0 else ItemSerializer
        entity = Order if idorder else Item
        idvalue = idorder if idorder else iditem

        if idorder:
            # - to je ce kliknemo na shipped ali received na Order, se vnese tudi shipped ali received
            # vseh pripadajocih itemov TODO: klient ne ve, dokler ne refresha strani - treba je obvestit
            # controllerje na strani klienta
            # - preglej pripadajoce item-e, ce imajo shipping oz. received vnesen
            for item in Order.objects.get(id=idorder).item_set.all():
                if (ship and not item.shipped) or (not ship and not item.received):
                    update_entry(Item, item.id, ship)

        return HttpResponse(get_json(update_entry(entity, idvalue, tip=ship), serializer))

    @list_route(methods=['post'])
    def new_order(self, request):
        data = request.data
        print(data)
        order = data.get('order', None)
        if order:
            storeid = order.get('store', None)
            if not storeid:
                return HttpResponse('no store selected')
            items = order.get('items', None)
            shfrom = order.get('shfrom', None)
            shto = order.get('shto', None)
            price = order.get('price', None)
            daysfrom = order.get('daysfrom', None)
            daysto = order.get('daysto', None)

            store = Store(id=storeid)
            o = Order(price=price, ordered=timezone.now(), shippingDateTo=shto, shippingDateFrom=shfrom,
                      shippingDaysFrom=daysfrom, shippingDaysTo=daysto, store=store)
            o.save()

            for item in items:
                i = Item(name=item.get('name', 'NoNameItem'), url=item.get('url', None), price=item.get('price', None),
                         shippingDateTo=item.get('shto', None), shippingDateFrom=item.get('shfrom', None),
                         shippingDaysFrom=item.get('daysfrom', None), shippingDaysTo=item.get('daysto', None), order=o)
                i.save()

        return HttpResponse('success')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    #import pdb; pdb.set_trace()

    @list_route(methods=['get'])
    def get_order(self, request):
        id = request.GET.get('order', False)
        queryset = Item.objects.filter(order_id=id)
        serializer = ItemSerializer(queryset, many=True)
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @list_route(methods=['post'])
    def new_store(self, request):
        data = request.data
        store_name = data.get('name', None)
        store_page = data.get('homepage', None)
        store_desc = data.get('description', '')

        print(data)
        if store_name and store_page:
            s = Store(name=store_name, homepage=store_page, description=store_desc)
            s.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')

    @list_route(methods=['post'])
    def edit_store(self, request):
        data = request.data
        storeid = data.get('id', None)
        if storeid:
            s = Store.objects.get(id=storeid)
            s.homepage = data.get('homepage', s.homepage)
            s.name = data.get('name', s.name)
            s.description = data.get('description', s.description)
            s.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')

    @list_route(methods=['post'])
    def remove_store(self, request):
        storeid = request.data.get('id', None)
        if storeid:
            s = Store(id=storeid)
            s.delete()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')
