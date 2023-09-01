from django.shortcuts import redirect,render
# from pathlib import Path
# import pickle
# pedido = Path('preco.pkl')
# pedido.touch(exist_ok=True)
# carro={'hamburguer':20,'fritas':15,'coca':10}
# with open('preco.pkl', 'wb') as fp:
#             pickle.dump(carro, fp)

def index(request):
    
    return render( request ,'home.html')