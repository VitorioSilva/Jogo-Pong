import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

pygame.mixer.music.load('musica.mpeg')
pygame.mixer.music.play(-1)

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Definição das variáveis do jogo
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
PADDLE_SPEED = 10
BALL_SPEED = 7

# Pontuação inicial
player_score = 0
opponent_score = 0

# Função para reiniciar o jogo
def reset_ball():
    return WIDTH // 2, HEIGHT // 2, random.choice([-1, 1]) * (BALL_SPEED_X - 2), random.choice([-1, 1]) * (BALL_SPEED_Y - 2)

# Desenha os elementos na tela
def draw_elements(player_paddle, opponent_paddle, ball):
    screen.fill(BLACK)
    pygame.draw.rect(screen, CYAN, player_paddle)
    pygame.draw.rect(screen, CYAN, opponent_paddle)
    pygame.draw.circle(screen, WHITE, (ball[0], ball[1]), BALL_RADIUS)
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    opponent_text = font.render(f"Opponent: {opponent_score}", True, WHITE)
    screen.blit(player_text, (50, 50))
    screen.blit(opponent_text, (WIDTH - 250, 50))

# Tela de opções
def options_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    start_text = font.render("Start", True, CYAN)
    quit_text = font.render("Quit", True, RED)
    screen.blit(start_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
    screen.blit(quit_text, (WIDTH // 2 - 50, HEIGHT // 2 + 50))
    pygame.display.update()
    selection = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selection = (selection + 1) % 2
                elif event.key == pygame.K_UP:
                    selection = (selection - 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selection == 0:
                        return True
                    else:
                        pygame.quit()
                        quit()
        screen.fill(BLACK)
        if selection == 0:
            pygame.draw.rect(screen, CYAN, (WIDTH // 2 - 60, HEIGHT // 2 - 60, 120, 50), 3)
        else:
            pygame.draw.rect(screen, RED, (WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 50), 3)
        screen.blit(start_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
        screen.blit(quit_text, (WIDTH // 2 - 50, HEIGHT // 2 + 50))
        pygame.display.update()

# Contagem regressiva
def countdown():
    font = pygame.font.Font(None, 48)
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        count_text = font.render(str(i), True, WHITE)
        screen.blit(count_text, (WIDTH // 2 - 20, HEIGHT // 2 - 20))
        pygame.display.update()
        time.sleep(1)

# Função principal do jogo
def main():
    global player_score, opponent_score
    clock = pygame.time.Clock()
    player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    while True:
        if options_screen():
            countdown()
            ball_x, ball_y, ball_dx, ball_dy = reset_ball()
            player_score = 0
            opponent_score = 0

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and player_paddle.y > 0:  
                    player_paddle.y -= PADDLE_SPEED
                if keys[pygame.K_s] and player_paddle.y < HEIGHT - PADDLE_HEIGHT:
                    player_paddle.y += PADDLE_SPEED
                if keys[pygame.K_UP] and opponent_paddle.y > 0: 
                    opponent_paddle.y -= PADDLE_SPEED
                if keys[pygame.K_DOWN] and opponent_paddle.y < HEIGHT - PADDLE_HEIGHT:
                    opponent_paddle.y += PADDLE_SPEED
                
                # Movimentação da bola
                ball_x += ball_dx
                ball_y += ball_dy
                
                # Verifica colisões da bola com as bordas
                if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
                    ball_dy = -ball_dy
                
                # Verifica colisões da bola com as paletas
                if ball_x - BALL_RADIUS <= player_paddle.x + PADDLE_WIDTH and player_paddle.y <= ball_y <= player_paddle.y + PADDLE_HEIGHT:
                    ball_dx = -ball_dx
                elif ball_x + BALL_RADIUS >= opponent_paddle.x and opponent_paddle.y <= ball_y <= opponent_paddle.y + PADDLE_HEIGHT:
                    ball_dx = -ball_dx
                
                # Verifica se a bola saiu pela lateral
                if ball_x - BALL_RADIUS == 0:
                    opponent_score += 1
                    ball_x, ball_y, ball_dx, ball_dy = reset_ball()
                elif ball_x + BALL_RADIUS == WIDTH:
                    player_score += 1
                    ball_x, ball_y, ball_dx, ball_dy = reset_ball()
                
                draw_elements(player_paddle, opponent_paddle, (ball_x, ball_y))
                pygame.display.update()
                clock.tick(60)

main()