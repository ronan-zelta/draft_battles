from django.test import TestCase
from rest_framework.test import APIClient
from .models import NFLPlayer


class PlayerListTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        NFLPlayer.objects.create(name="John Williams", uid="WillJo00", fp_2020=200)

    def test_list_players(self):
        response = self.client.get("/api/players/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Williams")

    
class PlayerDetailTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        NFLPlayer.objects.create(name="John Williams", uid="WillJo00", fp_2020=200)

    def test_retrieve_player(self):
        response = self.client.get("/api/players/WillJo00/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "John Williams")

    def test_player_not_found(self):
        response = self.client.get("/api/players/KeavRo99/")
        self.assertEqual(response.status_code, 404)


class PlayerYearPointsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        NFLPlayer.objects.create(name="John Williams", uid="WillJo00", fp_2020=200)

    def test_retrieve_player_year_points(self):
        response = self.client.get("/api/players/WillJo00/2020/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["fantasy_points"], 200)

    def test_no_data_for_year(self):
        response = self.client.get("/api/players/WillJo00/2021/")
        self.assertEqual(response.status_code, 404)

    def test_player_not_found_year_points(self):
        response = self.client.get("/api/players/KeavRo99/2020/")
        self.assertEqual(response.status_code, 404)


class PlayerSearchTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        NFLPlayer.objects.create(name="John Williams", uid="WillJo00", fp_2020=200)

    def test_search_players(self):
        response = self.client.get("/api/players/search/?q=John")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Williams")

    def test_search_players_empty_query(self):
        response = self.client.get("/api/players/search/")
        self.assertEqual(response.status_code, 400)
