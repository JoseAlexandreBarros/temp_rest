from django.shortcuts import render
from django.http import HttpResponse
from .models import Reservas,Carrinho
from pathlib import Path
import pickle
import os
import os.path
def reserva(request):
    
    
    nome= request.POST.get('nome')
    horario= request.POST.get('horario')
    local= request.POST.get('local')
    dia= request.POST.get('dia')
    dias=int(dia)
    if 'reservar' in request.POST:
        if  Reservas.objects.filter(nome=nome).exists():
            return render (request, 'home.html',{'mensagem':'Já há reserva para esse cliente'})

        if dias>31 or dias<1:
            return render (request, 'home.html',{'mensagem':'Dia do mês inválido'})
        
        if Reservas.objects.filter(horarios=horario).filter(locais=local).filter(data_reserva=dia).exists():
            return render (request, 'home.html',{'mensagem':'reserva indisponível'})
        
        reservas=Reservas(
            nome=nome,
            horarios=horario,
            locais=local,
            data_reserva=dia

        )

        reservas.save()
        
        

        return render (request, 'home.html',{'reservas': reservas})

    elif  'cancelar' in request.POST:
        if  Reservas.objects.filter(horarios=horario).filter(locais=local).filter(data_reserva=dia).filter(nome=nome).exists():
            Reservas.objects.filter(horarios=horario).filter(locais=local).filter(data_reserva=dia).filter(nome=nome).delete()
            return render (request, 'home.html',{'mensagem':'reserva cancelada'})
        else:
            return render (request, 'home.html',{'mensagem':'reserva inexistente'})
    
    
def registrar(request):
    Carrinho.objects.filter(atual='atual').update(atual='nulo')
    usuario= request.POST.get('usuario')
    identidade=1
    if not Carrinho.objects.filter(usuario=usuario).exists():
        carrinho=Carrinho(
            usuario=usuario,
            identidade=identidade,
            atual='atual'
        )
        carrinho.save()
        carr={}
        pedido = Path(f'{usuario}.pkl')
        pedido.touch(exist_ok=True)
        with open(f'{usuario}.pkl', 'wb') as fp:# o novo dicionário é salvo no arquivo do carrinho.
                pickle.dump(carr, fp)

    
    else:
         Carrinho.objects.filter(usuario=usuario).update(atual='atual')
         if not os.path.isfile(f'{usuario}.pkl'):
              pedido = Path(f'{usuario}.pkl')
              pedido.touch(exist_ok=True)
              carr={}
              with open(f'{usuario}.pkl', 'wb') as fp:# o novo dicionário é salvo no arquivo do carrinho.
                pickle.dump(carr, fp)
    carro=Carrinho.objects.get(atual='atual')
    with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
    with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
    total=0
    lista=[]
    for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price
    
    return render (request, 'home.html',{'mensagem3': f'{usuario}','mensagem': f'Você entrou com o pedido {usuario}','preco':total,'lista':lista,'carro':carros})
def adicionar_prato(request):
    
    pedido = Path('preco.pkl')
    pedido.touch(exist_ok=True)
    
    prato= request.POST.get('nome_prato')
    precos= request.POST.get('preco_prato')
    
    with open('preco.pkl', 'rb') as fp:
            preco = pickle.load(fp)
    if prato in preco.keys():
            return render (request,'home.html',{'prato':'prato já existente'})
    else:
        preco[prato]=precos
            
        with open('preco.pkl', 'wb') as fp:
            pickle.dump(preco, fp)
        return render (request,'home.html',{'prato': 'prato adicionado'})
    
def sair(request):
     
     Carrinho.objects.filter(atual='atual').update(atual='nulo')
     return render(request, 'home.html',{'mensagem':'saída do pedido atual'})

def ham(request):
     if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem2':'É necessário estar logado em um pedido para adicionar pratos'})
     else:
        
        carro=Carrinho.objects.get(atual='atual')
        with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
        if 'hamburguer' in carros.keys(): 
                carros['hamburguer']+=1
                with open(f'{carro}.pkl', 'wb') as fp:
                    pickle.dump(carros, fp)
        else:
            carros['hamburguer']=1
            with open(f'{carro}.pkl', 'wb') as fp:
                pickle.dump(carros, fp)

        # if not Carrinho.objects.filter(atual='atual').exists():
        #   return render (request,'home.html',{'mensagem':'É necessário estar logado em um pedido para gerenciar o pedido'})
     
        carro=Carrinho.objects.get(atual='atual')
        with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
        with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
        total=0
        lista=[]
        for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price

                
                
        return render (request,'home.html',{'mensagem3': f'{carro}','mensagem2': 'hamurguer adicionado ao pedido','preco':total,'lista':lista,'carro':carros})
     
    
