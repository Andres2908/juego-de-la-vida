import pygame
import numpy as np
import time

pygame.init()

# Tamaño de la ventana de ejecución
width, height = 500, 500
screen = pygame.display.set_mode((height, width))

# Color del lienzo y y ejecución
bg = 255, 0, 57
screen.fill(bg)

# Número de cuadritos en el eje x Y y
nxC, nyC = 30, 30

# Tamaño de los cuadritos
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas
gameState = np.zeros((nxC, nyC))


# Automata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1


pauseExect = False

# Bucle de ejecución
while True:

    # Hacemos la copia del estado anterior
    newGameState = np.copy(gameState)

    # Limpiamos la pantalla cada décima de segundo
    screen.fill(bg)
    time.sleep(2)

    # Registramos eventos de teclado y ratón
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)
                             ), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
                # Evaluamos el estado de cada celda vecina
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                    gameState[(x) % nxC, (y-1) % nyC] + \
                    gameState[(x+1) % nxC, (y-1) % nyC] + \
                    gameState[(x-1) % nxC, (y) % nyC] + \
                    gameState[(x+1) % nxC, (y) % nyC] + \
                    gameState[(x-1) % nxC, (y+1) % nyC] + \
                    gameState[(x) % nxC, (y+1) % nyC] + \
                    gameState[(x+1) % nxC, (y+1) % nyC]

                print(n_neigh)

                # regla 1
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # regla 2
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Con esto generamos las cordenadas para que pinte los bordes de cada cuadrito
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCH, (y+1) * dimCH)]

            # Informamos en que pantalla y de que color quermos pintar los bordes
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)
    pygame.display.flip()
