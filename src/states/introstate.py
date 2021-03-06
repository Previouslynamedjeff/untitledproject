import pygame
from src.utilities.buttons import Button
from src.states.state import State


start = Button((500, 50), (100, 100), None)
setting = Button((500, 50), (100, 200), None)

'''
This state renders when the game begins, providing the player a menu to start their game
'''
class IntroState(State):

    def __init__(self):
        super().__init__()

    def enter(self):

        def escape1():
            self.changeTo = "play"

        def escape2():
            self.changeTo = "setting"
            
        start.function = escape1
        setting.function = escape2
  
    def exit(self):
        self.changeTo = None
  

    def update(self, keyspressed, keysdown):
        #update things
        start.update()
        setting.update()
    

    def render(self, screen, h: float, w: float):
        start.pos = (w // 2, h // 2 + 50)
        setting.pos = (w // 2, h // 2 - 50)
        start.render(screen)
        setting.render(screen)
