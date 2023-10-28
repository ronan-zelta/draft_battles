from django.shortcuts import render
from rest_framework import generics, status, views
from .models import NFLPlayer
from .serializers import NFLPlayerSerializer
from rest_framework.response import Response

class PlayerList(generics.ListCreateAPIView):
    queryset = NFLPlayer.objects.all()
    serializer_class = NFLPlayerSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NFLPlayer.objects.all()
    serializer_class = NFLPlayerSerializer
    lookup_field = 'uid'

class PlayerYearPoints(views.APIView):

    def get(self, request, uid, year):
        try:
            # Retrieve the player using the provided uid
            player = NFLPlayer.objects.get(uid=uid)
        except NFLPlayer.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get fantasy points for the given year using Python's getattr function
        fantasy_points = getattr(player, f"fp_{year}", None)

        # Check if points data exists for the given year
        if fantasy_points is None:
            return Response({"error": f"No data available for year {year}"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"player_uid": uid, "year": year, "fantasy_points": fantasy_points})