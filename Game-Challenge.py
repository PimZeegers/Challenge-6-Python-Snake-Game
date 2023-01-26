
import pygame
from pygame.locals import *
import time
import random
easteregg=[]

SIZE = 40 #Vakjes grootte,
BACKGROUND_COLOR = (33, 84, 27) #Achtergrond kleur
class Apple: #Class, met het ID "Apple"
    def __init__(self, parent_screen):#Defenitie met tijdelijke variablen
        self.parent_screen = parent_screen # Lock  positie op scherm
        self.image = pygame.image.load("resources/apple.png").convert() #Laad het plaatje naar het scherm
        self.x = 120 # Groote van de hitbox van de appel, X-as.
        self.y = 120 # Groote van de hitbox van de appel, Y-as.

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        if self.length == 10: #Bij .. lengte in blokken activeer de easteregg
            print("Gelukt!") # Print gelukt in de console voor conformatie dat het werkt, voegt niets toe aan de game, is ook niet in game te zien.
            self.image = pygame.image.load("resources/Easteregg.jpg").convert() # vervangt het plaatje van de slang naar gouden eieren.
            # Moet nog code toegevoegd worden dat de slang na 5 seconden weer terug veranderd in de normale slang.

class Game:  
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pim & Tibo's game")
        self.surface = pygame.display.set_mode((1000, 800)) #scherm-grootte instellen naar 
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"

        # als de snake de muur raakt 
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            raise "Collision Occured"

    def display_score(self):                                                    #Score displayen
        font = pygame.font.SysFont('arial',30)                                  #Font setting,arial grootte 30.
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))   #De score bepalen met behulp van de lengte van de slang
        self.surface.blit(score,(850,10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Opnieuw: Enter, Afsluiten: Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.25) # Snelheid van de slang, normaal .25

if __name__ == '__main__':
    game = Game()
    game.run()


