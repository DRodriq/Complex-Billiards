import config
import model

import random
import numpy as np


class Simulation:
    def __init__(self):

        self.dimensions = [model.genesis(), model.genesis()]  # 2d
        self.balls = [model.genesis() for _ in range(len(config.BALLS))]

        self.primes = self.dimensions + self.balls

        self.state = self.balls.copy()

        self.max_x = self.primes[0] ** (config.MAP_DIMENSION)
        self.max_y = self.primes[1] ** (config.MAP_DIMENSION)

        self.init_ball_positions()

        self.move_buffer = [1 for _ in range(len(self.balls))]

        self.rules = []


    def init_ball_positions(self):
        for i in range(len(self.state)):
            x = random.randint(1, config.MAP_DIMENSION)
            y = random.randint(1, config.MAP_DIMENSION)

            self.state[i] *= self.primes[0] ** (x)
            self.state[i] *= self.primes[1] ** (y)


    def get_ball_position(self, ball):
        x = 0
        y = 0
        n = ball
        while n % self.dimensions[0] == 0:
            n //= self.dimensions[0]
            x += 1
        while n % self.dimensions[1] == 0:
            n //= self.dimensions[1]
            y += 1
    
        return (x-1,y-1)
    
    
    def get_ball_from_event(self, event):
        for i in range(len(self.balls)):
            if event % self.balls[i] == 0:
                return self.balls[i]
        print(f"[DEBUG] No ball found for event {event}")
        raise ValueError("No ball found for event")
            

    def get_overlay(self):
        overlay = np.ones((config.MAP_DIMENSION, config.MAP_DIMENSION))
        for item in self.state:
            x,y = self.get_ball_position(item)
            for ball in self.balls:
                if item % ball == 0:
                    overlay[x][y] *= ball

        return overlay

    def step(self):
        for i in range(len(self.state)):
            if self.move_buffer[i] > 0:
                self.state[i] *= self.move_buffer[i]
            else:
                self.state[i] //= self.move_buffer[i]

            if self.state[i] % (self.max_x*self.dimensions[0]) == 0:
                self.state[i] //= self.max_x
                self.state[i] *= self.dimensions[0]
            if self.state[i] % (self.max_y*self.dimensions[1]) == 0:
                self.state[i] //= self.max_y
                self.state[i] *= self.dimensions[1]

            if self.state[i] % self.dimensions[0] != 0:
                self.state[i] *= self.max_x
            if self.state[i] % self.dimensions[1] != 0:
                self.state[i] *= self.max_y

        self.move_buffer = self.get_next_buffer()

    def perturb(self):
        invert = random.choice([True, False])
        ball_ind = random.randint(0, len(self.balls)-1)
        vec = random.choice(self.dimensions)
        if invert:
            vec = -vec
        self.move_buffer[ball_ind] *= vec

    def get_state_velocity(self):
        v = 1
        for vec in self.move_buffer:
            v *= abs(vec)
        return v if v != 1 else 0


    def create_rule(self):
        ball_1 = random.choice(self.balls)
        vec_1 = random.choice(self.dimensions)
        invert = random.choice([True, False])
        if invert:
            vec_1 = -vec_1

        ball_2 = random.choice(self.balls)
        while ball_1 == ball_2:
            ball_2 = random.choice(self.balls)
        vec_2 = random.choice(self.dimensions)
        invert = random.choice([True, False])
        if invert:
            vec_2 = -vec_2

        self.rules.append((ball_1*vec_1, ball_2*vec_2))


    def get_next_buffer(self):
        next_buffer = [1 for _ in range(len(self.balls))]
        events = [ball*move for ball, move in zip(self.balls, self.move_buffer)]
        causal_rules = [rule[0] for rule in self.rules]
        effect_rules = [rule[1] for rule in self.rules]

        for i in range(len(causal_rules)):
            if causal_rules[i] in events:
                effected_ball = self.get_ball_from_event(effect_rules[i])
                effect_vel = effect_rules[i] // effected_ball
                next_buffer[self.balls.index(effected_ball)] *= effect_vel

        return next_buffer
    

    def get_next_velocity(self):
        next_buffer = self.get_next_buffer()
        v = 1
        for vec in next_buffer:
            v *= abs(vec)
        return v if v != 1 else 0

