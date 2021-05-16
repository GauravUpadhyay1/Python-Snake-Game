import pygame
import random
import os
# initialization
x = pygame.init()
pygame.mixer.init()

# init colors
black = (0, 0, 0)
red = (255, 0, 0)
maroon = (153, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (2, 2, 255)
# screen variables
screen_width = 600
screen_height = 500
font = pygame.font.SysFont("Blade", 40, italic=True, bold=True)
font2 = pygame.font.SysFont("comicsansms", 50)
font3 = pygame.font.SysFont("comicsansms", 28)

# display
gamewindow = pygame.display.set_mode((screen_width, screen_height))

# game caption or name
pygame.display.set_caption("DesiSnake")
wel_img = pygame.image.load('img/snake3.jpg')
wel_img = pygame.transform.scale(wel_img, (200, 200)).convert_alpha()

# clock
clock = pygame.time.Clock()
pygame.display.update()


def welcome():
    pygame.mixer.music.load('audio\music.mp3')
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        gamewindow.fill(black)
        gamewindow.blit(wel_img, (200, 50))
        screen_text2("WELCOME TO SNAKES", red, 18,  240)
        screen_text3("Press enter to play", red, 170,  295)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    gameloop()
        pygame.display.update()
        clock.tick(60)


def plot(gamewindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.circle(gamewindow, yellow, (x, y), snake_size)


def screen_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def screen_text2(text, color, x, y):
    screen_text2 = font2.render(text, True, color)
    gamewindow.blit(screen_text2, [x, y])


def screen_text3(text, color, x, y):
    screen_text3 = font3.render(text, True, color)
    gamewindow.blit(screen_text3, [x, y])


def gameloop():
    fps = 60
    exit_game = False
    game_over = False
    food_x = random.randint(20, screen_width)
    food_y = random.randint(20, screen_height)
    snake_size = 10
    snake_x = 100
    snake_y = 120
    velocity_x = 0
    velocity_y = 0
    init_velocity = 4
    snake_list = []
    snake_length = 1
    score = 0

    if (not os.path.exists("score.txt")):
        with open('score.txt', 'w') as f:
            f.write("0")

    with open("score.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("score.txt", "w") as f:
                f.write(str(highscore))
            gamewindow.fill(black)
            screen_text(
                "Game Over! Press enter to continue ", maroon, 24, 225)
            screen_text(
                ("Your Score: " + str(score)), blue, 188, 259)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if abs(snake_x-food_x) < 7 and abs(snake_y-food_y) < 7:
                score += 10
                pygame.mixer.music.load('audio\quack.mp3')
                pygame.mixer.music.play()
                # print(score)
                food_x = random.randint(20, screen_width)
                food_y = random.randint(20, screen_height)
                snake_length += 4
                if score > int(highscore):
                    highscore = score

            if (len(snake_list) > snake_length):
                del snake_list[0]

            if (snake_x < 0) or (snake_x > screen_width) or (snake_y < 0) or (snake_y > screen_height):
                # pygame.mixer.music.load('audio\hiss.mp3')
                # pygame.mixer.music.play()
                pygame.mixer.music.load('audio/hiss.mp3')
                pygame.mixer.music.play()
                game_over = True

            if head in snake_list[0:-1]:
                pygame.mixer.music.load('audio/hiss.mp3')
                pygame.mixer.music.play()
                game_over = True

            gamewindow.fill(black)

            screen_text(("Score: " + str(score)), blue, 10, 10)
            screen_text(("High Score: " + str(highscore)), blue, 350, 10)
            pygame.draw.circle(gamewindow, red,
                               (food_x, food_y), snake_size)
        plot(gamewindow, yellow, snake_list, snake_size)
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


welcome()
