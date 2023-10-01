from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Prices
from .serializers import PricesSerializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class PricesViewSet(ModelViewSet):
    queryset = Prices.objects.all()
    serializer_class = PricesSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_price(self, request):
        user = request.user
        data = request.data
        try:
            if user.type == 'dono':
                Prices.objects.create(
                    barber_id=data['barber_id'],
                    cut_price=data['cut_price'],
                    cut_description=data['cut_description']
                )
                return Response({'message': 'Novo preço registrado'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Somente o dono da barbearia pode registrar um novo preço!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar novo preço!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_prices_by_barber(self, request):
        params = request.query_params
        try:
            prices = Prices.objects.filter(barber__barber_id=params['barber_id']).order_by('cut_price')
            serializer = PricesSerializers(prices, many=True)
            return Response({'message': 'Preços encontrados', 'prices': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar os preços de corte do barbeiro'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_all_prices(self, request):
        try:
            prices = Prices.objects.all().order_by('cut_price')
            serializer = PricesSerializers(prices, many=True)
            return Response({'message': 'Preços encontrados', 'prices': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar os preços de corte'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
