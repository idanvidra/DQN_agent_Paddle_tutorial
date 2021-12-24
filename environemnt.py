'''
Inspired by shivajbd 
https://towardsdatascience.com/create-your-own-reinforcement-learning-environment-beb12f4151ef
https://github.com/shivaverma/Orbit
'''


import turtle


class Paddle():

    def __init__(self) -> None:

        self.done = False
        self.reward = 0
        self.hit, self.miss = 0, 0

        # background
        self.win = turtle.Screen()  # create screen
        self.win.title('Paddle')
        self.win.bgcolor('black')  # set background color
        self.win.tracer(0)
        self.win.setup(width=600, height=600)  # set screen as 600x600

        # paddle
        self.paddle = turtle.Turtle()
        self.paddle.shape('square')
        self.paddle.speed(0)
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)  # 1x5 paddle
        self.paddle.penup()  # no drawing while moving
        self.paddle.color('white')
        self.paddle.goto(0, -275)  # set paddle to bottom of the screen

        # ball
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.color('red')
        self.ball.penup()  # no drawing while moving
        self.ball.goto(0, 100)  # place the shape in the middle
        self.ball.dx = 0.5  # ball x-axis velocity
        self.ball.dy = -0.5  # ball y-axis velocity

        # soreboard
        self.score = turtle.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.hideturtle()  # make turtle invisable - hide the shape
        self.score.goto(0, 270)  # set scoreboard at the top of the screen
        self.score.penup()
        self.score.write("Hit: {}   Missed: {}".format(
            self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))

        # keyboard control
        self.win.listen()
        # call paddle_right on right arrow key click
        self.win.onkey(self.paddle_right, 'Right')
        # call paddle_left on left arrow key click
        self.win.onkey(self.paddle_left, 'Left')

    # paddle movement
    def paddle_right(self):
        x = self.paddle.xcor()  # get x coordinates of paddle
        if x < 225:
            self.paddle.setx(x+20)

    def paddle_left(self):
        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x-20)

    def run_frame(self):
        self.win.update()

        # ball movement
        # update the balls x coordiante using velocity
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        # update the balls y coordiante using velocity
        self.ball.sety(self.ball.ycor() + self.ball.dy)

        # ball collisions
        # collisions with walls
        if self.ball.xcor() > 290:  # ball touches right wall
            self.ball.setx(290)
            self.ball.dx *= -1  # reverse x axis velocity

        if self.ball.xcor() < -290:  # ball touches left wall
            self.ball.setx(-290)
            self.ball.dx *= -1  # reverse x axis velocity

        if self.ball.ycor() > 290:  # ball touches the ceiling
            self.ball.sety(290)
            self.ball.dy *= -1  # reverse y axis velocity

        # collision with ground
        if self.ball.ycor() < -290:  # ball touches ground
            self.ball.goto(0, 100)
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(
                self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 3  # reward -3 if ball touches ground
            self.done = True

        # collision with paddle
        if abs(self.ball.ycor() + 250) < 2 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
            self.ball.dy *= -1  # reverse y axis velocity
            self.hit += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(
                self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward += 3  # reward +3 if paddle touches ball

    # agent control

    def reset(self):
        self.paddle.goto(0, -275)
        self.ball.goto(0, 100)
        return [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball.dx, self.ball.dy]

    def step(self, action):
        '''
        # 0 move left
        # 1 do nothing
        # 2 move right
        '''
        self.reward = 0
        self.done = 0
        if action == 0:  # move paddle to the left
            self.paddle_left()
            self.reward -= 0.2  # reward - 0.1 so the agent saves on moves

        if action == 2:  # move paddle to the right
            self.paddle_right()
            self.reward -= 0.2

        self.run_frame()  # run the game for one frame, reward is also updated inside this func

        # create state vector
        state = [self.paddle.xcor(), self.ball.xcor(), self.ball.ycor(),
                 self.ball.dx, self.ball.dy]

        return self.reward, state, self.done


if __name__ == '__main__':
    env = Paddle()

    # main loop
    while True:
        env.run_frame()
