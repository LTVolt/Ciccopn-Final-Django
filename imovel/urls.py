from django.urls import path

from . import views

app_name = 'imovel'

urlpatterns = [
    path('', views.home, name='home'),
    path('imoveis/', views.lista_imoveis, name='lista_imoveis'),
    path('imoveis/<int:id_imovel>/', views.detalhe_imovel, name='detalhe_imovel'),
    path('conta/registo/', views.registo, name='registo'),
    path('conta/login/', views.login_utilizador, name='login'),
    path('conta/perfil/', views.perfil, name='perfil'),
    path('conta/anunciante/', views.painel_anunciante, name='painel_anunciante'),
    path('conta/anunciante/anuncios/novo/', views.criar_anuncio, name='criar_anuncio'),
    path('conta/anunciante/anuncios/<int:id_imovel>/editar/', views.editar_anuncio, name='editar_anuncio'),
    path('conta/anunciante/anuncios/<int:id_imovel>/apagar/', views.apagar_anuncio, name='apagar_anuncio'),
    path('conta/logout/', views.logout_utilizador, name='logout'),
]
