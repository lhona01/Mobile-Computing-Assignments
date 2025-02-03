import numpy as np
import random

class A1:
    def __init__(self):
        self.transition_matrix = None
        self.states = None

    def generate_markov_chain(self, state_list, sequence):
        """
        This method generates a transition matrix based on the provided state sequence.
        state_list: List of all possible states.
        sequence: Sequence of observed states (e.g., daily weather patterns).
        Returns: Transition matrix as a 2D numpy array.
        """
        # Initialize state indices and count matrix
        self.states = state_list
        state_indices = {state: idx for idx, state in enumerate(state_list)}
        num_states = len(state_list)
        count_matrix = np.zeros((num_states, num_states), dtype=int)

        # Fill count matrix by analyzing the state sequence
        for i in range(1, len(sequence)):
            prev_state = sequence[i - 1]
            curr_state = sequence[i]
            prev_idx = state_indices[prev_state]
            curr_idx = state_indices[curr_state]
            count_matrix[prev_idx][curr_idx] += 1

        # Convert counts to probabilities to form transition matrix
        row_sums = count_matrix.sum(axis=1, keepdims=True)
        self.transition_matrix = count_matrix / row_sums
        return self.transition_matrix

    def generate_samples(self, start_state, seed, length):
        """
        Generate a sequence of states based on the Markov chain.
        start_state: The first state in the generated sequence.
        seed: Random seed to ensure reproducibility.
        length: The length of the sequence (including start state).
        Returns: List of states in the generated sequence.
        """
        random.seed(seed)  # Set the random seed for reproducibility
        generated_sequence = [start_state]
        state_indices = {state: idx for idx, state in enumerate(self.states)}

        for _ in range(length):
            current_state = generated_sequence[-1]
            current_idx = state_indices[current_state]
            transition_probs = self.transition_matrix[current_idx]
            rand_value = random.random()

            # Find the next state based on the transition probabilities
            cumulative_prob = 0.0
            for idx, prob in enumerate(transition_probs):
                cumulative_prob += prob
                if rand_value < cumulative_prob:
                    generated_sequence.append(self.states[idx])
                    break

        #print(generated_sequence)
        return generated_sequence

    def stationary_distribution(self):
        """
        Compute the stationary distribution of the Markov chain.
        Returns: The stationary distribution as a 1D numpy array.
        """
        # Solve π * P = π for stationary distribution using eigenvector approach
        eigenvalues, eigenvectors = np.linalg.eig(self.transition_matrix.T)
        stationary_vec = eigenvectors[:, np.isclose(eigenvalues, 1)]
        
        # Normalize the stationary distribution
        stationary_vec = stationary_vec / stationary_vec.sum()
        print(stationary_vec.real.flatten())
        return stationary_vec.real.flatten()

potential_states =  ['Sunny', 'Cloudy', 'Rainy']
sequence_of_states = ['Sunny', 'Sunny', 'Rainy', 'Cloudy', 'Sunny', 'Rainy', 'Sunny', 'Sunny']

markov_chain_generator = A1()

apple = markov_chain_generator.generate_markov_chain(potential_states, sequence_of_states)
markov_chain_generator.generate_samples("Sunny", 24, 15)
markov_chain_generator.stationary_distribution()