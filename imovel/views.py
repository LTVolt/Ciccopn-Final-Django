from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.db.models import Prefetch

from .models import Anunciante, Concelho, Distrito, Freguesia, Imovel, ImovelImagem, PerfilUtilizador
from .forms import ImovelForm, RegistoForm


MAX_IMAGENS_POR_ANUNCIO = 40


def _parse_int(value, min_value=None, max_value=None):
	try:
		parsed = int(value)
		if min_value is not None and parsed < min_value:
			return None
		if max_value is not None and parsed > max_value:
			return None
		return parsed
	except (TypeError, ValueError):
		return None


def _parse_decimal(value):
	try:
		if value in (None, ''):
			return None
		return Decimal(str(value))
	except (InvalidOperation, ValueError):
		return None


def _get_or_create_perfil(user):
	perfil, _ = PerfilUtilizador.objects.get_or_create(user=user)
	return perfil


def _get_anunciante_by_user(user):
	if not user.email:
		return None
	return Anunciante.objects.filter(email__iexact=user.email).first()


def _get_localizacao_context(post_data=None, imovel=None):
	distritos = Distrito.objects.all().order_by('nome')
	concelhos = Concelho.objects.select_related('id_distrito').all().order_by('nome')
	freguesias = Freguesia.objects.select_related('id_concelho__id_distrito').all().order_by('nome')

	selected_freguesia = ''
	selected_concelho = ''
	selected_distrito = ''

	if post_data is not None:
		selected_distrito = (post_data.get('distrito') or '').strip()
		selected_concelho = (post_data.get('concelho') or '').strip()
		selected_freguesia = (post_data.get('id_freguesia') or '').strip()
	elif imovel and imovel.id_freguesia_id:
		selected_freguesia = str(imovel.id_freguesia_id)
		selected_concelho = str(imovel.id_freguesia.id_concelho_id)
		selected_distrito = str(imovel.id_freguesia.id_concelho.id_distrito_id)

	if selected_freguesia and (not selected_concelho or not selected_distrito):
		freguesia = Freguesia.objects.select_related('id_concelho__id_distrito').filter(pk=selected_freguesia).first()
		if freguesia:
			if not selected_concelho:
				selected_concelho = str(freguesia.id_concelho_id)
			if not selected_distrito:
				selected_distrito = str(freguesia.id_concelho.id_distrito_id)

	return {
		'distritos': distritos,
		'concelhos': concelhos,
		'freguesias': freguesias,
		'selected_localizacao': {
			'distrito': selected_distrito,
			'concelho': selected_concelho,
			'freguesia': selected_freguesia,
		},
	}


def _guardar_imagens_galeria(imovel, imagens_upload):
	if not imagens_upload:
		return

	atual = imovel.imagens.count()
	espaco_disponivel = max(0, MAX_IMAGENS_POR_ANUNCIO - atual)
	if espaco_disponivel <= 0:
		return

	base_ordem = imovel.imagens.count()
	for idx, ficheiro in enumerate(imagens_upload[:espaco_disponivel], start=1):
		ImovelImagem.objects.create(
			id_imovel=imovel,
			imagem=ficheiro,
			ordem=base_ordem + idx,
		)


def home(request):
	total_imoveis = Imovel.objects.count()
	return render(request, 'imovel/home.html', {'total_imoveis': total_imoveis})


def lista_imoveis(request):
	distrito_id = request.GET.get('distrito', '').strip()
	concelho_id = request.GET.get('concelho', '').strip()
	freguesia_id = request.GET.get('freguesia', '').strip()
	tipologia_raw = request.GET.get('tipologia', '').strip()
	wc_raw = request.GET.get('numero_wc', '').strip()
	preco_min_raw = request.GET.get('preco_min', '').strip()
	preco_max_raw = request.GET.get('preco_max', '').strip()
	area_min_raw = request.GET.get('area_min', '').strip()
	area_max_raw = request.GET.get('area_max', '').strip()

	tipologia = _parse_int(tipologia_raw, 0, 9)
	numero_wc = _parse_int(wc_raw, 0, 9)
	preco_min = _parse_decimal(preco_min_raw)
	preco_max = _parse_decimal(preco_max_raw)
	area_min = _parse_decimal(area_min_raw)
	area_max = _parse_decimal(area_max_raw)

	imoveis = (
		Imovel.objects.select_related(
			'id_freguesia__id_concelho__id_distrito',
			'id_anunciante',
		)
		.prefetch_related(Prefetch('imagens', queryset=ImovelImagem.objects.order_by('ordem', 'id_imagem')))
		.all()
	)

	if distrito_id:
		imoveis = imoveis.filter(id_freguesia__id_concelho__id_distrito_id=distrito_id)
	if concelho_id:
		imoveis = imoveis.filter(id_freguesia__id_concelho_id=concelho_id)
	if freguesia_id:
		imoveis = imoveis.filter(id_freguesia_id=freguesia_id)
	if tipologia is not None:
		imoveis = imoveis.filter(numero_quartos=tipologia)
	if numero_wc is not None:
		imoveis = imoveis.filter(numero_wc=numero_wc)
	if preco_min is not None:
		imoveis = imoveis.filter(preco__gte=preco_min)
	if preco_max is not None:
		imoveis = imoveis.filter(preco__lte=preco_max)
	if area_min is not None:
		imoveis = imoveis.filter(area__gte=area_min)
	if area_max is not None:
		imoveis = imoveis.filter(area__lte=area_max)

	imoveis = imoveis.order_by('-data_anuncio')

	distritos = Distrito.objects.all().order_by('nome')
	concelhos = Concelho.objects.select_related('id_distrito').all().order_by('nome')
	freguesias = Freguesia.objects.select_related('id_concelho').all().order_by('nome')

	context = {
		'imoveis': imoveis,
		'distritos': distritos,
		'concelhos': concelhos,
		'freguesias': freguesias,
		'range_0_9': range(10),
		'selected': {
			'distrito': distrito_id,
			'concelho': concelho_id,
			'freguesia': freguesia_id,
			'tipologia': '' if tipologia is None else str(tipologia),
			'numero_wc': '' if numero_wc is None else str(numero_wc),
			'preco_min': preco_min_raw,
			'preco_max': preco_max_raw,
			'area_min': area_min_raw,
			'area_max': area_max_raw,
		},
	}

	return render(request, 'imovel/lista_imoveis.html', context)


