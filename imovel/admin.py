from django.contrib import admin
from django.utils.html import format_html
from .models import Rede, Agencia, Consultor, Proprietario, Distrito, Concelho, Freguesia, Anunciante, Imovel, PerfilUtilizador

# ============================================
# CONFIGURAÇÃO DO PAINEL ADMIN
# ============================================

@admin.register(Rede)
class RedeAdmin(admin.ModelAdmin):
	list_display = ('id_rede', 'nome')
	search_fields = ('nome',)


@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
	list_display = ('id_agencia', 'nome', 'id_rede')
	search_fields = ('nome',)
	list_filter = ('id_rede',)


@admin.register(Consultor)
class ConsultorAdmin(admin.ModelAdmin):
	list_display = ('id_consultor', 'nome', 'id_agencia')
	search_fields = ('nome',)
	list_filter = ('id_agencia',)


@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):
	list_display = ('id_proprietario', 'nome')
	search_fields = ('nome',)


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
	list_display = ('id_distrito', 'nome')
	search_fields = ('nome',)


@admin.register(Concelho)
class ConcelhoAdmin(admin.ModelAdmin):
	list_display = ('id_concelho', 'nome', 'id_distrito')
	search_fields = ('nome',)
	list_filter = ('id_distrito',)


@admin.register(Freguesia)
class FreguesiAdmin(admin.ModelAdmin):
	list_display = ('id_freguesia', 'nome', 'id_concelho')
	search_fields = ('nome',)
	list_filter = ('id_concelho',)


@admin.register(Anunciante)
class AnuncianteAdmin(admin.ModelAdmin):
	list_display = ('id_anunciante', 'email', 'telefone', 'get_tipo_display')
	search_fields = ('email',)
	list_filter = ('tipo',)
	fieldsets = (
		('Informação Pessoal', {
			'fields': ('email', 'telefone', 'tipo')
		}),
		('Referência', {
			'fields': ('id_proprietario', 'id_consultor', 'id_agencia')
		}),
	)


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
	list_display = ('id_imovel', 'morada', 'preco', 'numero_quartos', 'numero_wc', 'data_anuncio')
	search_fields = ('morada', 'descricao')
	list_filter = ('numero_quartos', 'numero_wc', 'data_anuncio', 'id_freguesia')
	fieldsets = (
		('Informação do Imóvel', {
			'fields': ('morada', 'descricao', 'area', 'imagem_principal')
		}),
		('Características', {
			'fields': ('numero_quartos', 'numero_wc', 'data_construcao')
		}),
		('Preço e Localização', {
			'fields': ('preco', 'id_freguesia')
		}),
		('Contacto', {
			'fields': ('id_anunciante',)
		}),
		('Data (Automática)', {
			'fields': ('data_anuncio', 'imagem_preview'),
			'classes': ('collapse',)
		}),
	)
	readonly_fields = ('data_anuncio', 'imagem_preview')

	def imagem_preview(self, obj):
		if obj.imagem_principal:
			return format_html('<img src="{}" style="max-width: 180px; height:auto;" />', obj.imagem_principal.url)
		return '-'
	imagem_preview.short_description = 'Pré-visualização'


@admin.register(PerfilUtilizador)
class PerfilUtilizadorAdmin(admin.ModelAdmin):
	list_display = ('user', 'tipo_utilizador', 'criado_em')
	list_filter = ('tipo_utilizador',)
	search_fields = ('user__username', 'user__email')
