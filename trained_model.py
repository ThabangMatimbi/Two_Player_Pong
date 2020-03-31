import pygame, random

black = (0,0,0)
red = (255,0,0)
white = (255,255,255)
blue = (0,0,225)
green = (0,255,0)
silver = (192,192,192)




print("Use the number to choose the speed of the ball")
print(" 1 - Low level ")
print(" 2 - Medium level")
print(" 3 - Advanced level")
print(" 4 - Pro level")
speed = input("Choose speed number level (e.g 1 for Low Level): ")


class BallSpeed(object):
    def __init__(self, speed):
        self.speed = speed


    @property
    def ball_speed(self):
        if int(self.speed) == 1:
            ball_speed =5
            return ball_speed
        elif int(self.speed) ==2:
            ball_speed = 7
            return ball_speed
        elif int(self.speed) ==3:
            ball_speed = 10
            return ball_speed
        elif int(self.speed)==4:
            ball_speed =12
            return ball_speed
        else:
            print("Invalid number. Enter integer between 1 to 4")



class Enemy(BallSpeed):
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,50)

    def update(self,ball,beep_sound):
        
        if self.rect.centery > ball.rect.centery:
            diff = self.rect.centery - ball.rect.centery
            if diff <= BallSpeed(speed).ball_speed-1:
                self.rect.centery = ball.rect.centery
            else:
                self.rect.y -= BallSpeed(speed).ball_speed-3
        elif self.rect.centery < ball.rect.centery:
            diff = ball.rect.centery - self.rect.centery
            if diff <= 5:
                self.rect.centery = ball.rect.centery
            else:
                self.rect.y += BallSpeed(speed).ball_speed-3
        # Check if we hit the ball
        if self.rect.colliderect(ball.rect):
            ball.speed_x *= -1
            ball.rect.right = self.rect.left
            # Play effect sound
            beep_sound.play()

    def draw(self,screen):
        # Draw the rectangle onto the screen
        pygame.draw.rect(screen,black,self.rect)