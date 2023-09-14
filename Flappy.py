import pygame
import random
import sys  # to exit game
from pygame.locals import *

FPS = 32
screen_width = 289
screen_height = 511


SCREEN = pygame.display.set_mode((screen_width, screen_height))
ground_y = screen_height * 0.8  # 80% of the pic will be considered

game_sprites = {}
game_sounds = {}

player = 'gallery/sprites/bird.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'


def welcomeScreen():

    playerX = int(screen_width / 5)
    playerY = int((screen_height - game_sprites['player'].get_height()) / 2)

    messageX = int((screen_height - game_sprites['message'].get_width()) / 2)
    messageY = int(screen_height * 0.13)
    baseX = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(game_sprites['background'], (0, 0))
                SCREEN.blit(game_sprites['player'], (playerX, playerY))
                SCREEN.blit(game_sprites['message'], (messageX, messageY))
                SCREEN.blit(game_sprites['base'], (baseX, ground_y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerX = int(screen_width / 5)
    playerY = int(screen_width / 2)
    baseX = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': screen_width + 200, 'y': newPipe1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': newPipe2[0]['y']},
    ]

    lowerPipes = [
        {'x': screen_width + 200, 'y': newPipe1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8           # velocity at time of flapping
    playerFlapped = False         # only when bird flaps

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    game_sounds['wing'].play()

        crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes)  # return true if player crashes

        if crashTest:
            return

            # check score
        playerMidPos = playerX + game_sprites['player'].get_width() /2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    print(f'''Your score is {score}''')
                    game_sounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
             playerFlapped = False
             playerHeight = game_sprites ['player'].get_height()
             playerY = playerY + min(playerVelY, ground_y - playerY - playerHeight)

                # moving pipes to left
        for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
             upperPipes['x'] += pipeVelX
             lowerPipes['x'] += pipeVelX
                # adding a new pipe when first one almost passes screen
        if 0 < upperPipes[0]['x'] < 5:
             newpipe = getRandomPipe()
             upperPipes.append(newpipe[0])
             lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < - game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(game_sprites['background'], (0,0))
        for upperPipes, lowerPipes in zip(upperPipes, lowerPipes):
            SCREEN.blit(game_sprites['pipe'][0], (upperPipes['x'], upperPipes['y']))
            SCREEN.blit(game_sprites['pipe'][1], (lowerPipes['x'], lowerPipes['y']))

        SCREEN.blit(game_sprites['base'], (baseX, ground_y))
        SCREEN.blit(game_sprites['player'], (playerX, playerY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
                width += game_sprites['numbers'][digit].get_width()
        Xoffset = (screen_width - width) / 2

        for digit in myDigits:
            SCREEN.blit(game_sprites['numbers'][digit], (Xoffset, screen_height * 0.12))
            Xoffset += game_sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerX, playerY, upperPipes, lowerPipes):
    if playerY > ground_y - 25 or playerY < 0:
        game_sounds['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and abs (playerX - pipe['x']))<game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playerY + game_sprites['player'].get_width() > pipe['y']) and abs(playerX - pipe['x']) < \
                game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True
    return False

def getRandomPipe():
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screen_height / 3
    y2 = offset + random.randrange(0, int(screen_height - game_sprites['base'].get_height() - 1.2 * offset))
    pipeX = screen_height + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Game By Elijah Turtel®')
    game_sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),

    )


    game_sprites['message'] = pygame.image.load('gallery/sprites/message.jpg').convert_alpha()
    game_sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
                            pygame.image.load(pipe).convert_alpha()
                            )

    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    game_sprites['background'] = pygame.image.load(background).convert()
    game_sprites['player'] = pygame.image.load(player).convert()


    while True:
        welcomeScreen()
        mainGame()



