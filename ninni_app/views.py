from typing import Mapping
from django.shortcuts import render, redirect
import random
import datetime

def index(request):
    return render(request, "index.html")

def init(request):                  # POST request
    request.session['gold_target'] = request.POST['target_gold']        # put the target_gold from form into the request session
    request.session['turn_target'] = request.POST['target_turns']       # ditto for target_turns
    request.session['gold_amount'] = 0
    request.session['turns_amount'] = 0
    request.session['activity_log'] = []
    return redirect('/home')

def home(request):
    return render(request, "home.html")

def process_farm(request):
    x = main(request, 10, 20, "farm")               # each method calls the "main" method to keep it DRY
    if x != None:                                   # if x comes back with a value then Gameover! 
        return render(request, "gameover.html")

    return render(request, "home.html")

def process_cave(request):
    x = main(request, 5, 10, "cave")
    if x != None:                  
        return render(request, "gameover.html")

    return render(request, "home.html")

def process_house(request):
    x = main(request, 2, 5, "house")
    if x != None:                  
        return render(request, "gameover.html")

    return render(request, "home.html")

def process_casino(request):
    x = main(request, -50, 50, "casino!")
    if x != None:                  
        return render(request, "gameover.html")

    return render(request,"home.html")

def main(request, num1, num2, type):                # the "main" method, where most of the fun happens

    gold = random.randint(num1, num2)
    request.session['gold_amount'] += gold
    request.session['turns_amount'] += 1

    x = request.session.get('gold_amount')          # "get" the session variables out to perform GameOver tests
    y = request.session.get('turns_amount')
    a = request.session.get('gold_target')
    b = request.session.get('turn_target')

    if int(x) >= int(a) and int(y) > int(b):         # needed to convert the values to (int)
        request.session['win'] = 'You are Winner!'
        return 1
    elif int(x) < int(a) and int(y) > int(b):
        request.session['win'] = 'You lose. Sad!'
        return 2

    time = datetime.datetime.today()
    if gold >= 0:
        activity = f'+{gold} gold pieces from the {type} {time.strftime("(%Y/%m/%d %I:%M %p)")}'
    else:
        activity = f'You lost {gold} gold pieces in the {type} {time.strftime("(%Y/%m/%d %I:%M %p)")}'
    request.session['activity_log'].append(activity)
    
    return 

def reset(request):
    request.session.flush()
    return redirect('/')

