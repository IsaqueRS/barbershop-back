from django.core.exceptions import ObjectDoesNotExist
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
                    cut_price=data['cut_price'],
                    cut_description=data['cut_description'],
                    cut_photo=data.get('cut_photo', '')
                )
                return Response({'message': 'Novo preço registrado'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Somente o dono da barbearia pode registrar um novo preço!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar novo preço!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_price(self, request):
        user = request.user
        data = request.data
        price_id = data['price_id']
        try:
            if user.type == 'dono':
                price = Prices.objects.get(id=price_id)
                if user in price.barber.company.owner.all():
                    Prices.objects.filter(id=price_id).update(
                        cut_price=data['cut_price'],
                        cut_description=data['cut_description'],
                        cut_photo=data.get('cut_photo', '')
                    )
                    return Response({'message': 'Preço atualizado'}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Somente o dono da barbearia ou os próprios barbeiros podem atualizar os preços!'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Somente usuários do tipo dono podem atualizar os preços!'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar novo preço!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def exclude_price(self, request):
        data = request.data
        user = request.user
        try:
            price = Prices.objects.get(id=data['price_id'])
            if user.type == 'dono':
                if user in price.barber.company.owner.all():
                    price.delete()
                    return Response({'message': 'Preço excluido com sucesso'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Apenas o(s) dono(s) da barbearia pode(m) excluir os preços dos cortes!'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Apenas usuários do tipo dono podem realizar esta ação!'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'message': 'Preço não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao excluir preço!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def price_by_id(self, request):
        params = request.query_params
        try:
            price = Prices.objects.get(id=params['price_id'])
            serializer = PricesSerializers(price)
            return Response({'message': 'Preço encontrado com sucesso', 'price': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Preço não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar preço!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_all_prices(self, request):
        try:
            prices = Prices.objects.all().order_by('cut_price')
            serializer = PricesSerializers(prices, many=True)
            return Response({'message': 'Preços encontrados', 'prices': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar os preços dos cortes!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def order_by_prices(self, request):
        sort_by = request.query_params.get('sort_by')
        try:
            prices = Prices.objects.filter()
            if sort_by == 'price_asc':
                price = prices.order_by('cut_price')
                serializer = PricesSerializers(price, many=True)
                return Response({'message': 'Preços encontrados', 'prices': serializer.data}, status=status.HTTP_200_OK)

            elif sort_by == 'price_desc':
                price = prices.order_by('-cut_price')
                serializer = PricesSerializers(price, many=True)
                return Response({'message': 'Preços encontrados', 'prices': serializer.data}, status=status.HTTP_200_OK)

            elif sort_by == '' or ' ' or None:
                price = prices.order_by('id')
                serializer = PricesSerializers(price, many=True)
                return Response({'message': 'Preços encontrados', 'prices': serializer.data}, status=status.HTTP_200_OK)

        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar preços!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

