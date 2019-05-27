
import turtle
import os
import random
import time
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

total_hp = 3
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
pen.write("Remaining HP A: {}  Remaining HP B: {}".format(hp_a, hp_b), align="center", font=("Courier", 24, "normal"))

# Bullet list
bullet_list_a = []
bullet_list_b = []

ballspeed = 10
last_move_a = ballspeed,0
last_move_b = -1 * ballspeed,0



# Functions
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
    pen.write("Remaining HP A: {}  Remaining HP B: {}".format(hp_a, hp_b), align="center", font=("Courier", 24, "normal"))

    for bullet in bullet_list_a + bullet_list_b:
        bullet.hideturtle()
    bullet_list_a = []
    bullet_list_b = []

    last_move_a = ballspeed,0
    last_move_b = -1 * ballspeed,0

# Main game loop
def make_move_a():
    up_or_down = random.randint(0,1)
    if up_or_down == 0:
        paddle_a_up()
    else:
        paddle_a_down()
    
    shoot = random.randint(0,50)
    if shoot == 0:
        paddle_a_shoot()

def make_move_b():
    up_or_down = random.randint(0,1)
    if up_or_down == 0:
        paddle_b_up()
    else:
        paddle_b_down()
    
    shoot = random.randint(0,50)
    if shoot == 0:
        paddle_b_shoot()
while True:
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
            bullet_list_a.remove(ball)


    for ball in bullet_list_b.copy():
        if ball.xcor() < -350:
            ball.hideturtle()
            bullet_list_b.remove(ball)


    # Paddle and ball collisions
    for ball in bullet_list_b.copy():
        if ball.xcor() < -340 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50:
            hp_a -= 1
            if hp_a > 0:
                pen.clear()
                pen.write("Remaining HP A: {}  Remaining HP B: {}".format(hp_a, hp_b), align="center", font=("Courier", 24, "normal"))
                ball.hideturtle()
                bullet_list_b.remove(ball)
            else:
                reset_game()
    for ball in bullet_list_a.copy():
        if ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
            hp_b -= 1
            if hp_b > 0:
                pen.clear()
                pen.write("Remaining HP A: {}  Remaining HP B: {}".format(hp_a, hp_b), align="center", font=("Courier", 24, "normal"))
                ball.hideturtle()
                bullet_list_a.remove(ball)
            else:
                reset_game()
        
    


