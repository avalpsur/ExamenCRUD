from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('promociones/listar',views.listar_promociones,name='lista_promociones'),
    path('promociones/crear',views.promocion_create,name='promocion_create'),
    path('promociones/editar/<int_promocion_id>',views.promocion_editar,name='promocion_editar'),
    path('promociones/eliminar/<int:promocion_id>',views.promocion_eliminar,name='promocion_eliminar'),
]