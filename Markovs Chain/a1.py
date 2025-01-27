import numpy as np
import random

class A1:
    
    def __init__(self):
        self.potential_states = {}  # dictionary to map states to indices
        self.potential_states_1 = {} # dictionary to map indices to states
        self.transition_matrix = None # probability of transitioning to next state, given current state
        self.samples = None # newly generated samples given transition_matrix/probability

    #----------------------------------------------------------
    # generate_markov_chain(self, string[], string[])
    def generate_markov_chain(self, potential_states, sequence_of_states):
        """
        This method generates a transition matrix based on the provided state sequence.
        potential_states: List of all possible states.
        sequence_of_states: Sequence of observed states (e.g., daily weather patterns).
        Returns: Transition matrix as a 2D numpy array.
        """
        # store potential states and map them to indices
        for i in range(len(potential_states)):
            self.potential_states[potential_states[i]] = i  # potential_states["A"] = index_1
            self.potential_states_1[i] = potential_states[i] # potential_state_1[index_1] = "A"

        transition_count = np.zeros((len(potential_states), len(potential_states)))

        # count transitions in the sequence_of_states
        for i in range(len(sequence_of_states) - 1):
            row_index = self.potential_states[sequence_of_states[i]]
            col_index = self.potential_states[sequence_of_states[i + 1]]
            transition_count[row_index][col_index] += 1
        
        transition_matrix = np.zeros((len(potential_states), len(potential_states)))

        # calculate the transition matrix based on counts
        for row in range(len(transition_matrix)):
            row_sum = np.sum(transition_count[row])
            for col in range(len(transition_matrix[row])):
                transition_matrix[row][col] = transition_count[row][col] / row_sum

        #print("Transition Matrix:")
        #print(transition_matrix)

        self.transition_matrix = transition_matrix
        return transition_matrix
    
    #---------------------------------------------------------------------
    # generate_samples(self, string, int, int)
    def generate_samples(self, first_state, random_seed, length):
        """
        Generate a sequence of states based on the Markov chain.
        first_state: The first state in the generated sequence.
        seed: Random seed to ensure reproducibility.
        length: The length of the sequence (including start state).
        Returns: List of states in the generated sequence.
        """
        if not first_state in self.potential_states:
            return
        
        random.seed(random_seed)
        self.samples = np.empty(length + 1, dtype=object)  

        #                     |------------0.4---------0.6-----------1|
        # transition to state:     A             B           C 
        # example ^^
        # chances/percentage/likelihood of going to x state given you are in Y state
        state_change_divider = np.zeros((len(self.potential_states), len(self.potential_states)))

        for row in range(len(state_change_divider)):
            for col in range(len(state_change_divider[row])):
                if col == 0:
                    state_change_divider[row][col] = self.transition_matrix[row][col]
                else:
                    state_change_divider[row][col] = state_change_divider[row][col - 1] + self.transition_matrix[row][col]
        
        #print("state chage table")
        #print(state_change_divider)

        # generate sample
        for i in range(len(self.samples)):
            if i == 0:
                self.samples[i] = first_state
                continue

            random_number = random.uniform(0, 1) #allows decimals
            current_state_index = self.potential_states[self.samples[i - 1]]

            for j in range(len(state_change_divider[current_state_index])):
                if random_number < state_change_divider[current_state_index][j]:
                    self.samples[i] = self.potential_states_1[j]
                    break

        #print("sample")
        #print(self.samples)
        print(self.samples)
        return self.samples

    def stationary_distribution(self):
        """
        Compute the stationary distribution of the Markov chain.
        Returns: The stationary distribution as a 1D numpy array.
        """
        # Solve π * P = π for stationary distribution using eigenvector approach
        
        
        # Normalize the stationary distribution
        


# Testing the generate_markov_chain function

potential_states =  ['Sunny', 'Cloudy', 'Rainy']
sequence_of_states = ['Sunny', 'Sunny', 'Rainy', 'Cloudy', 'Sunny', 'Rainy', 'Sunny', 'Sunny']


# Create an instance of A1
markov_chain_generator = A1()

# generate_transiton matrix
markov_chain_generator.generate_markov_chain(potential_states, sequence_of_states)
markov_chain_generator.generate_samples("Cloudy", 24, 15)
