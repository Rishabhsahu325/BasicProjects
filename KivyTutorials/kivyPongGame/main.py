from kivy.app import App #base class for creating and starting kivy applications
from kivy.uix.widget import Widget #Widget class for all ui classes to inherit from
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
) 
#numberic property allows contraint to use only numeric values
#referenceList property automatically changes values of parameters used to create the reference list property
#objectProperty allows creating a reference to .kv file widgets withinthe python code
from kivy.vector import Vector #vector of cartesian coordinates
from kivy.clock import Clock #used to schedule events at specified intervals here


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    #objects in .kv file 
    #these are specified under ponggame widget 
    # and mapped to the file's widgets in the .kv file as ball: pong_ball
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App): #inheriting kivy's app class
    def build(self):  #overloading build method that defines behaviour on calling run method
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)#scheduling method calls of game object
        return game


if __name__ == '__main__':
    PongApp().run() #construct the application object then run it
