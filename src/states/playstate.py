import pygame
from src.player import Player
from src.letters import Letter
from src.letterspit import Letterspit
from src.enemy import Spitter
from src.turret import Turret
from src.bullet import Bullet 
import math
import random

pygame.font.init()


'''
State that is called during the main game
'''
class PlayState():

    def __init__(self):
        self.changeTo = None
        self.states = {"play", "intro", "pause", "setting"}
        self.player = None
        self.letter = []

        # Creates src.player.Player object
        self.player = Player()

        # Summons a letterspit and creates enemy list
        self.lettergen = Letterspit()
        self.lettergen.cap = 20
        self.lettergen.level = 1
        self.enemylist = [Spitter(100, (50, 50)),Spitter(100, (100, 100)),Spitter(100, (150, 150))]

        self.armageddon_status = False
        self.armageddon_cur = 0
        self.arma_counter = 0

        self.money = 0
        self.turrets = []
        self.money_font = pygame.font.SysFont("Arial", 50)


    def enter(self):
        # Armageddon happens at the start for testing purposes FOR NOW
        self.armageddon_status = True
        f = open('src/utilities/segmenttree.txt', 'r')
        self.arma = f.readlines()
        f.close()
        pass
  
    def exit(self):

        self.changeTo = None


    def armageddon(self):
        if self.armageddon_cur == 0:
            #start armageddon
            self.arma_counter = 0
        change = False
        y = 0
        if self.arma_counter % 5 == 0:
            for nxt in self.arma:
                y += 15
                relx, rely = 700, 0
                #angle = math.atan2(rely+random.randint(-30, 30), relx+ random.randint(-30, 30))
                angle = math.atan2(rely, relx)
                direction = {
                    "angle": angle,
                    "chx": math.cos(angle),
                    "chy": math.sin(angle)
                }
                if self.armageddon_cur < len(nxt):
                    change = True
                    if nxt[self.armageddon_cur] != " ":
                        self.letter.append(Letter(1, direction, (0, y), nxt[self.armageddon_cur], (255, 245, 255)))
            self.armageddon_cur += 1
            if not change:
                self.armageddon_status = False
        self.arma_counter += 1

    def update(self, keyspressed, keysdown):
        # Calls armageddon 
        if self.armageddon_status:
            self.armageddon()

        # Summons letters
        res = self.lettergen.update((self.player.x, self.player.y), None)
        if res != None:
            self.letter.append(res)
        self.player.update(keysdown)
        removelist = []

        # TODO: calculate bullet and letter collisions, update letter/bullet hp here
        for nxt in self.letter:
            for bullet in self.player.bulletList:
                bullet.update() 
                if bullet.body.colliderect(nxt.body):
                    bullet.hp -= 1
                    nxt.hp -= 5

                if bullet.hp <= 0 or bullet.distance > bullet.rRange:
                    removelist.append(bullet)
                
        # When letters hit the player, health and letter removal is executed here
        for nxt in self.letter:
            if self.player.body.colliderect(nxt.body):
                if self.player.hp.hp - nxt.hp >= 0:
                    self.player.hp.hp -= nxt.hp
                removelist.append(nxt)
        
        # Deletes old letters and awards money for killing letters 
        for nxt in self.letter:
            nxt.update()
            if nxt.hp <= 0:
                removelist.append(nxt)
                self.money += nxt.max_health
            elif nxt.x > 700 or nxt.x < 0 or nxt.y > 700 or nxt.x < 0:
                removelist.append(nxt)

        # Letter cleanup
        for nxt in removelist:
            if nxt in self.letter:
                self.letter.remove(nxt)

        reeemovelist = []
        for go in self.enemylist:
            for nxt in go.peons:
                nxt.update()
                if self.player.body.colliderect(nxt.body):
                    if self.player.hp.hp - 5 >= 0:
                        self.player.hp.hp -= 5
                    removelist.append(nxt)
                
                if self.player.attack.body and self.player.attack.body.colliderect(nxt.body):
                #two cases, letter has more or attack has more hp
                    tmp = self.player.attack.hp
                    self.player.attack.hp -= min(tmp, nxt.hp)
                    nxt.hp -= min(tmp, nxt.hp)

                if nxt.hp <= 0:
                    removelist.append(nxt)
                    self.money += nxt.max_health
                elif nxt.x > 700 or nxt.x < 0 or nxt.y > 700 or nxt.x < 0:
                    removelist.append(nxt)

            for nxt in removelist:
                if nxt in go.peons:
                    go.peons.remove(nxt)
            
            if self.player.attack.body and self.player.attack.body.colliderect(go.body):
                #two cases, letter has more or attack has more hp
                    tmp = self.player.attack.hp
                    self.player.attack.hp -= min(tmp, go.hp)
                    go.hp -= min(tmp, go.hp)

            if go.hp <= 0:
                self.money += go.max_health
                reeemovelist.append(go)

            go.update((self.player.x, self.player.y))
        
        for nxt in reeemovelist:
            self.enemylist.remove(nxt)

    def render(self, screen, h: float, w: float):
        self.player.render(screen, (h, w))
        for nxt in self.letter:
            nxt.render(screen, (h, w))
        for nxt in self.enemylist:
            for go in nxt.peons:
                go.render(screen, (h, w))
            nxt.render(screen)

        for nxt in self.player.bulletList:
            nxt.render(screen, (w, h))
        money_text = self.money_font.render("$"+str(self.money), False, (38,54,139))
        screen.blit(money_text, ((700-money_text.get_width())//2, 40))

