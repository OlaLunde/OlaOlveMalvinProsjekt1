import random
import tkinter as tk


COLOURS = ["red", "blue", "green", "yellow", "black", "white"]
secret_code = [random.choice(COLOURS) for _ in range(4)]
max_guesses = 10


class Mastermind:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")
        
        self.guess_count = 0
        self.guess = []
        self.chosen_colours = []
        

        
    