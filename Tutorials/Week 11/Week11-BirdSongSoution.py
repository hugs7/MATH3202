def f_sing(s):
    return 12 + .002*s

def f_forage(s):
    return 8 + .007*s

p_sing = .004
p_food = .6
rest_food = 3.6
food_patch = 32

def songD(t,x,m):
    if x < 0:
        s = int(x) - 1
    else:
        s = int(x)
    p = x - s
    return p*song(t,s+1,m)[0] + (1-p)*song(t,s,m)[0]
 
def songB(t,s,m):
    # uncomment to see result without "blurring"
    # return songD(t,s,m)
    return .25*songD(t,s-6.4,m) + .5*songD(t,s,m) + .25*songD(t,s+6.4,m)

   
song_ = {}   
def song(t,s,m):
    if s <= 0:
        return (0, 'Dead')
    elif t == 150:
        if m == 'Y':
            return (2, 'Mate')
        else:
            return (1, 'Lonely')
    
    if (t,s,m) not in song_:
        if t >= 75:
            song_[t,s,m] = (songB(t+1,s-rest_food,m), 'Rest')
        else:
            rest = songB(t+1,s-rest_food,m)
            sing = p_sing*songB(t+1,s-f_sing(s),'Y') + \
                (1-p_sing)*songB(t+1,s-f_sing(s),m)
            forage = p_food*songB(t+1,s-f_forage(s)+food_patch,m) + \
                (1-p_food)*songB(t+1,s-f_forage(s),m)
            song_[t,s,m] = (max((rest,'Rest'),(sing,'Sing'),(forage,'Forage')))
    
    return song_[t,s,m]

def sing(t):
    s = 1
    while song(t,s,'N')[1] != 'Sing':
        s = s + 1
    return s
    
import pylab
sings = [sing(t) for t in range(75)]
pylab.plot(range(75),sings)
pylab.xlabel('Time segment')
pylab.ylabel('Food reserve required to sing')
pylab.show()





