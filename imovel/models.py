from django.db import models
from django.contrib.auth.models import User

# ============================================
# MODELO 1: REDE DE AGÊNCIAS
# ============================================
class Rede(models.Model):
	"""
	Representa uma rede/grupo de agências imobiliárias.
    
	Exemplo: "Century 21", "Remax", etc.
	"""
	id_rede = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=255)
    
	class Meta:
		db_table = 'rede'
		verbose_name = 'Rede'
		verbose_name_plural = 'Redes'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 2: AGÊNCIA
# ============================================
class Agencia(models.Model):
	"""
	Representa uma agência imobiliária.
	Uma agência pertence a uma rede.
    
	Exemplo: "Century 21 - Porto"
	"""
	id_agencia = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=255)
	id_rede = models.ForeignKey(
		Rede,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_rede'
	)
    
	class Meta:
		db_table = 'agencia'
		verbose_name = 'Agência'
		verbose_name_plural = 'Agências'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 3: CONSULTOR
# ============================================
class Consultor(models.Model):
	"""
	Representa um consultor/agente imobiliário.
	Um consultor trabalha numa agência.
	"""
	id_consultor = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=255)
	id_agencia = models.ForeignKey(
		Agencia,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_agencia'
	)
    
	class Meta:
		db_table = 'consultor'
		verbose_name = 'Consultor'
		verbose_name_plural = 'Consultores'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 4: PROPRIETÁRIO
# ============================================
class Proprietario(models.Model):
	"""
	Representa um proprietário de imóvel.
	"""
	id_proprietario = models.IntegerField(primary_key=True)
	nome = models.CharField(max_length=255)
    
	class Meta:
		db_table = 'proprietario'
		verbose_name = 'Proprietário'
		verbose_name_plural = 'Proprietários'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 5: DISTRITO
# ============================================
class Distrito(models.Model):
	"""
	Representa um distrito português.
    
	Exemplos: Porto, Lisboa, Aveiro, Braga, etc.
	"""
	id_distrito = models.CharField(max_length=9, primary_key=True)
	nome = models.CharField(max_length=255)
    
	class Meta:
		db_table = 'distrito'
		verbose_name = 'Distrito'
		verbose_name_plural = 'Distritos'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 6: CONCELHO
# ============================================
class Concelho(models.Model):
	"""
	Representa um concelho português.
	Um concelho pertence a um distrito.
    
	Exemplo: "Porto" pertence ao distrito "Porto"
	"""
	id_concelho = models.CharField(max_length=9, primary_key=True)
	nome = models.CharField(max_length=255)
	id_distrito = models.ForeignKey(
		Distrito,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_distrito'
	)
    
	class Meta:
		db_table = 'concelho'
		verbose_name = 'Concelho'
		verbose_name_plural = 'Concelhos'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 7: FREGUESIA
# ============================================
class Freguesia(models.Model):
	"""
	Representa uma freguesia portuguesa.
	Uma freguesia pertence a um concelho.
    
	Exemplo: "Cedofeita" pertence a "Porto"
	"""
	id_freguesia = models.AutoField(primary_key=True)
	codigo_freguesia = models.CharField(max_length=9, null=True, blank=True)
	nome = models.CharField(max_length=255)
	id_concelho = models.ForeignKey(
		Concelho,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_concelho'
	)
    
	class Meta:
		db_table = 'freguesia'
		verbose_name = 'Freguesia'
		verbose_name_plural = 'Freguesias'
    
	def __str__(self):
		return self.nome


