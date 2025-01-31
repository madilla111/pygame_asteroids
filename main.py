import sys
import pygame
from player import *
from asteroid import *
from asteroidfield import *
from constants import *

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    
    player = Player((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2))
    

    
    
    while True:
        #aparently you need this
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
                
                
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("ouch!")
                
            for bullet in shots:
                if asteroid.collision(bullet):
                    bullet.kill()
                    asteroid.split()
                    break

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
            
        pygame.display.flip()
        #limits frame rate to 60fps
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