def detalhe_imovel(request, id_imovel):
	imovel = get_object_or_404(
		Imovel.objects.select_related(
			'id_freguesia__id_concelho__id_distrito',
			'id_anunciante',
		).prefetch_related('imagens'),
		pk=id_imovel,
	)
	return render(request, 'imovel/detalhe_imovel.html', {'imovel': imovel})


def registo(request):
	if request.user.is_authenticated:
		return redirect('imovel:perfil')

	if request.method == 'POST':
		form = RegistoForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Conta criada com sucesso. Bem-vindo!')
			perfil = _get_or_create_perfil(user)
			if perfil.is_anunciante:
				return redirect('imovel:painel_anunciante')
			return redirect('imovel:perfil')
	else:
		form = RegistoForm()

	return render(request, 'imovel/registo.html', {'form': form})


def login_utilizador(request):
	if request.user.is_authenticated:
		return redirect('imovel:perfil')

	next_url = request.GET.get('next') or request.POST.get('next')

	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			perfil = _get_or_create_perfil(user)
			messages.success(request, 'Login efetuado com sucesso.')
			if next_url:
				return redirect(next_url)
			if perfil.is_anunciante:
				return redirect('imovel:painel_anunciante')
			return redirect('imovel:perfil')
	else:
		form = AuthenticationForm(request)

	return render(request, 'imovel/login.html', {'form': form, 'next': next_url})


@login_required
def perfil(request):
	perfil = _get_or_create_perfil(request.user)
	imoveis_associados = Imovel.objects.none()
	if perfil.is_anunciante and request.user.email:
		imoveis_associados = Imovel.objects.filter(id_anunciante__email=request.user.email)

	context = {
		'perfil': perfil,
		'imoveis_associados': imoveis_associados[:10],
		'total_imoveis_associados': imoveis_associados.count(),
	}
	return render(request, 'imovel/perfil.html', context)


@login_required
def painel_anunciante(request):
	perfil = _get_or_create_perfil(request.user)
	if not perfil.is_anunciante and not request.user.is_superuser:
		messages.error(request, 'Acesso reservado a contas do tipo Anunciante.')
		return redirect('imovel:perfil')

	imoveis = Imovel.objects.none()
	if request.user.email:
		imoveis = Imovel.objects.filter(id_anunciante__email=request.user.email).order_by('-data_anuncio')

	context = {
		'perfil': perfil,
		'imoveis': imoveis[:30],
		'total_imoveis': imoveis.count(),
	}
	return render(request, 'imovel/painel_anunciante.html', context)


