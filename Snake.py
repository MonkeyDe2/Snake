import pygame
import numpy as np
import time
import math
from tqdm import tqdm
import random


def collisionWithApple(applePosition, score):
	applePosition = [random.randrange(1,50)*10, random.randrange(1,50)*10]
	score += 1
	return applePosition, score

def collisionWithWalls(snakeHead):
	if snakeHead[0] >= 500 or snakeHead[0] <= 0 or snakeHead[1] >= 500 or snakeHead[1] <= 0:
		return 1
	else:
		return 0

def collisionWithSelf(snakeStart,snakePosition):
	# snakeHead = snakePosition[0]
	if snakeStart in snakePosition[1:]:
		return 1
	else:
		return 0 

def isDirectionBlocked(snakePosition, currentDirectionVector):
	nextStep = snakePosition[0] + currentDirectionVector
	snakeHead = snakePosition[0]
	if collisionWithWalls(snakeHead) == 1 or collisionWithSelf(snakeHead,snakePosition) == 1:
		return 1
	else:
		return 0

def generateSnake(snakeHead, snakePosition, applePosition, buttonDirection, score):
	if buttonDirection == 1:
		snakeHead[0] += 10
	elif buttonDirection == 0:
		snakeHead[0] -= 10
	elif buttonDirection == 2:
		snakeHead[1] += 10
	elif buttonDirection == 3:
		snakeHead[1] -= 10
	else:
		pass

	if snakeHead == applePosition:
		applePosition, score = collisionWithApple(applePosition, score)
		snakePosition.insert(0,list(snakeHead))
	else:
		snakePosition.insert(0,list(snakeHead))
		snakePosition.pop()

	return snakePosition, applePosition, score

def displaySnake(display,snakePosition):
	for position in snakePosition:
		pygame.draw.rect(display, (255,0,0), pygame.Rect(position[0],position[1],10,10))

def displayApple(display,applePosition):
	pygame.draw.rect(display,(0,255,0),pygame.Rect(applePosition[0],applePosition[1],10,10))

def playGame(snakeHead,snakePosition,applePosition,buttonDirection,score, display, clock, iteration=0):
	crashed = False
	# prevButtonDirection = 1
	# buttonDirection = 1
	# currentDirectionVector = np.array(snakePosition[0])-np.array(snakePosition[1])

	while crashed is not True:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				crashed = True


		display.fill((255,255,255))
	# 		if event.type == pygame.KEYDOWN:
	# 			if event.key == pygame.K_LEFT and prevButtonDirection != 1:
	# 				buttonDirection = 0
	# 			elif event.key == pygame.K_RIGHT and prevButtonDirection != 0:
	# 				buttonDirection = 1
	# 			elif event.key == pygame.K_UP and prevButtonDirection != 2:
	# 				buttonDirection = 3
	# 			elif event.key == pygame.K_DOWN and prevButtonDirection != 3:
	# 				buttonDirection = 2
	# 			else:
	# 				buttonDirection = buttonDirection

		# display.fill(windowColor)
		displayApple(display, applePosition)
		displaySnake(display, snakePosition)

		snakePosition, applePosition, score = generateSnake(snakeHead, snakePosition, applePosition, buttonDirection, score)
		pygame.display.set_caption("SCORE: " + str(score) + "    Iteration: "+str(iteration))
		pygame.display.update()
		# prevButtonDirection = buttonDirection
		# if isDirectionBlocked(snakePosition, currentDirectionVector) == 1:
		# 	crashed = True

		clock.tick(500000)
		return snakePosition, applePosition, score


def displayFinalScore(displayText, finalScore):
	largeText = pygame.font.Font('freesansbold.ttf', 35)
	TextSurf = largeText.render(displayText, True, black)
	TextRect = TextSurf.get_rect()
	TextRect.center = ((displayWidth/2), (displayHeight/2))
	display.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(2)



#######################################################################################################
def startingPositions():
	snakeStart = [100,100]
	snakePosition = [[100,100],[90,100],[80,100]]
	applePosition = [random.randrange(1,50)*10,random.randrange(1,50)*10]
	score = 3

	return snakeStart, snakePosition, applePosition, score

