from random import randint

import kivy
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.vector import Vector


class DemarrageWindow(Widget):
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

            # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1
        pass


class DemarrageApp(App):
    ball = ObjectProperty(None)

    def build(self):
        demarrageWindow = DemarrageWindow()
        demarrageWindow.serve_ball()
        Clock.schedule_interval(demarrageWindow.update, 1 / 60)
        return demarrageWindow


class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


if __name__ == '__main__':
    DemarrageApp().run()
