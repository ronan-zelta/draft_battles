from django.shortcuts import render, redirect

def homepage(request):
    return render(request, 'main/homepage.html')

def play_game(request):
    position_list = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX"]
    mode = request.GET.get('mode', '1qb').lower()

    if mode not in ['1qb', 'sflx']: 
        return redirect('/')

    if  mode == 'sflx': position_list[6] = "SFLX"
    context = {
        'positions_list': position_list,
        'mode': mode,
    }

    return render(request, 'main/play_game.html', context)