def fritas(request):
     if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem2':'É necessário estar logado em um pedido para adicionar pratos'})
     else:
        carro=Carrinho.objects.get(atual='atual')

        with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
        if 'fritas' in carros.keys(): 
                carros['fritas']+=1
                with open(f'{carro}.pkl', 'wb') as fp:
                    pickle.dump(carros, fp)
        else:
            carros['fritas']=1
            with open(f'{carro}.pkl', 'wb') as fp:
                pickle.dump(carros, fp)

        if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem':'É necessário estar logado em um pedido para gerenciar o pedido'})
     
     carro=Carrinho.objects.get(atual='atual')
     with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
     with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
     total=0
     lista=[]
     for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price
        
     return render (request,'home.html',{'mensagem3': f'{carro}', 'mensagem2': 'fritas adicionado ao pedido','preco':total,'lista':lista,'carro':carros})
     
def coca(request):
     if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem2':'É necessário estar logado em um pedido para adicionar pratos'})
     else:
        carro=Carrinho.objects.get(atual='atual')
        

        with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
        if 'coca' in carros.keys(): 
                carros['coca']+=1
                with open(f'{carro}.pkl', 'wb') as fp:
                    pickle.dump(carros, fp)
        else:
            carros['coca']=1
            with open(f'{carro}.pkl', 'wb') as fp:
                pickle.dump(carros, fp)
        if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem':'É necessário estar logado em um pedido para gerenciar o pedido'})
     
     carro=Carrinho.objects.get(atual='atual')
     with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
     with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
     total=0
     lista=[]
     for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price
     return render (request,'home.html',{'mensagem3': f'{carro}','mensagem2': 'coca adicionado ao pedido','preco':total,'lista':lista,'carro':carros})
     
# def ir(request):
#      if not Carrinho.objects.filter(atual='atual').exists():
#           return render (request,'home.html',{'mensagem':'É necessário estar logado em um pedido para gerenciar o pedido'})
     
#      carro=Carrinho.objects.get(atual='atual')
#      with open(f'{carro}.pkl', 'rb') as fp: 
#             carros = pickle.load(fp)
#      with open('preco.pkl', 'rb') as fp: 
#             precos = pickle.load(fp)
     
#      total=0
#      lista=[]
#      for pratos in carros.keys():
#              if pratos in precos.keys():
#                 lista.append(pratos)
#                 price=int(precos[pratos])
#                 total+=carros[pratos]*price
     
     
#      return render (request,'pedidos.html',{'preco':total,'lista':lista,'carro':carros}) 

def retirar(request,pratos):
     carro=Carrinho.objects.get(atual='atual')
     with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
     carros.pop(pratos)
     with open(f'{carro}.pkl', 'wb') as fp: 
            carros = pickle.dump(carros,fp)

     
     with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
     with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
     total=0
     lista=[]
     for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price
     
     
     return render (request,'home.html',{'preco':total,'lista':lista,'carro':carros})

def voltar(request):
    return render( request ,'home.html')

def menu(request):
     with open('preco.pkl', 'rb') as fp: 
            menu = pickle.load(fp)
     
            
     if len(menu)==3:
          return render (request,'home.html',{'vazio':'No momento não há outros pratos. Adicione algum!'})
     if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem':'É necessário estar logado em um pedido para gerenciar o pedido'})
     
     carro=Carrinho.objects.get(atual='atual')
     with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
     with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
     total=0
     lista=[]
     for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price
     return render (request,'home.html',{'menu':menu,'preco':total,'lista':lista,'carro':carros})

def retirar_prato(request,prato):
     with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     precos.pop(prato)
     with open('preco.pkl', 'wb') as fp: 
            precos = pickle.dump(precos,fp)
     with open('preco.pkl', 'rb') as fp: 
            menu = pickle.load(fp)
     return render (request,'home.html',{'menu':menu})

def prato_pedido(request,prato):
     if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem2':'É necessário estar logado em um pedido para adicionar pratos'})
     else:
        carro=Carrinho.objects.get(atual='atual')
        

        with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
        if prato in carros.keys(): 
                carros[prato]+=1
                with open(f'{carro}.pkl', 'wb') as fp:
                    pickle.dump(carros, fp)
        else:
            carros[prato]=1
            with open(f'{carro}.pkl', 'wb') as fp:
                pickle.dump(carros, fp)
        if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem':'É necessário estar logado em um pedido para gerenciar o pedido'})
     
     carro=Carrinho.objects.get(atual='atual')
     with open(f'{carro}.pkl', 'rb') as fp: 
            carros = pickle.load(fp)
     with open('preco.pkl', 'rb') as fp: 
            precos = pickle.load(fp)
     
     total=0
     lista=[]
     for pratos in carros.keys():
             if pratos in precos.keys():
                lista.append(pratos)
                price=int(precos[pratos])
                total+=carros[pratos]*price
        
     return render (request,'home.html',{'mensagem3': f'{carro}','mensagem2': f'{prato} adicionado ao pedido','preco':total,'lista':lista,'carro':carros})
     
def deletar(request):
     if not Carrinho.objects.filter(atual='atual').exists():
          return render (request,'home.html',{'mensagem2':'É necessário estar logado para cancelar o pedido'})
     carro=Carrinho.objects.get(atual='atual')
     os.remove(f'{carro}.pkl')
     Carrinho.objects.filter(atual='atual').update(atual='nulo')
     return render (request,'home.html',{'mensagem2':'Seu pedido foi cancelado'})