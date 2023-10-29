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
    
class PlayerSearch(views.APIView):
    """
    Search for players based on a substring of their name.
    """

    def get(self, request):
        # Retrieve the search query from the query parameters
        search_term = self.request.query_params.get('q', None)
        
        if not search_term:
            return Response({"error": "A search query must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the players whose name contains a word which starts with query
        pattern = r'\b' + search_term
        players = NFLPlayer.objects.filter(name_searchable__iregex=pattern)
        
        # Serialize the filtered players
        serializer = NFLPlayerSerializer(players, many=True)

        return Response(serializer.data)