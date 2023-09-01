from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('reserva/',views.reserva,name='reserva'),
    path('registrar/',views.registrar,name='registrar'),
    path('adicionar_prato/',views.adicionar_prato,name='adicionar_prato'),
    path('sair/',views.sair,name='sair'),
    path('ham/',views.ham,name='ham'),
    path('fritas/',views.fritas,name='fritas'),
    path('coca/',views.coca,name='coca'),
    # path('ir/',views.ir,name='ir'),
    path('retirar/<str:pratos>',views.retirar,name='retirar'),
    path('voltar/',views.voltar,name='voltar'),
    path('menu/',views.menu,name='menu'),
    path('retirar_prato/<str:prato>',views.retirar_prato,name='retirar_prato'),
    path('prato_pedido/<str:prato>',views.prato_pedido,name='prato_pedido'),
    path('deletar/',views.deletar,name='deletar')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)