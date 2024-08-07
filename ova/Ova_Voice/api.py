# api.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET', 'POST'])
@csrf_exempt
def ova_api(request):
    if request.method == 'POST':
        # Aquí procesas los datos enviados desde Tkinter
        data = request.data
        # Procesa los datos según sea necesario
        return Response({'message': 'Datos recibidos', 'data': data})
    else:
        return Response({'message': 'API activa'})


