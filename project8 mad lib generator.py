import random

stories = [
    "I found a {adjective} {animal} that loves {verb} in {place}.",
    "In {place}, a {animal} was {verb} in a very {adjective} way."
]

adjective = input("Enter the adjective here: ")
animal = input("Enter the name of the animal here: ")
verb = input("Enter the verb here: ")
place = input("Enter the place here: ")

story = random.choice(stories)

print(story.format(
    adjective=adjective,
    animal=animal,
    verb=verb,
    place=place
))