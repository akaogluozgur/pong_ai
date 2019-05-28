
import turtle
import os
import random
import time
from player import Player
from player import breed
from itertools import combinations
import operator
import numpy as np
import json
from datetime import datetime
import sys



wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)
wn.listen()

total_hp = 3
generation_num = 0
population_num = 10 # even number is required
children_number = 4
random_number = int(population_num/2) - children_number
max_round = 1000

cur_pop = []
for i in range(population_num):
    cur_pop.append(Player())

# Get file argument
arg_count = len(sys.argv)
args = sys.argv
print('Number of arguments:', arg_count, 'arguments.')
print('Argument List:', args)
if arg_count > 1:
    print("Using given file as initial weights!")
    read_file_name = args[1]
    generation_num = int(read_file_name.split("_")[1])
    f = open(read_file_name, "r")
    weights = json.load(f)
    for i in range(population_num):
        cur_weight = weights[str(i)]
        cur_pop[i].brain.set_weights(cur_weight)
        print(i, "th player's weights are set!")

combos = list(combinations(range(population_num),2))

p_a, p_b = None, None


# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5,stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5,stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

hp_a = total_hp
hp_b = total_hp

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)


# Bullet list
bullet_list_a = []
bullet_list_b = []

ballspeed = 10
last_move_a = ballspeed,0
last_move_b = -1 * ballspeed,0

clipsize = 3

# Functions
def save_pop_nn():
    output_dict = {}
    for ix, p in enumerate(cur_pop):
        weights_list = []
        for i in p.brain.get_weights():
            weights_list.append(i.tolist())
        output_dict[str(ix)] = weights_list
    file_name = "gen_" + str(generation_num)+ "_nn_weights_" + str(datetime.now()) + ".json"
    f = open(file_name, "w")
    json.dump(output_dict, f, indent=4, sort_keys=True)
    f.flush()
    f.close()

wn.onkeypress(save_pop_nn, "s")

def paddle_a_up():
    global last_move_a
    y = paddle_a.ycor()
    if y < 260: 
        y += 20
        paddle_a.sety(y)
        last_move_a = ballspeed, ballspeed

def paddle_a_down():
    global last_move_a
    y = paddle_a.ycor()
    if y > -240:
        y -= 20
        paddle_a.sety(y)
        last_move_a = ballspeed, -1 * ballspeed

def paddle_b_up():
    global last_move_b
    y = paddle_b.ycor()
    if y < 260:
        y += 20
        paddle_b.sety(y)
        last_move_b = -1 * ballspeed , ballspeed

def paddle_b_down():
    global last_move_b
    y = paddle_b.ycor()
    if y > -240:
        y -= 20
        paddle_b.sety(y)
        last_move_b = -1 * ballspeed, -1 * ballspeed

def paddle_a_shoot():
    if len(bullet_list_a) < 3:
        ball = turtle.Turtle()
        ball.speed(0)
        ball.shape("square")
        ball.color("white")
        ball.penup()
        y = paddle_a.ycor()
        x = paddle_a.xcor()
        ball.goto(x + 20, y)
        ball.dx, ball.dy =  last_move_a
        bullet_list_a.append(ball)

def paddle_b_shoot():
    if len(bullet_list_b) < 3:
        ball = turtle.Turtle()
        ball.speed(0)
        ball.shape("square")
        ball.color("red")
        ball.penup()
        y = paddle_b.ycor()
        x = paddle_b.xcor()
        ball.goto(x - 20, y)
        ball.dx, ball.dy =  last_move_b
        bullet_list_b.append(ball)

