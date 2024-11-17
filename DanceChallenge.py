import pgzrun
from random import randint
from pgzero.actor import Actor
import pygame

# Initialize audio
pygame.mixer.init()
pygame.mixer.music.load("NeverGonnaGive.mp3")
pygame.mixer.music.play(-1)

WIDTH = 800
HEIGHT = 600
CENTRE_X = WIDTH / 2
CENTRE_Y = HEIGHT / 2

# Game Variables
move_list = []
display_list = []

score1 = 0  # Player 1 score
score2 = 0  # Player 2 score
current_move1 = 0  # Player 1 current move
current_move2 = 0  # Player 2 current move
count = 4
dance_length = randint(3, 6)

say_dance = False
show_countdown = True
moves_complete = False
game_over = False
game_duration = 105
start_time = pygame.time.get_ticks()

# Actors
dancer1 = Actor("dancer-start")
dancer1.pos = CENTRE_X + 175, CENTRE_Y - 40

dancer2 = Actor("dancer2-start")  # Second dancer actor
dancer2.pos = CENTRE_X - 190, CENTRE_Y - 40  # Position to the right of dancer1

# Player 1 controls (arrows)
up = Actor("up")
up.pos = CENTRE_X + 175, CENTRE_Y + 110
right = Actor("right")
right.pos = CENTRE_X + 235, CENTRE_Y + 170
down = Actor("down")
down.pos = CENTRE_X+175, CENTRE_Y + 230
left = Actor("left")
left.pos = CENTRE_X +115, CENTRE_Y + 170

# Player 2 controls (WASD)
w = Actor("up")
w.pos = CENTRE_X - 190, CENTRE_Y + 110
d = Actor("right")
d.pos = CENTRE_X - 130, CENTRE_Y + 170
s = Actor("down")
s.pos = CENTRE_X - 190, CENTRE_Y + 230
a = Actor("left")
a.pos = CENTRE_X - 250, CENTRE_Y + 170

def draw():
    global game_over, score1, score2, say_dance, count, show_countdown

    screen.clear()
    screen.blit("stageup", (0, 0))
    dancer1.draw()
    dancer2.draw()  # Draw the second dancer
    up.draw()
    right.draw()
    down.draw()
    left.draw()
    w.draw()
    d.draw()
    s.draw()
    a.draw()
    screen.draw.text("Player 1 Score: " + str(score1), color="black", topright=(WIDTH - 150, 10))
    screen.draw.text("Player 2 Score: " + str(score2), color="black", topleft=(10, 10))

    if game_over:
        if score1 > score2:
            winner_text = "Player 1 Wins!"
        elif score2 > score1:
            winner_text = "Player 2 Wins!"
        else:
            winner_text = "It's a Tie!"

        screen.draw.text("Game Over!", color="black", topleft=(CENTRE_X - 130, 220), fontsize=60)
        screen.draw.text(winner_text, color="black", topleft=(CENTRE_X - 130, 300), fontsize=60)
        screen.draw.text("Final Scores - Player 1: " + str(score1) + " Player 2: " + str(score2), color="black", topleft=(CENTRE_X - 250, 350), fontsize=40)
    elif say_dance:
        screen.draw.text("Dance!", color="black", topleft=(CENTRE_X - 65, 150), fontsize=60)
    elif show_countdown:
        screen.draw.text(str(count), color="black", topleft=(CENTRE_X - 8, 150), fontsize=60)


def reset_dancers():
    if not game_over:
        dancer1.image = "dancer-start"
        dancer2.image = "dancer2-start"  # Reset second dancer image
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"
        w.image = "up"
        d.image = "right"
        s.image = "down"
        a.image = "left"


def update_dancer(dancer, move, player):
    if not game_over:
        if player == 1:
            if move == 0:
                up.image = "up-lit"
                dancer.image = "dancer-up"
            elif move == 1:
                right.image = "right-lit"
                dancer.image = "dancer-right"
            elif move == 2:
                down.image = "down-lit"
                dancer.image = "dancer-down"
            elif move == 3:
                left.image = "left-lit"
                dancer.image = "dancer-left"
        elif player == 2:
            if move == 0:
                w.image = "up-lit"
                dancer.image = "dancer2-up"
            elif move == 1:
                d.image = "right-lit"
                dancer.image = "dancer2-right"
            elif move == 2:
                s.image = "down-lit"
                dancer.image = "dancer2-down"
            elif move == 3:
                a.image = "left-lit"
                dancer.image = "dancer2-left"

        clock.schedule(reset_dancers, 0.5)


def display_moves():
    global move_list, display_list, dance_length, say_dance, show_countdown, current_move1, current_move2

    if display_list:
        this_move = display_list.pop(0)
        update_dancer(dancer1, this_move, player=1)
        update_dancer(dancer2, this_move, player=2)
        clock.schedule(display_moves, 1.5)  # Increase this value to slow down the moves
    else:
        say_dance = True
        show_countdown = False


def generate_moves():
    global move_list, display_list, dance_length, count, show_countdown, say_dance

    count = 4
    move_list = []
    display_list = []
    say_dance = False

    for _ in range(dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)

    show_countdown = True
    countdown()


def countdown():
    global count, game_over, show_countdown

    if count > 1:
        count -= 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()


def next_move(player):
    global dance_length, current_move1, current_move2, moves_complete

    if player == 1:
        if current_move1 < dance_length - 1:
            current_move1 += 1
        else:
            moves_complete = True
    else:
        if current_move2 < dance_length - 1:
            current_move2 += 1
        else:
            moves_complete = True


def on_key_up(key):
    global score1, score2, game_over, move_list, current_move1, current_move2

    if key == keys.UP:
        update_dancer(dancer1, 0, player=1)
        if move_list[current_move1] == 0:
            score1 += 1
            next_move(1)

    elif key == keys.RIGHT:
        update_dancer(dancer1, 1, player=1)
        if move_list[current_move1] == 1:
            score1 += 1
            next_move(1)

    elif key == keys.DOWN:
        update_dancer(dancer1, 2, player=1)
        if move_list[current_move1] == 2:
            score1 += 1
            next_move(1)

    elif key == keys.LEFT:
        update_dancer(dancer1, 3, player=1)
        if move_list[current_move1] == 3:
            score1 += 1
            next_move(1)

    elif key == keys.W:
        update_dancer(dancer2, 0, player=2)
        if move_list[current_move2] == 0:
            score2 += 1
            next_move(2)

    elif key == keys.D:
        update_dancer(dancer2, 1, player=2)
        if move_list[current_move2] == 1:
            score2 += 1
            next_move(2)

    elif key == keys.S:
        update_dancer(dancer2, 2, player=2)
        if move_list[current_move2] == 2:
            score2 += 1
            next_move(2)

    elif key == keys.A:
        update_dancer(dancer2, 3, player=2)
        if move_list[current_move2] == 3:
            score2 += 1
            next_move(2)



def update():
    global game_over, current_move1, current_move2, moves_complete
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
    if elapsed_time >= game_duration:
       end_game()


    if not game_over and moves_complete:
        generate_moves()
        moves_complete = False
        current_move1 = 0
        current_move2 = 0

def end_game():
    global game_over
    game_over = True


generate_moves()
pgzrun.go()
