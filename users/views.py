from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.contrib.auth import authenticate

from users.models import UserProfile, Barbers
from users.serializers import UserSerializer, BarbersSerializer

from utils import generate_random_password, send_email


class UserViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def register_user(self, request):
        data = request.data
        try:
            email = data['email']

            if UserProfile.objects.filter(email__iexact=email):
                return Response({'message': 'Um usuário com este email já existe.'}, status=status.HTTP_409_CONFLICT)

            first_name = data['full_name'].split(' ', 1)[0]

            user = UserProfile.objects.create(
                username=first_name,
                full_name=data['full_name'],
                email=data['email'],
                token_google=data['token_google']
            )

            user.set_password(data['password'])
            user.save()
            token = Token.objects.create(user=user)
            # token = Token.objects.create(user=users)
            # UserViewSet.send_email_confirm_user(user, request)
            return Response({'message': 'Usuário Cadastrado.'}, status=status.HTTP_200_OK)
            # return Response({'msg': 'Usuário Cadastrado.', 'token': user.auth_token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            # sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro no cadastro de usuário.', 'error': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        user = request.user
        data = request.data
        try:
            email = data['email'].strip()
            password = data['password']
            if UserProfile.objects.filter(email__iexact=email) or Barbers.objects.filter(email_barber__iexact=email):
                user_authenticate = UserProfile.objects.get(email=email, password=password)
                if user.type == 'cliente' or 'dono':
                    if user_authenticate:
                        serializer = UserSerializer(user_authenticate)
                        return Response({
                            'message': 'Login realizado com sucesso',
                            'user': serializer.data
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Senha inválida'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    if user.type == 'barbeiro':
                        barber_authenticate = Barbers.objects.get(email_barber=email, password=password)
                        if barber_authenticate:
                            serializer = BarbersSerializer(barber_authenticate)
                            return Response({
                                'message': 'Login realizado com sucesso',
                                'user': serializer.data
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({'message': 'Senha inválida'}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({
                            'message': 'Você não possui permissão para realizar o cadastro'
                        }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Não existe usuário com o email informado'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao realizar login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_user(self, request):
        try:
            user = UserProfile.objects.get(id=request.user.id)
            user.delete()
            return Response({'message': 'Sucesso Apagado!'},
                            status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'message': 'Usuario Nao Existente.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({'message': 'Nao Foi Possivel Deletar usuario, Entre em Contato com o Suporte.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_user(self, request):
        user = request.user
        data = request.data
        try:
            user.full_name = data['full_name']
            user.email = data['email']
            names = user.full_name.split(' ', 1)[0]
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ' '
            user.save()
            return Response({'message': 'Dados alterados com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar o usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_user(self, request):
        user = request.user
        try:
            user = UserProfile.objects.get(id=user.id)
            serializer = UserSerializer(user)
            return Response({'message': 'Perfil encontrado', 'user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar perfiL'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_user_by_id(self, request):
        params = request.query_params
        try:
            user = UserProfile.objects.get(id=params['user_id'])
            serializer = UserSerializer(user)
            return Response({'message': 'Usuário encontrado', 'user': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar usuário'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_users(self, request):
        try:
            users = UserProfile.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({'message': 'Usuários encontrados', 'users': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar usuários'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_users_by_type(self, request):
        params = request.query_params
        try:
            users = UserProfile.objects.filter(type=params['type_user']).order_by('id')
            serializer = UserSerializer(users, many=True)
            return Response({'message': 'Usuários encontrados', 'users': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar usuários'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def search_users(self, request):
        params = request.query_params
        try:
            users = UserProfile.objects.filter(username__icontains=params['name'])
            serializer = UserSerializer(users, many=True)
            return Response({'message': 'Usuário encontrado', 'user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar por usuário'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BarberViewSet(ModelViewSet):
    queryset = Barbers.objects.all()
    serializer_class = BarbersSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_barber(self, request):
        user = request.user
        data = request.data
        try:
            barber_id = data['barber_id']
            type_user = UserProfile.objects.get(id=barber_id)

            if (
                    UserProfile.objects.filter(email__iexact=data['email_barber']) or
                    Barbers.objects.filter(email_barber__iexact=data['email_barber'])
            ):
                return Response({'message': 'Um usuário com este email já existe.'}, status=status.HTTP_409_CONFLICT)

            if type_user.type != 'barbeiro':
                return Response({'message': 'Somente usuários do tipo barbeiro podem ser registrados'},
                                status=status.HTTP_400_BAD_REQUEST)

            if user.type == 'dono':
                random_password = generate_random_password()
                Barbers.objects.create(
                    company_id=user.owner_company.id,
                    barber_id=barber_id,
                    profile_photo=data.get('profile_photo', None),
                    password=random_password,
                    email_barber=data['email_barber']
                )
                message = (
                            f'O usuário {user.username} cadastrou você na barbearia {user.owner_company}. '
                            f'Sua senha de acesso é {random_password}'
                )
                send_email(data['email_barber'], 'Barbershop', message)

                return Response({'message': 'Barbeiro registrado com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Apenas o dono da barbearia pode adicionar novos barbeiros!'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Error ao registrar novo barbeiro!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def login_barber(self, request):
        user = request.user
        data = request.data
        try:
            email = data['email_barber'].strip()
            password = data['password']
            if user.type == 'barbeiro' or 'dono':
                if UserProfile.objects.filter(email__iexact=email) or Barbers.objects.filter(
                        email_barber__iexact=email):
                    user_authenticate = Barbers.objects.get(email_barber=email, password=password)
                    if user_authenticate:
                        serializer = BarbersSerializer(user_authenticate)
                        return Response({
                            'message': 'Login realizado com sucesso',
                            'user': serializer.data
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Senha inválida'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'message': 'Não existe usuário com o email informado'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Apenas usuários considerados barbeiros podem realizar este login!'},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao realizar login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_all_barbers(self, request):
        try:
            barbers = Barbers.objects.all()
            serializer = BarbersSerializer(barbers, many=True)
            return Response({'message': 'Barbeiros encontrados', 'barbers': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar barbeiros!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_barber(self, request):
        user = request.user
        data = request.data
        try:
            barber_id = data['barber_id']
            type_user = UserProfile.objects.get(id=barber_id)
            email = data['email_barber']

            if UserProfile.objects.filter(email__iexact=email):
                return Response({'message': 'Um usuário com este email já existe.'}, status=status.HTTP_409_CONFLICT)

            if type_user.type != 'barbeiro':
                return Response({'message': 'Somente usuários do tipo barbeiro podem ser registrados'},
                                status=status.HTTP_400_BAD_REQUEST)

            if user.type == 'dono':
                Barbers.objects.filter(pk=data['id']).update(
                    barber_id=data['barber_id'],
                    company_id=data['company_id'],
                    profile_photo=data.get('profile_photo', None),
                    email_barber=email
                )

                return Response({'message': 'Barbeiro atualizado com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Apenas o dono da barbearia pode atualizar barbeiros'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar barbeiro!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def barber_by_id(self, request):
        params = request.query_params
        try:
            barber = Barbers.objects.get(id=params['barber_id'])
            serializer = BarbersSerializer(barber)
            return Response({'message': 'Barbeiro encontrado com sucesso', 'barber': serializer.data},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Barbeiro não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar por barbeiro!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_barber(self, request):
        user = request.user
        data = request.data
        try:
            if user.type == 'dono':
                barber = Barbers.objects.get(id=data['barber_id'])
                if user in barber.company.owner.all():
                    barber.delete()
                    return Response({'message': 'Barbeiro deletado com sucesso'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Apenas o dono da barbearia pode deletar barbeiros'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Apenas o usuários do tipo dono podem deletar barbeiros'},
                                status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'message': 'Barbeiro não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao deletar barbeiro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def search_barber(self, request):
        params = request.query_params
        try:
            barber = Barbers.objects.filter(barber__username__icontains=params['barber_name'])
            serializer = BarbersSerializer(barber, many=True)
            return Response({'message': 'Barbeiro(s) encontrado(s)', 'barbers': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar barbeiro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def barbers_by_company(self, request):
        params = request.query_params
        try:
            barber = Barbers.objects.filter(company_id=params['company_id'])
            serializer = BarbersSerializer(barber, many=True)
            return Response({'message': 'Barbeiro(s) encontrado(s)', 'barbers': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar barbeiros'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
