from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


# Create your views here.
def cadastro(request):
    # Redireciona user se ele já estiver logado
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method =="POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # strip = remove os espaços em branco
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.WARNING,  'Preencha todos os campos')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(request, constants.WARNING,
                                 'Digite duas senhas iguais')
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            # Mensagem de sucesso
            messages.add_message(request, constants.SUCCESS,
                                 'Usuário criado com sucesso')
            return render(request, 'cadastro.html')
        except:
            # Mensagem de erro
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema')
            return render(request, 'cadastro.html')


        # Return in terminal
        #print(nome, email, senha, confirmar_senha)
        # Return in browser
        #return HttpResponse(f'{nome}, {email}, {senha}, {confirmar_senha}')

def logar(request):
    # Redireciona user se ele já estiver logado
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome, password=senha)
        # print (user)

        if user is not None:
            # Logar o usuario
            login(request, user)
            return redirect('/divulgar/novo_pet')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
            return render(request, 'login.html')

        # return HttpResponse(f'{nome} {senha}')

def sair(request):
    logout(request)
    return redirect('/auth/login')