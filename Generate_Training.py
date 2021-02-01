from Snake import *

def generateTrainingDataY(snakePosition, angleWithApple, buttonDirection, direction, trainingDataY, isFrontBlocked, isLeftBlocked, isRightBlocked):
	if direction == -1:
		if isLeftBlocked == 1:
			if isFrontBlocked == 1 and isRightBlocked == 0:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, 1)
				trainingDataY.append([0,0,1])
			elif isFrontBlocked == 0 and isRightBlocked == 1:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, 0)
				trainingDataY.append([0,1,0])
			elif isFrontBlocked == 0 and isRightBlocked == 0:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, 1) 
				trainingDataY.append([0,0,1])
			 
		else:
			trainingDataY.append([1,0,0])
 
	elif direction == 0:
		if isFrontBlocked == 1:
			if isLeftBlocked == 1 and isRightBlocked == 0:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, 1)
				trainingDataY.append([0,0,1])
			elif isLeftBlocked == 0 and isRightBlocked == 1:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, -1)
				trainingDataY.append([1,0,0])
			elif isLeftBlocked == 0 and isRightBlocked == 0:
				trainingDataY.append([0,0,1])
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, 1)		   
		else:
			trainingDataY.append([0,1,0])
	else:
		if isRightBlocked == 1:
			if isLeftBlocked == 1 and isFrontBlocked == 0:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, 0)
				trainingDataY.append([0,1,0])
			elif isLeftBlocked == 0 and isFrontBlocked == 1:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, -1)
				trainingDataY.append([1,0,0])
			elif isLeftBlocked == 0 and isFrontBlocked == 0:
				direction, buttonDirection = directionVector(snakePosition, angleWithApple, -1)
				trainingDataY.append([1,0,0])			   
		else:
			trainingDataY.append([0,0,1])
	
	return direction, buttonDirection, trainingDataY

def generateTrainingData(display, clock):
	trainingDataX = []
	trainingDataY = []
	trainingGames = 1000
	stepsPerGame = 2000

	for iteration in tqdm(range(trainingGames)):
		snakeStart, snakePosition, applePosition, score = startingPositions()
		prevAppleDistance = appleDistanceFromSnake(applePosition, snakePosition)

		for _ in range(stepsPerGame):
			angle, snakeDirectionVector, appleDirectionVectorNormalised, snakeDirectionVectorNormalised = angleWithApple(snakePosition, applePosition)
			direction, buttonDirection = generateRandomDirection(snakePosition, angle)
			currentDirectionVector, isFrontBlocked, isLeftBlocked, isRightBlocked = blockedDirections(snakePosition)

			direction, buttonDirection, trainingDataY = generateTrainingDataY(snakePosition, angleWithApple, \
				buttonDirection, direction, trainingDataY,isFrontBlocked,isLeftBlocked, isRightBlocked)

			if isFrontBlocked == 1 and isLeftBlocked ==1 and isRightBlocked == 1:
				break

			trainingDataX.append([isLeftBlocked,isFrontBlocked,isRightBlocked,appleDirectionVectorNormalised[0], \
				snakeDirectionVectorNormalised[0], appleDirectionVectorNormalised[1], snakeDirectionVectorNormalised[1]])

			snakePosition, applePosition, score = playGame(snakeStart, snakePosition, applePosition, buttonDirection, score, display, clock, iteration)


	return trainingDataX, trainingDataY