# ============================================
# MODELO 8: ANUNCIANTE
# ============================================
class Anunciante(models.Model):
	"""
	Representa quem anuncia um imóvel.
	Pode ser um proprietário, consultor ou agência.
    
	Tipo:
	- 1 = Proprietário
	- 2 = Consultor
	- 3 = Agência
	"""
	TIPO_CHOICES = [
		(1, 'Proprietário'),
		(2, 'Consultor'),
		(3, 'Agência'),
	]
    
	id_anunciante = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=255)
	telefone = models.CharField(max_length=20)
	tipo = models.IntegerField(choices=TIPO_CHOICES)
    
	id_proprietario = models.ForeignKey(
		Proprietario,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_proprietario'
	)
	id_consultor = models.ForeignKey(
		Consultor,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_consultor'
	)
	id_agencia = models.ForeignKey(
		Agencia,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_column='id_agencia'
	)
    
	class Meta:
		db_table = 'anunciante'
		verbose_name = 'Anunciante'
		verbose_name_plural = 'Anunciantes'
    
	def __str__(self):
		return f"{self.email} ({self.get_tipo_display()})"
    
	def get_tipo_display_pt(self):
		"""Retorna o tipo em português"""
		return dict(self.TIPO_CHOICES).get(self.tipo, "Desconhecido")


# ============================================
# MODELO 9: IMÓVEL (Principal)
# ============================================
class Imovel(models.Model):
	"""
	Representa um imóvel à venda ou aluguer.
	Este é o modelo central do site imobiliário.
	"""
	id_imovel = models.AutoField(primary_key=True)
	morada = models.CharField(max_length=255)
	data_anuncio = models.DateTimeField(auto_now_add=True)
	preco = models.DecimalField(max_digits=12, decimal_places=2)
	descricao = models.TextField(null=True, blank=True)
	numero_quartos = models.PositiveIntegerField(default=0)
	numero_wc = models.PositiveIntegerField(default=0)
	imagem_principal = models.ImageField(upload_to='imoveis/', null=True, blank=True)
	data_construcao = models.DateField(null=True, blank=True)
	area = models.DecimalField(max_digits=6, decimal_places=2)
    
	id_anunciante = models.ForeignKey(
		Anunciante,
		on_delete=models.CASCADE,
		db_column='id_anunciante'
	)
	id_freguesia = models.ForeignKey(
		Freguesia,
		on_delete=models.CASCADE,
		db_column='id_freguesia'
	)
    
	class Meta:
		db_table = 'imovel'
		verbose_name = 'Imóvel'
		verbose_name_plural = 'Imóveis'
		ordering = ['-data_anuncio']  # Ordenar por mais recente primeiro
    
	def __str__(self):
		return f"{self.morada} - €{self.preco}"
    
	def get_preco_formatado(self):
		"""Retorna o preço formatado com símbolo de euro"""
		return f"€{self.preco:,.2f}"
    
	def get_localizacao(self):
		"""Retorna a localização completa (Distrito, Concelho, Freguesia)"""
		try:
			concelho = self.id_freguesia.id_concelho
			distrito = concelho.id_distrito if concelho else None
			partes = []
			if self.id_freguesia:
				partes.append(str(self.id_freguesia.nome))
			if concelho:
				partes.append(str(concelho.nome))
			if distrito:
				partes.append(str(distrito.nome))
			return ", ".join(partes)
		except:
			return "Localização desconhecida"


# ============================================
# MODELO 10: PERFIL DE UTILIZADOR
# ============================================
class PerfilUtilizador(models.Model):
	"""
	Perfil adicional do utilizador para definir o papel na aplicação.

	- COMUM: utilizador com acesso geral
	- ANUNCIANTE: utilizador com acesso a funcionalidades de anunciante
	"""
	TIPO_COMUM = 'COMUM'
	TIPO_ANUNCIANTE = 'ANUNCIANTE'

	TIPO_CHOICES = [
		(TIPO_COMUM, 'Utilizador comum'),
		(TIPO_ANUNCIANTE, 'Anunciante'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_imovel')
	tipo_utilizador = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_COMUM)
	criado_em = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'perfil_utilizador'
		verbose_name = 'Perfil de Utilizador'
		verbose_name_plural = 'Perfis de Utilizador'

	def __str__(self):
		return f"{self.user.username} - {self.get_tipo_utilizador_display()}"

	@property
	def is_anunciante(self):
		return self.tipo_utilizador == self.TIPO_ANUNCIANTE
