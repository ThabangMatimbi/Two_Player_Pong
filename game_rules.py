import pygame, random
import start_manu
from start_manu import Menu
import trained_model
from trained_model import Enemy
from trained_model import *



SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

print("Choose the target score")
best_of = input("Best of: ")


#speed = input("Choose speed number level (e.g 1 for Low Level): ")



class Game(object):
    def __init__(self):
        self.font = pygame.font.SysFont('Calibri', 15, False, False)
        self.ttf_font = pygame.font.SysFont('Calibri', 15, False, False)
        self.menu = Menu(("start","about","exit"),font_color=white,font_size=40)
        self.show_about_frame = False # True: display about frame of the menu
        self.show_menu = True # True: when we are playing the game
        # Create ball object
        self.ball = Ball(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
        # Create the player
        self.player = Player(50,SCREEN_HEIGHT / 2)
        # Create the enemy
        self.enemy = Enemy(SCREEN_WIDTH - 65,SCREEN_HEIGHT / 2)
        # Load beep sound
        self.beep_sound = pygame.mixer.Sound("blip_sound.ogg")
        # Count the score of the player
        self.player_score = 0
        # Count the score of the enemy
        self.enemy_score = 0
        

    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.show_menu and not self.show_about_frame:
                        if self.menu.state == 0:
                            self.show_menu = False
                            self.game_init()
                        elif self.menu.state == 1:
                            self.show_about_frame = True
                        elif self.menu.state == 2:
                            # User clicked exit
                            return True
                elif event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.show_about_frame = False

                elif event.key == pygame.K_UP:
                    self.player.go_up()
                elif event.key == pygame.K_DOWN:
                    self.player.go_down()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.stop()
            
        return False

    def run_logic(self):
        if not self.show_menu:
            self.ball.update()
            self.player.update(self.ball,self.beep_sound)
            self.enemy.update(self.ball,self.beep_sound)
            if self.ball.rect.x < 0:
                self.ball.reset()
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.enemy_score += 1
            elif self.ball.rect.x > SCREEN_WIDTH:
                self.ball.reset()
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.player_score += 1

    def game_init(self):
        # Return to the initial values
        # Set ball in the center of the screen
        self.ball.rect.centerx = SCREEN_WIDTH / 2
        self.ball.rect.centery = SCREEN_HEIGHT / 2
        # Set ball change_x and change_y initial values
        self.ball.speed_x = -5
        self.ball.speed_y = 0
        # Set player and enemy in the initial position
        self.player.rect.centery = SCREEN_HEIGHT / 2
        self.enemy.rect.centery = SCREEN_HEIGHT / 2
        # Set scores to 0
        self.player_score = 0
        self.enemy_score = 0
        
        

    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands
        screen.fill(silver)
        time_wait = False # True: when we have to wait at the end 
        # --- Drawing code should go here
        if self.show_menu:
            if self.show_about_frame:
                # Display the about frame
                self.display_message(screen,"More info will be added soon....Press 'Esc' to go back to the manu ---By Thabang Matimbi")

            else:
                # Display the menu
                self.menu.display_frame(screen)

        # Check if the player won the game
        elif self.player_score == int(best_of):
            self.display_message(screen,"Congratulations! You Won!",black)
            time_wait = True
            self.player_score = 0
            self.enemy_score = 0
            self.show_menu = True
            
        # Check if the enemy won the game
        elif self.enemy_score == int(best_of):
            self.display_message(screen,"You lost",red)
            time_wait = True
            self.player_score = 0
            self.enemy_score = 0
            self.show_menu = True
        else:
            # Display the game
            self.ball.draw(screen)
            self.player.draw(screen)
            self.enemy.draw(screen)
            # Draw center line
            for y in range(0,SCREEN_HEIGHT,20):
                pygame.draw.rect(screen,green, [SCREEN_WIDTH / 2, y, 2, 10])
            # Draw the score
            player_score_label = self.font.render(str(self.player_score),True,black)
            screen.blit(player_score_label,(270,10))
            enemy_score_label = self.font.render(str(self.enemy_score),True,black)
            screen.blit(enemy_score_label,(350,10))
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- This is for the game to wait a few seconds to display the message
        if time_wait:
            pygame.time.wait(3000)

    def display_message(self,screen,message,color=blue):
        label = self.font.render(message,True,color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)
        # Draw the label onto the screen
        screen.blit(label,(posX,posY))

class Ball(object):
    def __init__(self,x,y):
        # Create rect to represent the position of the ball
        self.rect = pygame.Rect(x,y,12,12)
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        # Check for limits
        if self.rect.top < 0:
            self.speed_y *= -1
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1
            self.rect.bottom = SCREEN_HEIGHT
        # Move left/right
        self.rect.x += self.speed_x
        # Move up/down
        self.rect.y += self.speed_y

    def reset(self):
        # Return to initial values
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2
        self.speed_x = -7
        self.speed_y = random.randint(-5,5)

    def draw(self,screen):
        pygame.draw.rect(screen,red,self.rect)




class Player(BallSpeed):
    
    def __init__(self,x,y):
        # Create rect to represent the position of the player
        self.rect = pygame.Rect(x,y,15,50)
        self.change = 0

    def update(self,ball,beep_sound):
        
        # Check for limits
        if self.rect.top <= 0 and self.change < 0:
            self.change = 0
        elif self.rect.bottom >= SCREEN_HEIGHT and self.change > 0:
            self.change = 0
        # Check if we hit the ball
        if self.rect.colliderect(ball.rect):
            # this is a random change in speed betweern -7 and 7
            ball.speed_y = random.randint(-BallSpeed(speed).ball_speed,BallSpeed(speed).ball_speed)
            ball.speed_x *= -1
            ball.rect.left = self.rect.right
            # Play effect sound
            beep_sound.play()
        # Move up/down
        self.rect.y += self.change

    def go_up(self):
        self.change = -BallSpeed(speed).ball_speed

    def go_down(self):
        self.change = BallSpeed(speed).ball_speed

    def stop(self):
        self.change = 0

    def draw(self,screen):
        # Draw the rectangle onto the screen
        pygame.draw.rect(screen,black,self.rect)


