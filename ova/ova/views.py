from django.http import HttpResponse
from django.template import Template, context


def saludo(request): #primera vista
    
    doc_externo = open("C:/Users/gemac/OVA/templates/index.html")
    
    plt = Template(doc_externo.read())
    
    doc_externo.close()
    
    ctx = context()
    
    documento = plt.render(ctx)
    
    return HttpResponse(documento)
