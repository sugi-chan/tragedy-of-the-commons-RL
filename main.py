from tragedy import TOC
from netlearner import DQNLearner
import time


def main():
    num_learning_rounds = 20000
    #print('dqn',DQNLearner())
    game = TOC(num_learning_rounds = num_learning_rounds, learner = DQNLearner()) #Deep Q Network Learner
    #game = Game(num_learning_rounds, Learner()) #Q learner
    number_of_test_rounds = 1000
    for k in range(0,num_learning_rounds + number_of_test_rounds):
        game.play_game()


    #df = game.p.get_optimal_strategy()
    #print(df)
    #df.to_csv('optimal_policy.csv')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))