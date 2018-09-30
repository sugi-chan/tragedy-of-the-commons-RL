from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop,Adam
import numpy as np
import pandas as pd
from tragedy import team
import itertools
from random import choice, randint
from keras.models import load_model

def use_predicted_probability(predicted_classs):
	
	if predicted_classs == 0:
		fish_to_play = 1
		
	elif predicted_classs == 1:
		fish_to_play = 2
		
	elif predicted_classs == 2:
		fish_to_play = 3
		
	elif predicted_classs == 3:
		fish_to_play = 4
		
	elif predicted_classs == 4:
		fish_to_play = 5
		
	elif predicted_classs == 5:
		fish_to_play = 6
		
	elif predicted_classs == 6:
		fish_to_play = 7
		
	elif predicted_classs == 7:
		fish_to_play = 8
		
	elif predicted_classs == 8:
		fish_to_play = 9
		
	elif predicted_classs == 9:
		fish_to_play = 10
		
	elif predicted_classs == 10:
		fish_to_play = 11
		
	elif predicted_classs == 11:
		fish_to_play = 12
		
	elif predicted_classs == 12:
		fish_to_play = 13
		
	elif predicted_classs == 13:
		fish_to_play = 14
		
	elif predicted_classs == 14:
		fish_to_play =15
		
	elif predicted_classs == 15:
		fish_to_play = 16
		
	elif predicted_classs == 16:
		fish_to_play = 17
		
	elif predicted_classs == 17:
		fish_to_play = 18
		
	elif predicted_classs == 18:
		fish_to_play = 19
		
	elif predicted_classs == 19:
		fish_to_play = 20
		
	return fish_to_play

def random_fish():
    fish_to_play = randint(0,19)
    return fish_to_play


class DQNLearner(team):
	def __init__(self):
		super().__init__()
		self._learning = True
		self._learning_rate = .1
		self._discount = .1
		self._epsilon = .8

		# Create Model
		# input. opp  last  played, player last played, opp_score,player_score, current_fishery_count, 
		model = Sequential()

		model.add(Dense(32, init='glorot_normal', activation = 'relu', input_dim=5))

		model.add(Dense(64, init='glorot_normal', activation = 'relu'))
		#model.add(Dense(128, init='glorot_normal', activation = 'relu'))
		#model.add(Dense(128, init='glorot_normal', activation = 'relu'))
		#output in this case should be a 60 way classification
		#representing the 60 ways you can choose 3 cards out of 5

		model.add(Dense(20, init='glorot_normal',activation='linear'))

		opt = RMSprop()
		model.compile(loss='mse', optimizer=opt)

		self._model = model



	def get_action(self, state):
		#need to modify the way that it does the prediction.... 
		#print(state.shape)
		#print(convert_card_list(state),convert_card_list(state).shape,type(convert_card_list(state)))

		#print('state in get action',state)
		fish_state_array = np.reshape(np.asarray(state), (1, 5))
		#print('np array',state)
		rewards = self._model.predict(fish_state_array, batch_size=1)

		predicted_classs = np.argmax(rewards)
		#print('class', predicted_classs, rewards.shape)
		#print('looking at weird thing',rewards[0][0],rewards[0][1],rewards)
		# can probably solve using a mapping of the actions and just outputing the label of the max of the chain
		if np.random.uniform(0,1) < self._epsilon:
			#get argmax of 60 way classification array
			# see use_predicted_probability() in choice testing notebook
			action = use_predicted_probability(predicted_classs)

		else:
			#if above the epsilon value, then choose one of 60
			# see picked_cards() in battle_prototype
			action = random_fish() #i can generate the permutations and throw the list in here

		self._last_state = fish_state_array
		self._last_action = action
		self._last_target = rewards


		return action
	
	def update(self,new_state,reward):
		if self._learning:
			#print('state in get action',new_state)
			fish_state_array = np.reshape(np.asarray(new_state), (1, 5))
			#print('np array',new_state)
			rewards = self._model.predict([fish_state_array], batch_size=1)
			maxQ = np.amax(rewards)
			new = self._discount * maxQ
			
			#### This looks annoying AF... 
			if self._last_action == 1:
				self._last_target[0][0] = reward+new

			elif self._last_action == 2:
				self._last_target[0][1] = reward+new

			elif self._last_action == 3:
				self._last_target[0][2] = reward+new

			elif self._last_action == 4:
				self._last_target[0][3] = reward+new

			elif self._last_action == 5:
				self._last_target[0][4] = reward+new

			elif self._last_action == 6:
				self._last_target[0][5] = reward+new

			elif self._last_action == 7:
				self._last_target[0][6] = reward+new

			elif self._last_action == 8:
				self._last_target[0][7] = reward+new

			elif self._last_action == 9:
				self._last_target[0][8] = reward+new

			elif self._last_action == 10:
				self._last_target[0][9] = reward+new

			elif self._last_action == 11:
				self._last_target[0][10] = reward+new

			elif self._last_action == 12:
				self._last_target[0][11] = reward+new

			elif self._last_action == 13:
				self._last_target[0][12] = reward+new

			elif self._last_action == 14:
				self._last_target[0][13] = reward+new

			elif self._last_action == 15:
				self._last_target[0][14] = reward+new

			elif self._last_action == 16:
				self._last_target[0][15] = reward+new

			elif self._last_action == 17:
				self._last_target[0][16] = reward+new

			elif self._last_action == 18:
				self._last_target[0][17] = reward+new

			elif self._last_action == 19:
				self._last_target[0][18] = reward+new

			elif self._last_action == 20:
				self._last_target[0][19] = reward+new

			
			#print('last_state', self._last_state[0])
			# Update model
			self._model.fit(self._last_state, self._last_target, batch_size=1, epochs=1, verbose=0)
	
	def save_rl_model(self,name_model):
		self._model.save(str(name_model)+'.h5')


	
