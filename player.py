import pygame
from shot import *
from circleshape import *
from constants import *

class Player(CircleShape):
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.PLAYER_SPEED = 0
        self.count = 0
        self.old_rotation = pygame.Vector2(0, 1).rotate(self.rotation)
        self.forward = pygame.Vector2(0, 1)
        self.new_rotation = None
        self.rotation_history = []
        self.DELAY = 0
        self.slow_direction = None
        self.stopping = False
        self.shot_delay = 2
        
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        
    def clear(self):
        self.slow_direction = None
        self.old_rotation = None
        self.rotation_history = []
        self.stopping = False
        
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
    def shoot(self, dt):
        self.shot_delay += dt
        print(self.shot_delay)
        if self.shot_delay > 0.5:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_delay = 0
        
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Handle left rotation (counter-clockwise) - Only allow when moving
        if keys[pygame.K_a]:
            # if we are pressing W or S put in true to say we are moving and turning
            if keys[pygame.K_w] or keys[pygame.K_s]:
                self.rotate(-dt, True)
            else:
                self.rotate(-dt, False)
            
        # Handle right rotation (clockwise) - Only allow when moving
        if keys[pygame.K_d]:  # Allow rotation only if moving
            if keys[pygame.K_w] or keys[pygame.K_s]:
                self.rotate(dt, True)
            else:
                self.rotate(dt, False)
            
        # Handle forward movement (accelerating)
        if keys[pygame.K_w]:
            if self.stopping:
                self.clear()
            self.move(dt, True)
            if self.PLAYER_SPEED < PLAYER_SPEED_MAX:
                self.PLAYER_SPEED += 10  # Gradually increase speed
                
        # Handle backward movement (decelerating)
        if keys[pygame.K_s]:
            if self.stopping:
                self.clear()
            self.move(dt, True)
            if self.PLAYER_SPEED > PLAYER_SPEED_MAX_BACK:
                self.PLAYER_SPEED -= 10  # Gradually decrease speed
                
                # Handle stopping when no movement keys are pressed
        elif self.PLAYER_SPEED != 0 and not keys[pygame.K_w] and not keys[pygame.K_s]: 
            if self.stopping == False:
                self.stopping = True
                
            if self.slow_direction == None:
                self.slow_direction = self.rotation
                
            if self.PLAYER_SPEED < 0:
                self.PLAYER_SPEED += 5  # Gradual decrease in speed
                self.move(dt, False)
                
            elif self.PLAYER_SPEED > 0:                
                self.PLAYER_SPEED -= 5  # Gradual decrease in speed
                
                self.move(dt, False)
            if self.PLAYER_SPEED == 0:
                self.clear()
                
        if keys[pygame.K_SPACE]:
            self.shoot(dt)
        elif not keys[pygame.K_SPACE] and self.shot_delay < 1:
            self.shot_delay = 2



            
            
    def rotate(self, dt, moving):
        # Allow rotation only when the player is actively moving (pressing W or S)
        if abs(self.PLAYER_SPEED) > 0 and moving:  # Ensure the player is moving
            # Scale turn speed based on the player's current speed
            turn_scale = max(1.0 - abs(self.PLAYER_SPEED) / PLAYER_SPEED_MAX, 0.3)  # Scale turn speed as speed increases
            rotation_increment = PLAYER_TURN_SPEED * turn_scale * dt  # Apply scaled rotation speed
            
            # Update the rotation history
            self.rotation_history.append(self.rotation)
            
            # Update the rotation incrementally, applying the turn scale
            self.rotation += rotation_increment

            # Smoothly transition the forward direction (using old_rotation as the forward vector)
            target_rotation = pygame.Vector2(0, 1).rotate(self.rotation)  # The new forward direction based on the updated rotation
            self.old_rotation = self.old_rotation.lerp(target_rotation, 0.1)  # Interpolate between old and new rotation smoothly

        else:
            rotation_increment = PLAYER_TURN_SPEED * dt
            self.rotation += rotation_increment


        
    def move(self, dt, decel):
        #print(self.rotation)
        if decel and len(self.rotation_history) == 0:
            # Lock the travel direction when decelerating (not pressing W or S)
            self.old_rotation = pygame.Vector2(0, 1).rotate(self.rotation)
        elif not decel:
            # Clean up rotation history when not decelerating
            self.rotation_history = []
            self.old_rotation = pygame.Vector2(0, 1).rotate(self.slow_direction)

        # When not pressing W or S, do not change the direction (keep it locked)
        if abs(self.PLAYER_SPEED) > 0:
            # Apply delayed rotation from history if applicable
            if len(self.rotation_history) > 0:
                self.DELAY += dt  # Increment DELAY by dt for smooth time-based delay
                if self.DELAY >= 0.25:  # Set a reasonable delay (0.25s or adjust for smoothness)
                    self.old_rotation = pygame.Vector2(0, 1).rotate(self.rotation_history.pop())
                    self.DELAY = 0  # Reset delay after applying rotation

            elif len(self.rotation_history) == 0:
                self.DELAY = 0  # Reset DELAY when history is empty

            # Ensure the forward direction remains locked (do not rotate during deceleration)
            self.forward = self.old_rotation

        # Update position based on speed and forward direction
        self.position += self.forward * self.PLAYER_SPEED * dt

