import tensorflow as tf
from tensorflow import keras
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# config.log_device_placement = True 


from Snake import *
from keras.models import model_from_json

def runGameWithML(model,display,clock):
	maxScore = 3
	avgScore = 0
	testGames = 1000
	stepsPerGame = 2000


	for iteration in tqdm(range(testGames)):
		snakeStart, snakePosition, applePosition, score = startingPositions()

		countSameDirection = 0
		prevDirection = 0

		for _ in range(stepsPerGame):
			currentDirectionVector, isFrontBlocked, isLeftBlocked, isRightBlocked = blockedDirections(snakePosition)
			angle, snakeDirectionVector, appleDirectionVectorNormalised, snakeDirectionVectorNormalised = angleWithApple(snakePosition, applePosition)
			predictions = []

			predictedDirection = np.argmax(np.array(model.predict(np.array([isLeftBlocked,isFrontBlocked,isRightBlocked,appleDirectionVectorNormalised[0],snakeDirectionVectorNormalised[0],appleDirectionVectorNormalised[1],\
					snakeDirectionVectorNormalised[1]]).reshape(-1,7)))) -1

			if predictedDirection == prevDirection:
				countSameDirection += 1
			else:
				countSameDirection = 0
				prevDirection = predictedDirection

			newDirection = np.array(snakePosition[0]) - np.array(snakePosition[1])
			if predictedDirection == -1:
				newDirection = np.array([newDirection[1], -newDirection[0]])
			if predictedDirection == 1:
				newDirection = np.array([-newDirection[1], newDirection[0]])

			buttonDirection = generateButtonDirection(newDirection)

			nextStep = snakePosition[0] + currentDirectionVector
			if collisionWithWalls(snakePosition[0]) == 1 or collisionWithSelf(nextStep.tolist(), snakePosition) == 1:
				break

			snakePosition, applePosition, score = playGame(snakeStart, snakePosition, applePosition, buttonDirection, score, display, clock, iteration)

			if score > maxScore:
				maxScore = score

		avgScore += score

	return maxScore, avgScore / testGames

# jsonFile = open('model.json','r')
# loadedJsonModel = jsonFile.read()
# model = model_from_json(loadedJsonModel)
# model.load_weights('model.h5')

model = tf.keras.models.load_model('savedModel')
model.summary()


# # print(np.argmax(np.array(newModel.predict(np.array([0,0,0,0.948633,0,-0.1622777,\
# 					1]).reshape(-1,7)))) -1)



displayWidth = 500
displayHeight = 500
pygame.init()
display = pygame.display.set_mode((displayWidth,displayHeight))
clock=pygame.time.Clock()
maxScore, avgScore = runGameWithML(model, display, clock)
print("MAX SCORE: ", maxScore)
print("AVG SCORE: ", avgScore)