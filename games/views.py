"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from games.models import Game
from games.serializers import GameSerializer
from datetime import date
from datetime import datetime 

def list_games(objects):
    lista = []
    for elemento in objects:
        lista.append(elemento['name'])
    return lista

@api_view(['GET', 'POST'])
def game_list(request):
    games = Game.objects.all()

    if request.method == 'GET':
        game_serializer = GameSerializer(games, many=True)
        return Response(game_serializer.data)

    elif request.method == 'POST':
        game_serializer = GameSerializer(data=request.data)
        game_listed = list_games(GameSerializer(games, many=True).data)
        
        if game_serializer.is_valid():
            name = request.data['name']
            if name in game_listed:
                return Response(game_serializer.errors, status=status.HTTP_409_CONFLICT)
            else:
                game_serializer.save()
                return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)

    elif request.method == 'PUT':
        game_serializer = GameSerializer(game, data=request.data)
        games = Game.objects.all()
        game_listed = list_games(GameSerializer(games, many=True).data)

        if game_serializer.is_valid():
            name = request.data['nome']
            if name in game_listed:
                return Response(game_serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
            else:
                game_serializer.save()
                return Response(game_serializer.data, status=status.HTTP_200_OK)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        current_date = date.today()
        game_date = game.release_date  

        if current_date > game_date:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            game.delete()
            return Response(status=status.HTTP_410_GONE)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