def prime_factors(n):
    """Return the prime factors of the given number."""
    primes = model.PRIMES
    factors = []
    for prime in primes:
        if n % prime == 0:
            factors.append(prime)
    return factors

def prime_decomposition_matrix(matrix):
    """
    Return a matrix where each element is a list of the prime factors of the corresponding element in the input matrix.
    
    Parameters:
    matrix (np.ndarray): Input matrix.
    
    Returns:
    np.ndarray: Matrix of lists containing prime factors.
    """
    prime_matrix = np.empty(matrix.shape, dtype=object)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            prime_matrix[i, j] = prime_factors(int(matrix[i, j]))
    return prime_matrix

if __name__ == "__main__":
    sim = Simulation()

    # two dimensions and n balls
    assert sim.dimensions == [3,5]
    assert len(sim.balls) == len(config.BALLS)

    print(f"Dimensions: {sim.dimensions}")
    print(f"Balls: {sim.balls}")
    print(f"Primes: {sim.primes}")
    print(f"State: {sim.state}")

    # Test init ball positions are within bounds
    for ball in sim.state:
        pos = sim.get_ball_position(ball)
        assert pos[0] < config.MAP_DIMENSION
        assert pos[0] >= 0
        assert pos[1] < config.MAP_DIMENSION
        assert pos[1] >= 0

    # move buffer should be all ones and len should be equal to number of balls
    assert sim.move_buffer == [1 for _ in range(len(sim.balls))]

    # test state velocity
    sim.move_buffer[0] *= 3
    assert sim.get_state_velocity() == 3
    sim.move_buffer[0] *= 3
    assert sim.get_state_velocity() == 9
    sim.move_buffer[1] *= 5
    assert sim.get_state_velocity() == 45

    # test perturbation movements stays within bounds
    for i in range(1000):
        sim.perturb()
        sim.step()
        for item in sim.state:
            pos = sim.get_ball_position(item)
            try:
                assert pos[0] < config.MAP_DIMENSION
                assert pos[0] >= 0
                assert pos[1] < config.MAP_DIMENSION
                assert pos[1] >= 0
            except AssertionError:
                print(f"Error at iteration {i}")
                print(f"Ball: {item}")
                print(f"Position: {pos}")
                print(f"Dimensions: {sim.dimensions}")
                print(f"State: {sim.state}")
                print(f"Move buffer: {sim.move_buffer}")
                print(f"Max X: {sim.max_x}")
                print(f"Max Y: {sim.max_y}")
                quit()
    
    # test rule creation
    for i in range(100):
        sim.create_rule()
    assert len(sim.rules) == 100
    for rule in sim.rules:
        try:
            l_rule = rule[0]
            vel_1 = 3 if l_rule % 3 == 0 else 5
            assert l_rule % vel_1 == 0
            ball_1 = abs(l_rule // vel_1)
            assert ball_1 in sim.balls
        except AssertionError:
            print(f"Error at rule creation")
            print(f"Rule: {rule}")
            print(f"Testing left rule: {l_rule}")
            print(f"Balls: {sim.balls}")
            print(f"Velocities: {vel_1}")
            print(f"Ball 1: {ball_1}")
            quit()
        try:
            r_rule = rule[1]
            vel_2 = 3 if r_rule % 3 == 0 else 5
            assert r_rule % vel_2 == 0
            ball_2 = abs(r_rule // vel_2)
            assert ball_1 != ball_2
        except AssertionError:
            print(f"Error at rule creation")
            print(f"Rule: {rule}")
            print(f"Testing right rule: {r_rule}")
            print(f"Balls: {sim.balls}")
            print(f"Velocities: {vel_2}")
            print(f"Ball 1: {ball_2}")
            quit()

    sim.move_buffer = [1 for _ in range(len(sim.balls))]
    sim.move_buffer[0] *= 3
    sim.move_buffer[1] *= 5

    sim.rules = []
    sim.rules.append((11*5,19*-3))
    next_buff = sim.get_next_buffer()
    assert next_buff[4] == (-3)

    # test rule application
    sim.rules = []
    for i in range(10):
        sim.create_rule()
    

