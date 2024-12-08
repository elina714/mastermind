from sympy import symbols
from sympy.logic.boolalg import Or, And, Not
from sympy.logic.inference import satisfiable
import random
from itertools import permutations,combinations

class MasterMindSolver:
    def __init__(self, colors):
        """
                Initialize the MastermindSolver with a custom set of colors.

                Args:
                    colors (list): A list of color strings to use in the game.
        """
        self.COLORS = colors  # Use the custom color set
        self.length = len(colors)
        self.KB = []  # Knowledge Base
        self.init_propositions()
        self.init_knowledge_base()

    def init_propositions(self):
        """
        Define propositions dynamically as symbols based on the provided colors.
        """
        self.propositions = {}
        for i in range(1, self.length + 1):  # Positions are always 1-4
            for color in self.COLORS:
                self.propositions[f"P{i}_{color}"] = symbols(f"P{i}_{color}")
    def init_knowledge_base(self):
        ## One color per position (each position must have one color)
        one_color_per_position = [
            Or(*[self.propositions[f"P{i}_{color}"] for color in self.COLORS])  # Unpack the list with *
            for i in range(1, self.length + 1)
        ]

        ## One position per color (each color must be assigned to one position)
        one_position_per_color = [
            Or(*[self.propositions[f"P{i}_{color}"] for i in range(1, self.length + 1)])  # Unpack the list with *
            for color in self.COLORS
        ]
        ## No overlaps_per_position
        no_overlaps_per_position = [
            Not(And(self.propositions[f"P{i}_{color1}"], self.propositions[f"P{i}_{color2}"])) for i in range(1, self.length + 1) for color1 in self.COLORS
            for color2 in self.COLORS if color1 != color2
        ]
        # No overlaps_per_color
        no_overlaps_per_color = [
            Not(And(self.propositions[f"P{i}_{color}"], self.propositions[f"P{j}_{color}"])) for i in range(1, self.length + 1) for j in
            range(i + 1, self.length + 1) for color in self.COLORS
        ]
        self.KB = one_color_per_position + one_position_per_color + no_overlaps_per_position + no_overlaps_per_color

    def update_knowledge_base(self, guess, feedback):
        """
        Update the knowledge base with constraints based on the feedback.
        """
        new_constraints = []
        color_symbols = [self.propositions[f"P{i + 1}_{color}"] for i, color in enumerate(guess)]

        if feedback == 0:
            new_constraints.extend(Not(cs) for cs in color_symbols)
        elif feedback == 1:
            for i in range(self.length):
                constraint = [color_symbols[i]]
                constraint.extend(Not(color_symbols[j]) for j in range(4) if j != i)
                new_constraints.append(Or(*constraint))
        elif feedback == 2:
            constraints = []
            for true_positions in combinations(range(self.length), 2):
                condition = []
                for i in range(self.length):
                    if i in true_positions:
                        condition.append(color_symbols[i])
                    else:
                        condition.append(Not(color_symbols[i]))
                constraints.append(And(*condition))
            new_constraints.append(Or(*constraints))
        elif feedback == 3:
            for i in range(self.length):
                constraint = [Not(color_symbols[i])]
                constraint.extend(color_symbols[j] for j in range(self.length) if j != i)
                new_constraints.append(Or(*constraint))
        elif feedback == 4:
            new_constraints.append(And(*color_symbols))

        self.KB.extend(new_constraints)

    def refine_secret_space(self):
        """
        Refine the secret space based on the current KB.
        """
        combined_kb = And(*self.KB)
        solutions = satisfiable(combined_kb, all_models=True)
        possible_secrets = []

        for model in solutions:
            guess = []
            for i in range(1, 5):
                for color in self.COLORS:
                    if model[self.propositions[f"P{i}_{color}"]]:
                        guess.append(color)
                        break
            possible_secrets.append(tuple(guess))
        return possible_secrets

    def choose_best_guess(self, secret_space):
        """
        Choose the best guess from the refined secret space.
        """
        return random.choice(secret_space)

