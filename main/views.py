from django.shortcuts import render

def homepage(request):
    return render(request, 'main/homepage.html')

def play_game(request):
    context = {
        'positions_list': ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX"]
    }
    return render(request, 'main/play_game.html', context)
