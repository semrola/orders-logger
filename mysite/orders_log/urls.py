from django.conf.urls import url, include
from . import views
from rest_framework import routers
from orders_log import views
from django.views.generic import TemplateView


router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'stores', views.StoreViewSet)
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name="front/index.html"), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.loginview, name='login'),
    url(r'^logout$', views.logout_view, name='login'),
    #url(r'^loginpost$', views.loginpost, name='loginpost'),
    #url(r'^(?P<order_id>[0-9]+)/$', views.view_order, name='order'),
    #url(r'^latest/$', views.latest_orders, name='latest'),
    #url(r'^not_received/$', views.not_received, name='not_received'),
    #url(r'^items/(?P<item_id>[0-9]+)/$', views.view_item, name='item'),
    url(r'^api/', include(router.urls))
]