@login_required
def criar_anuncio(request):
	perfil = _get_or_create_perfil(request.user)
	if not perfil.is_anunciante and not request.user.is_superuser:
		messages.error(request, 'Apenas contas de anunciante podem criar anúncios.')
		return redirect('imovel:perfil')

	anunciante = _get_anunciante_by_user(request.user)
	if not anunciante and not request.user.is_superuser:
		messages.error(
			request,
			'Não existe registo de anunciante com o seu email na base de dados. Contacte o administrador.',
		)
		return redirect('imovel:painel_anunciante')

	if request.method == 'POST':
		form = ImovelForm(request.POST, request.FILES)
		if form.is_valid():
			imagens_upload = request.FILES.getlist('galeria_imagens')
			if len(imagens_upload) > MAX_IMAGENS_POR_ANUNCIO:
				loc_ctx = _get_localizacao_context(post_data=request.POST)
				messages.error(
					request,
					f'Pode enviar no maximo {MAX_IMAGENS_POR_ANUNCIO} imagens por anuncio.',
				)
				return render(
					request,
					'imovel/form_anuncio.html',
					{
						'form': form,
						'modo': 'criar',
						'max_imagens': MAX_IMAGENS_POR_ANUNCIO,
						'imagens_atuais': 0,
						**loc_ctx,
					},
				)

			imovel = form.save(commit=False)
			if request.user.is_superuser and not anunciante:
				messages.error(request, 'Superutilizador sem email correspondente a anunciante. Defina um email com registo em anunciante.')
				return redirect('imovel:painel_anunciante')
			imovel.id_anunciante = anunciante
			imovel.save()
			_guardar_imagens_galeria(imovel, imagens_upload)
			messages.success(request, 'Anúncio criado com sucesso.')
			return redirect('imovel:painel_anunciante')
	else:
		form = ImovelForm()

	loc_ctx = _get_localizacao_context(post_data=request.POST if request.method == 'POST' else None)

	return render(
		request,
		'imovel/form_anuncio.html',
		{
			'form': form,
			'modo': 'criar',
			'max_imagens': MAX_IMAGENS_POR_ANUNCIO,
			'imagens_atuais': 0,
			**loc_ctx,
		},
	)


@login_required
def editar_anuncio(request, id_imovel):
	perfil = _get_or_create_perfil(request.user)
	if not perfil.is_anunciante and not request.user.is_superuser:
		messages.error(request, 'Apenas contas de anunciante podem editar anúncios.')
		return redirect('imovel:perfil')

	queryset = Imovel.objects.select_related('id_anunciante').prefetch_related('imagens')
	if request.user.is_superuser:
		imovel = get_object_or_404(queryset, pk=id_imovel)
	else:
		imovel = get_object_or_404(queryset, pk=id_imovel, id_anunciante__email__iexact=request.user.email)

	if request.method == 'POST':
		form = ImovelForm(request.POST, request.FILES, instance=imovel)
		if form.is_valid():
			imagens_upload = request.FILES.getlist('galeria_imagens')
			imagens_atuais = imovel.imagens.count()
			if imagens_atuais + len(imagens_upload) > MAX_IMAGENS_POR_ANUNCIO:
				loc_ctx = _get_localizacao_context(post_data=request.POST, imovel=imovel)
				messages.error(
					request,
					f'Este anúncio já tem {imagens_atuais} imagens. Só pode adicionar mais {max(0, MAX_IMAGENS_POR_ANUNCIO - imagens_atuais)}.',
				)
				context = {
					'form': form,
					'imovel': imovel,
					'modo': 'editar',
					'max_imagens': MAX_IMAGENS_POR_ANUNCIO,
					'imagens_atuais': imagens_atuais,
					**loc_ctx,
				}
				return render(request, 'imovel/form_anuncio.html', context)

			form.save()
			_guardar_imagens_galeria(imovel, imagens_upload)
			messages.success(request, 'Anúncio atualizado com sucesso.')
			return redirect('imovel:painel_anunciante')
	else:
		form = ImovelForm(instance=imovel)

	loc_ctx = _get_localizacao_context(post_data=request.POST if request.method == 'POST' else None, imovel=imovel)

	context = {
		'form': form,
		'imovel': imovel,
		'modo': 'editar',
		'max_imagens': MAX_IMAGENS_POR_ANUNCIO,
		'imagens_atuais': imovel.imagens.count(),
		**loc_ctx,
	}
	return render(request, 'imovel/form_anuncio.html', context)


@login_required
def apagar_anuncio(request, id_imovel):
	perfil = _get_or_create_perfil(request.user)
	if not perfil.is_anunciante and not request.user.is_superuser:
		messages.error(request, 'Apenas contas de anunciante podem eliminar anúncios.')
		return redirect('imovel:perfil')

	queryset = Imovel.objects.select_related('id_anunciante')
	if request.user.is_superuser:
		imovel = get_object_or_404(queryset, pk=id_imovel)
	else:
		imovel = get_object_or_404(queryset, pk=id_imovel, id_anunciante__email__iexact=request.user.email)

	if request.method == 'POST':
		confirmacao = request.POST.get('confirmacao', '').strip().lower()
		if confirmacao == 'apagar':
			imovel.delete()
			messages.success(request, 'Anúncio apagado com sucesso.')
			return redirect('imovel:painel_anunciante')
		messages.error(request, 'Para eliminar o anúncio, escreva a palavra "apagar".')

	return render(request, 'imovel/apagar_anuncio.html', {'imovel': imovel})


@login_required
def logout_utilizador(request):
	if request.method == 'POST':
		logout(request)
		messages.info(request, 'Sessão terminada com sucesso.')
		return redirect('imovel:home')
	return redirect('imovel:perfil')
