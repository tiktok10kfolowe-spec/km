import random

HOUSE_EDGE = 0.20  # 20% profit for the house

def roll_dice(bet):
    result = random.randint(1, 6)
    if result >= 4:  # player wins on 4,5,6
        win_amount = bet * 2 * (1 - HOUSE_EDGE)
    else:
        win_amount = 0
    return result, win_amount

def flip_coin(bet, player_choice):
    """
    Flip a coin: Heads or Tails.
    Player chooses 'Heads' or 'Tails'.
    If player guesses correctly, they win double minus house edge.
    """
    player_choice = player_choice.capitalize()  # normalize input
    if player_choice not in ["Heads", "Tails"]:
        return None, 0  # invalid choice, no win

    outcome = random.choice(["Heads", "Tails"])
    if player_choice == outcome:
        win_amount = bet * 2 * (1 - HOUSE_EDGE)  # player wins
    else:
        win_amount = 0  # player loses
    return outcome, win_amount