def blockedDirections(snakePosition):
	currentDirectionVector = np.array(snakePosition[0]) - np.array(snakePosition[1])
	leftDirectionVector = np.array([currentDirectionVector[1], -currentDirectionVector[0]])
	rightDirectionVector = np.array([-currentDirectionVector[1], currentDirectionVector[0]])

	isFrontBlocked = isDirectionBlocked(snakePosition, currentDirectionVector)
	isLeftBlocked = isDirectionBlocked(snakePosition, leftDirectionVector)
	isRightBlocked = isDirectionBlocked(snakePosition, rightDirectionVector)

	return currentDirectionVector, isFrontBlocked, isLeftBlocked, isRightBlocked

def appleDistanceFromSnake(applePosition, snakePosition):
	return np.linalg.norm(np.array(applePosition) - np.array(snakePosition[0]))

def angleWithApple(snakePosition, applePosition):
	appleDirectionVector = np.array(applePosition) - np.array(snakePosition[0])
	snakeDirectionVector = np.array(snakePosition[0]) - np.array(snakePosition[1])

	normOfAppleDirectionVector = np.linalg.norm(appleDirectionVector)
	normOfSnakeDirectionVector = np.linalg.norm(snakeDirectionVector)

	if normOfAppleDirectionVector == 0:
		normOfAppleDirectionVector = 10
	if normOfSnakeDirectionVector == 0:
		normOfSnakeDirectionVector = 10

	appleDirectionVectorNormalised = appleDirectionVector/normOfAppleDirectionVector
	snakeDirectionVectorNormalised = snakeDirectionVector/normOfSnakeDirectionVector
	angle = math.atan2(appleDirectionVectorNormalised[1] * snakeDirectionVectorNormalised[0] - appleDirectionVectorNormalised[0] * snakeDirectionVectorNormalised[1], \
		appleDirectionVectorNormalised[0] * snakeDirectionVectorNormalised[0] + appleDirectionVectorNormalised[1] * snakeDirectionVectorNormalised[1])/math.pi

	return angle, snakeDirectionVector, appleDirectionVectorNormalised, snakeDirectionVectorNormalised


def generateRandomDirection(snakePosition, angleWithApple):
	direction = 0

	if angleWithApple > 0:
		direction = 1
	elif angleWithApple < 0:
		direction = -1
	else:
		direction = 0

	return directionVector(snakePosition,angleWithApple,direction)

def directionVector(snakePosition, angleWithApple, direction):

	currentDirectionVector = np.array(snakePosition[0]) - np.array(snakePosition[1])
	leftDirectionVector = np.array([currentDirectionVector[1], -currentDirectionVector[0]])
	rightDirectionVector = np.array([-currentDirectionVector[1], currentDirectionVector[0]])

	newDirection = currentDirectionVector

	if direction == -1:
		newDirection = leftDirectionVector
	if direction == 1:
		newDirection = rightDirectionVector

	buttonDirection = generateButtonDirection(newDirection)

	return direction, buttonDirection

def generateButtonDirection(newDirection):
	buttonDirection = 0
	if newDirection.tolist() == [10,0]:
		buttonDirection = 1
	elif newDirection.tolist() == [-10,0]:
		buttonDirection = 0
	elif newDirection.tolist() == [0,10]:
		buttonDirection = 2
	else:
		buttonDirection = 3

	return buttonDirection

######################################################################################################################

# if __name__ == "__main__":

# 	displayWidth = 500
# 	displayHeight = 500
# 	green = (0,255,0)
# 	red = (255,0,0)
# 	black = (0,0,0)
# 	windowColor = (200,200,200)

# 	clock = pygame.time.Clock()

# 	snakeHead = [250,250]
# 	snakePosition = [[250,250],[240,250],[230,250]]
# 	applePosition = [random.randrange(1,50)*10,random.randrange(1,50)*10]

# 	score = 0

# 	pygame.init()

# 	display = pygame.display.set_mode((displayWidth, displayHeight))
# 	display.fill(windowColor)
# 	pygame.display.update()

# 	finalScore = playGame(snakeHead,snakePosition,applePosition,1,score)
# 	display = pygame.display.set_mode((displayWidth,displayHeight))
# 	display.fill(windowColor)
# 	pygame.display.update()

# 	displayText = 'Your Score is: ' + str(finalScore)
# 	displayFinalScore(displayText, finalScore)

# 	pygame.quit()
	