"""This module is responsible for encopassing general utils functions"""
import string
import random


def generate_short_characters():
    """This function generates 3 random caracters"""
    characters = string.digits + string.ascii_letters
    picked_chars = random.choices(characters, k=3)
    return ("").join(picked_chars)
