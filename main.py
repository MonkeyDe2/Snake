from Snake import *
from Generate_Training import generateTrainingData
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

displayWidth = 500
displayHeight = 500

green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)

pygame.init()
display = pygame.display.set_mode((displayWidth, displayHeight))
clock=pygame.time.Clock()

trainingDataX, trainingDataY = generateTrainingData(display, clock)

model = Sequential()
model.add(Dense(units=9, input_dim=7))
model.add(Dense(units=15, activation='relu'))
model.add(Dense(units=3, activation='softmax'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

model.fit((np.array(trainingDataX).reshape(-1,7)),(np.array(trainingDataY).reshape(-1,3)), batch_size=256, epochs=3)

model.save('savedModel')
# model.save_weights('model.h5')
# model_json = model.to_json()
# with open('model.json','w') as json_file:
# 	json_file.write(model_json)

