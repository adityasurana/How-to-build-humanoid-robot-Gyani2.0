import random
play = random.randint(1)
if play == 0:
	os.system('vlc music1.mp3 vlc://quit') #music named "music1.mp3" will be played 
else:
	os.system('vlc music2.mp3 vlc://quit')
