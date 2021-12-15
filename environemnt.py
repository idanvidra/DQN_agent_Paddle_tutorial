'''
Inspired by shivajbd 
https://towardsdatascience.com/create-your-own-reinforcement-learning-environment-beb12f4151ef
https://github.com/shivaverma/Orbit
'''


import turtle

# background
win = turtle.Screen()  # create screen
win.title('Paddle')
win.bgcolor('black')  # set background color
win.tracer(0)
win.setup(width=600, height=600)  # set screen as 600x600

# paddle
paddle = turtle.Turtle()
paddle.shape('square')
paddle.speed(0)
paddle.shapesize(stretch_wid=1, stretch_len=5)  # 1x5 paddle
paddle.penup()  # no drawing while moving
paddle.color('white')
paddle.goto(0, -275)  # set paddle to bottom of the screen

# paddle movement


def paddle_right():
    x = paddle.xcor()  # get x coordinates of paddle
    if x < 225:
        paddle.setx(x+20)


def paddle_left():
    x = paddle.xcor()
    if x > -225:
        paddle.setx(x-20)


# keyboard control
win.listen()
win.onkey(paddle_right, 'Right')  # call paddle_right on right arrow key click
win.onkey(paddle_left, 'Left')  # call paddle_left on left arrow key click

# ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('red')
ball.penup()  # no drawing while moving
ball.goto(0, 100)  # place the shape in the middle
ball.dx = 0.05  # ball x-axis velocity
ball.dy = -0.05  # ball y-axis velocity

# soreboard
hit, miss = 0, 0  # init
score = turtle.Turtle()
score.speed(0)
score.color('white')
score.hideturtle()  # make turtle invisable - hide the shape
score.goto(0, 270)  # set scoreboard at the top of the screen
score.penup()
score.write(f"Hit: {hit} Missed: {miss}",
            align='center', font=('Courier', 24, 'normal'))

# main loop
while True:
    win.update()  # show screen continuesly

    # ball movement
    # update the balls x coordiante using velocity
    ball.setx(ball.xcor() + ball.dx)
    # update the balls y coordiante using velocity
    ball.sety(ball.ycor() + ball.dy)

    # ball collisions
    # collisions with walls
    if ball.xcor() > 290:  # ball touches right wall
        ball.setx(290)
        ball.dx *= -1  # reverse x axis velocity

    if ball.xcor() < -290:  # ball touches left wall
        ball.setx(-290)
        ball.dx *= -1  # reverse x axis velocity

    if ball.ycor() > 290:  # ball touches the ceiling
        ball.sety(290)
        ball.dy *= -1  # reverse y axis velocity

    # collision with ground
    if ball.ycor() < -290:  # ball touches ground
        ball.goto(0, 100)

    # collision with paddle
    if abs(ball.ycor() + 250) < 2 and abs(paddle.xcor() - ball.xcor()) < 55:
        ball.dy *= -1  # reverse y axis velocity
