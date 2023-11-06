import json
import random
import os


def micro_scramble(json_str: str, seed: int):
    
    # Use the seed for reproducibility
    random.seed(seed)
    
    # Scrambling operations
    def missing_comma(s):
        commas = [i for i, char in enumerate(s) if char == ',']
        if commas:
            return s[:commas[-1]] + s[commas[-1]+1:]
        return s

    def missing_bracket(s):
        brackets = [i for i, char in enumerate(s) if char in ['{', '[', '}', ']']]
        if brackets:
            return s[:brackets[-1]] + s[brackets[-1]+1:]
        return s

    def extra_comma(s):
        positions = [i for i, char in enumerate(s) if char in ['{', '[', ':']]
        if positions:
            pos = random.choice(positions)
            return s[:pos] + ',' + s[pos:]
        return s

    def extra_bracket(s):
        bracket_types = ['{', '[', '}', ']']
        positions = [i for i, char in enumerate(s) if char in bracket_types]
        if positions:
            pos = random.choice(positions)
            bracket = random.choice(bracket_types)
            return s[:pos] + bracket + s[pos:]
        return s
    
    operations = [missing_comma, missing_bracket, extra_comma, extra_bracket]
    
    num_edits = random.randint(1, 3)
    for _ in range(num_edits):
        # Randomly choose an operation and apply it
        json_str = random.choice(operations)(json_str)
    
    return json_str


examples = []

print('reading files')
examples_dir = os.path.join(os.path.dirname(__file__), "examples")
for examples_path in os.listdir(examples_dir):
    examples_path = os.path.join(examples_dir, examples_path)
    with open(examples_path) as f:
        examples += json.load(f)

print(len(examples))

scrambled_jsons = []
correct_jsons = []

print('generating scrabled jsons')
for seed, example in enumerate(examples):
    correct_json = json.dumps(example)
    scrambled_json = micro_scramble(correct_json, seed)

    scrambled_jsons += [scrambled_json]
    correct_jsons += [correct_json]


print('Scrambled JSONs:')
print(len(scrambled_jsons))
