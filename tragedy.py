#play tragedy of the commons
import random
import math
#rl_model_name = 'altruistic_1_9_26'
rl_model_name = 'greed_1_9_26'

class team:
    def __init__(self,type=None):
        self.payoff = 0
        self.type = type
    def get_action(self, state =None):
        print('hi')
        
    

def player_type(type=None, fishery_status=None):
    
    dice_roll = random.randint(1,20)
    


    if type == 'greedy':
        if fishery_status > 18:
            fish_count = random.randint(5,8)
        elif fishery_status > 15:
            fish_count = random.randint(2,6)
        elif fishery_status > 12:
            fish_count = random.randint(5,20)
            
    elif type == 'con':
        if fishery_status > 18:
            fish_count = random.randint(3,5)
        elif fishery_status > 15:
            fish_count = random.randint(1,4)
        elif fishery_status > 12:
            fish_count = random.randint(1,3)

    return fish_count
    
    


class TOC:
    def __init__(self, num_learning_rounds =None, learner = None, report_every=1000):
        self._num_learning_rounds = num_learning_rounds
        self._report_every = report_every
        self.player = learner
        self.win = 0
        self.loss = 0
        self.tie = 0
        self.game = 1
        self.evaluation = False
        self.turn_record = []
        
    def play_game(self):
        
        p1,p2,initial_fishery,fishery_count = self.reset_game()
        #opp  last  played, player last played, opp_score,player_score,turn#, current_fishery_count, 
        state = [0,0,0,0,20]
        turn_count = 0
        while True:


            p1_fish_count = p1.get_action(state)
            p2_fish_count = player_type(type = p2.type,fishery_status = fishery_count)


            total_harvest = p1_fish_count + p2_fish_count

            fishery_count -= total_harvest

            turn_count +=1
          
            if fishery_count <= 8 or turn_count >= 100:
                #print('')
                perated_fish = (fishery_count + total_harvest) / float(total_harvest)
                #fish_to_players = int(fishery_count / 2)
                p1.payoff += int(p1_fish_count * perated_fish)
                p2.payoff +=  int(p2_fish_count * perated_fish)

                if  self.evaluation == True:
                    print('game ends... total harvest:',total_harvest, 'new_fishery_count: ',0,
                        'p1 chose: ',p1_fish_count, 'p2 chose: ', p2_fish_count,
                            'player1 final score: ',p1.payoff, 'comp final score: ',p2.payoff)

                state1 = [p2_fish_count,p1_fish_count,p2.payoff,p1.payoff,0]
                '''
                winning and losing in long games is fine short term has worse consequences 
                '''
                #winner calculation
                if p1.payoff > p2.payoff:
                    p1.update(state1, math.sqrt(turn_count))
                    self.win +=1
                    if self.evaluation == True:
                        print('player 1 wins')

                elif p1.payoff < p2.payoff:
                    

                    p1.update(state1, -1)
                    self.loss +=1
                    if self.evaluation == True:
                        print('player  2 wins')
                else:
                    p1.update(state1,1)
                    self.tie +=1
                    if self.evaluation == True:
                        print('tie')    

                #winner(p1,p2,state1,self.evaluation)

                break

            else:

                fishery_count_holder=  fishery_count

                p1.payoff += p1_fish_count
                p2.payoff +=  p2_fish_count

                fishery_count = fishery_count*2

                if fishery_count > initial_fishery:
                    fishery_count = initial_fishery


                state1 = [p2_fish_count,p1_fish_count,p2.payoff,p1.payoff,fishery_count]
                #print(state1)
                #p1.update(state1,p1.payoff-p2.payoff)
                #p1.update(state1,math.sqrt(turn_count))
                p1.update(state1,10)


                if  self.evaluation == True:
                    print('total harvest:',total_harvest,'fishery_count: ',fishery_count_holder,'new_fishery_count: ',fishery_count,
                        'player1 score: ',p1.payoff, 'comp_score: ',p2.payoff)

        if self.evaluation == False:
            self.game += 1
            self.turn_record.append(turn_count)
            self.report()

        if self.game == self._num_learning_rounds:
            print("Turning off learning!")
            self.player._learning = False
            self.win = 0
            self.loss = 0

    def reset_game(self):
        
        initial_fishery = 20
        #fishery_count = initial_fishery
        p1  = self.player
        #print(self.player)
        p1.payoff = 0 
        #dice_roll = random.randint(1,3)
        #if dice_roll == 1:
        #    p1 = team('greedy')
        #elif dice_roll == 2:
        #    p1 = team('con')
        #elif dice_roll == 3:
        #    p1 = team('dice')
            
        dice_roll = random.randint(1,2)
        if dice_roll == 1:
            p2 = team('greedy')
        elif dice_roll == 2:
            p2 = team('con')
        

        #print(p1.type,p2.type)
        return p1,p2,initial_fishery,initial_fishery
    
    def report(self):
        #turned off for plotting 9/18
        if self.game % self._num_learning_rounds == 0:

            avg_turn_count =  sum(self.turn_record) / float(len(self.turn_record))
            self.turn_record = []
            print('##############################################')
            print('#                 Final Score                #')
            print('##############################################')
            print('')
            print(str(self.game) +","  +str(self.win / (self.win + self.loss)),' ties: ', self.tie)
            print('')
            print('average game length: ',avg_turn_count)
            print('##############################################')
            
            #turning off this section for testing
            self.evaluation = True
            self.player._epsilon = 1.0
            print('#################### G1 ######################')
            self.play_game()
            print('#################### G2 ######################')
            self.play_game()
            print('#################### G3 ######################')
            self.play_game()
            self.player._epsilon = .9
            self.evaluation = False
            
            self.win = 0
            self.loss = 0
            self.tie = 0
            self.player.save_rl_model('models/{}_iteration_{}'.format(rl_model_name,self.game))
            
        elif self.game % self._report_every == 0:
            avg_turn_count =  sum(self.turn_record) / float(len(self.turn_record))
            self.turn_record = []
            print('##############################################')
            print('#                Updated Score               #')
            print('##############################################')
            print('')
            print(str(self.game) +","  +str(self.win / (self.win + self.loss)),' ties: ', self.tie)
            print('')
            print('average game length: ',avg_turn_count)
            print('##############################################')
            
            #turning off this section for testing
            self.evaluation = True
            self.player._epsilon = 1.0
            print('#################### G1 ######################')
            self.play_game()
            print('#################### G2 ######################')
            self.play_game()
            print('#################### G3 ######################')
            self.play_game()
            self.player._epsilon = .9
            self.evaluation = False
            
            self.win = 0
            self.loss = 0
            self.tie = 0
            self.player.save_rl_model('models/{}_iteration_{}'.format(rl_model_name,self.game))

        
#game1 = Tragedy()
#game1.play_game()