def reset_game():
    global paddle_a, paddle_b, pen, bullet_list_a, bullet_list_b, last_move_a, last_move_b, hp_a, hp_b, total_hp, wn

    
    paddle_a.setx(-350)
    paddle_a.sety(0)
    paddle_b.setx(350)
    paddle_b.sety(0)
    wn.update()
    
    hp_a = total_hp
    hp_b = total_hp
    pen.clear()
    pen.write("Rem HP A: {}  Rem HP B: {} --GN:{}".format(hp_a, hp_b, generation_num), align="center", font=("Courier", 24, "normal"))

    for bullet in bullet_list_a + bullet_list_b:
        bullet.hideturtle()
        bullet.clear()
        del bullet
    bullet_list_a = []
    bullet_list_b = []

    last_move_a = ballspeed,0
    last_move_b = -1 * ballspeed,0

# Main game loop
def make_move_a():
    global last_move_a
    inputs = [  hp_a, 
                hp_b, 
                clipsize - len(bullet_list_a),
                clipsize - len(bullet_list_b),
                paddle_a.ycor() + 50,
                paddle_a.ycor() - 50,
                paddle_b.ycor() + 50,
                paddle_b.ycor() - 50,
                last_move_a[1],
                last_move_b[1],
                 ]

    for index in range(clipsize):
        try:
            inputs.append(abs(paddle_a.xcor() - bullet_list_a[index].xcor()))
            inputs.append(bullet_list_a[index].ycor())
            inputs.append(abs(bullet_list_a[index].dx))
            inputs.append(bullet_list_a[index].dy)
        except:
            inputs.append(1000)
            inputs.append(1000)
            inputs.append(0)
            inputs.append(0)

    for index in range(clipsize):
        try:
            inputs.append(abs(paddle_b.xcor() - bullet_list_b[index].xcor()))
            inputs.append(bullet_list_b[index].ycor())
            inputs.append(abs(bullet_list_b[index].dx))
            inputs.append(bullet_list_b[index].dy)
        except:
            inputs.append(1000)
            inputs.append(1000)
            inputs.append(0)
            inputs.append(0)

    up_or_down, shoot = p_a.move(inputs)
    
    if up_or_down == -1:
        paddle_a_down()
    elif up_or_down == 0:
        last_move_a = ballspeed,0
    else:
        paddle_a_up()
   
    if shoot == 1:
        paddle_a_shoot()

def make_move_b():
    global last_move_b
    inputs = [  hp_b, 
                hp_a, 
                clipsize - len(bullet_list_b),
                clipsize - len(bullet_list_a),
                paddle_b.ycor() + 50,
                paddle_b.ycor() - 50,
                paddle_a.ycor() + 50,
                paddle_a.ycor() - 50,
                last_move_b[1],
                last_move_a[1],
                 ]

    for index in range(clipsize):
        try:
            inputs.append(abs(paddle_b.xcor() - bullet_list_b[index].xcor()))
            inputs.append(bullet_list_b[index].ycor())
            inputs.append(abs(bullet_list_b[index].dx))
            inputs.append(bullet_list_b[index].dy)
        except:
            inputs.append(1000)
            inputs.append(1000)
            inputs.append(0)
            inputs.append(0)

    for index in range(clipsize):
        try:
            inputs.append(abs(paddle_a.xcor() - bullet_list_a[index].xcor()))
            inputs.append(bullet_list_a[index].ycor())
            inputs.append(abs(bullet_list_a[index].dx))
            inputs.append(bullet_list_a[index].dy)
        except:
            inputs.append(1000)
            inputs.append(1000)
            inputs.append(0)
            inputs.append(0)

    up_or_down, shoot = p_b.move(inputs)
    
    if up_or_down == -1:
        paddle_b_down()
    elif up_or_down == 0:
        last_move_b = -1 * ballspeed,0
    else:
        paddle_b_up()
   
    if shoot == 1:
        paddle_b_shoot()


