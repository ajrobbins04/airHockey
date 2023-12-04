# Overview

This program gives players the chance to play air hockey against each other. One player 
uses the w, a, s, and d keys to move around the screen while the other player uses the
top, bottom, left, and right arrows. Technically this game is unfinished. Goals are not
recognized, but it will be implemented very soon along with a scoring system.

The game does try to use some laws of physics to make air hockey more realistic. The 
puck will eventually slow down if it goes too long without colliding with a moving
puck. And puck collisions with non-moving paddles will not provide a lot of momentum.

I wrote this software because game programming is something that I have some experience
in using C++. Those projects always taught me a lot, and its been a while since I've
taken a crack at a game program. I was excited to try out Pygame because I don't have
as much experience in Python. This is actually the first program that I've written in 
Python using classes, so everything about this project was very new to me even though I
already understood the concepts behind game programming.

[Software Demo Video](https://youtu.be/Nyj7BUMzjQM)

# Development Environment

This game was developed in Python using the Pygame
library and the math library.

Python version: 3.9.4
Pygame version: 2.5.2

# Useful Websites

* [Real Python](https://realpython.com/pygame-a-primer/)
* [Pygame Docs](https://www.pygame.org/docs/)
* [Elastic Collisions](https://www.hoomanr.com/Demos/Elastic2/)

# Acknowledgements
* Special thanks to [Joiro Hatgaya](https://www.dafont.com/8bit-wonder.font) for the awesome font used in the main menu and to github username [NITDgpOS](https://github.com/NITDgpOS/AirHockey) for the add_vectors() method.

# Future Work

* Must be able to recognize goals.
* Must track scores between players.
* Create better flow with main menu. Users cannot go back to menu after beginning a game.
* Give users the option to select the color of their paddles.
* Allow for pauses in the game. 

