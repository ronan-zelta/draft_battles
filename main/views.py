from django.shortcuts import render

def homepage(request):
    return render(request, 'main/homepage.html')

def play_game(request):
    return render(request, 'main/play_game.html')