while True:    
    generation_num += 1
    if generation_num%2 == 0:
        save_pop_nn()
    pen.write("Rem HP A: {}  Rem HP B: {} --GN: {} Round {}/{}".format(hp_a, hp_b, generation_num,0,len(combos)), align="center", font=("Courier", 24, "normal"))
    # Round Starts
    for ix, combo in enumerate(combos):
        print("Generation:", generation_num, "Combination:", combo)
        pen.clear()
        pen.write("Rem HP A: {}  Rem HP B: {} --GN: {} Round {}/{}".format(hp_a, hp_b, generation_num, ix, len(combos)), align="center", font=("Courier", 24, "normal"))
        p_a = cur_pop[combo[0]]
        p_b = cur_pop[combo[1]]

        counter = max_round
        is_finished = False
        while not is_finished:
            counter -=1
            if counter == 0:
                p_a.score += (2*total_hp - (hp_a + hp_b))*0.2 + (hp_a - hp_b)
                p_b.score += (2*total_hp - (hp_a + hp_b))*0.2 + (hp_b - hp_a)
                reset_game()
                is_finished = True
                continue

            wn.update()
            
            move_func = {
                "0": make_move_a,
                "1":make_move_b
            }

            turn = random.randint(0, 1)
            move_func[str(turn)]()
            move_func[str(1 - turn)]()

            # Move the ball
            bullets = bullet_list_a + bullet_list_b
            for ball in bullets:
                ball.setx(ball.xcor() + ball.dx)
                ball.sety(ball.ycor() + ball.dy)


            # Border checking

            # Top and bottom
            for ball in bullets:
                if ball.ycor() > 290:
                    ball.sety(290)
                    ball.dy *= -1
                
            
                elif ball.ycor() < -290:
                    ball.sety(-290)
                    ball.dy *= -1
                

            # Left and right
            for ball in bullet_list_a.copy():
                if ball.xcor() > 350:
                    ball.hideturtle()
                    ball.clear()
                    bullet_list_a.remove(ball)
                    del ball


            for ball in bullet_list_b.copy():
                if ball.xcor() < -350:
                    ball.hideturtle()
                    bullet_list_b.remove(ball)
                    ball.clear()
                    del ball


            # Paddle and ball collisions
            for ball in bullet_list_b.copy():
                if ball.xcor() < -340 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50:
                    hp_a -= 1
                    if hp_a > 0:
                        pen.clear()
                        pen.write("Rem HP A: {}  Rem HP B: {} --GN: {} Round {}/{}".format(hp_a, hp_b, generation_num, ix, len(combos)), align="center", font=("Courier", 24, "normal"))
                        ball.hideturtle()
                        bullet_list_b.remove(ball)
                        ball.clear()
                        del ball
                    else:
                        p_a.score += (2*total_hp - (hp_a + hp_b))*0.2 + (hp_a - hp_b)
                        p_b.score += (2*total_hp - (hp_a + hp_b))*0.2 + (hp_b - hp_a)
                        reset_game()
                        is_finished = True
            for ball in bullet_list_a.copy():
                if ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
                    hp_b -= 1
                    if hp_b > 0:
                        pen.clear()
                        pen.write("Rem HP A: {}  Rem HP B: {} --GN: {} Round {}/{}".format(hp_a, hp_b, generation_num, ix, len(combos)), align="center", font=("Courier", 24, "normal"))
                        ball.hideturtle()
                        bullet_list_a.remove(ball)
                        ball.clear()
                        del ball
                    else:
                        p_a.score += (2*total_hp - (hp_a + hp_b))*0.2 + (hp_a - hp_b)
                        p_b.score += (2*total_hp - (hp_a + hp_b))*0.2 + (hp_b - hp_a)
                        reset_game()
                        is_finished = True

        print("Player A Total Score:", p_a.score, "Player B Total Score::", p_b.score)

    cur_pop.sort(key=operator.attrgetter('score'), reverse=True)

    cur_pop = cur_pop[: int(len(cur_pop)/2)]
    cur_pop_cp = cur_pop.copy()
    for i in range(children_number):
        father, mother = np.random.choice(cur_pop_cp, size = 2)
        child = breed(father, mother)
        cur_pop.append(child)

    for i in range(random_number):
        cur_pop.append(Player())
    
    for ix in range(len(cur_pop)):
        cur_pop[ix].score = 0

    


