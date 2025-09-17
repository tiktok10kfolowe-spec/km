import telebot
from balance import get_balance, update_balance, set_balance
from games import roll_dice, flip_coin
from stay_alive import keep_alive

TOKEN = "8241686611:AAFBQuiEpE76J4_aPpHj9gBwS98luOKd2uE"
bot = telebot.TeleBot(TOKEN)

OWNER_ID = 6460152970
update_balance(OWNER_ID, 0)  # ensure house exists

# Start Flask keep-alive server
keep_alive()

# ----------------- Helper -----------------
def is_owner(message):
    return message.from_user.id == OWNER_ID

# ----------------- Player Commands -----------------
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    welcome_text = (
        f"🎰 Welcome {message.from_user.first_name}!\n"
        f"ID: {user_id}\nBalance: ${get_balance(user_id):.2f}\n"
        "Commands:\n/balance\n/roll <amount>\n/coin <amount> <Heads/Tails>"
    )
    if is_owner(message):
        welcome_text += "\nOwner Commands:\n/add <id> <amount>\n/remove <id> <amount>\n/set <id> <amount>"
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=["balance"])
def balance_cmd(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f"💰 Balance: ${get_balance(user_id):.2f}")

@bot.message_handler(commands=["roll"])
def roll_cmd(message):
    user_id = message.from_user.id
    try:
        bet = float(message.text.split()[1])
    except:
        bot.reply_to(message, "⚠️ Usage: /roll <amount>")
        return
    if bet <= 0 or bet > get_balance(user_id):
        bot.reply_to(message, "⚠️ Invalid bet amount")
        return
    result, win = roll_dice(bet)
    net = win - bet
    update_balance(user_id, net)
    update_balance(OWNER_ID, -net)
    bot.send_message(
        message.chat.id,
        f"🎲 Rolled {result}\nBet: ${bet:.2f}\n{'Won' if net>0 else 'Lost'} ${abs(net):.2f}\n"
        f"Balance: ${get_balance(user_id):.2f}"
    )

@bot.message_handler(commands=["coin"])
def coin_cmd(message):
    user_id = message.from_user.id
    try:
        args = message.text.split()
        bet = float(args[1])
        choice = args[2].capitalize()  # Heads or Tails
    except:
        bot.reply_to(message, "⚠️ Usage: /coin <amount> <Heads/Tails>")
        return
    if bet <= 0 or bet > get_balance(user_id):
        bot.reply_to(message, "⚠️ Invalid bet amount")
        return
    outcome, win = flip_coin(bet, choice)
    if outcome is None:
        bot.reply_to(message, "⚠️ Invalid choice, type 'Heads' or 'Tails'")
        return
    net = win - bet
    update_balance(user_id, net)
    update_balance(OWNER_ID, -net)
    bot.send_message(
        message.chat.id,
        f"🪙 Coin: {outcome}\nYour choice: {choice}\nBet: ${bet:.2f}\n"
        f"{'Won' if net>0 else 'Lost'} ${abs(net):.2f}\nBalance: ${get_balance(user_id):.2f}"
    )

# ----------------- Owner Commands -----------------
@bot.message_handler(commands=["add"])
def add_cmd(message):
    if not is_owner(message):
        return
    try:
        user_id = int(message.text.split()[1])
        amount = float(message.text.split()[2])
    except:
        bot.reply_to(message, "⚠️ Usage: /add <id> <amount>")
        return
    new_bal = update_balance(user_id, amount)
    bot.send_message(
        message.chat.id,
        f"✅ Added ${amount:.2f} to {user_id}. New balance: ${new_bal:.2f}"
    )

@bot.message_handler(commands=["remove"])
def remove_cmd(message):
    if not is_owner(message):
        return
    try:
        user_id = int(message.text.split()[1])
        amount = float(message.text.split()[2])
    except:
        bot.reply_to(message, "⚠️ Usage: /remove <id> <amount>")
        return
    new_bal = update_balance(user_id, -amount)
    bot.send_message(
        message.chat.id,
        f"✅ Removed ${amount:.2f} from {user_id}. New balance: ${new_bal:.2f}"
    )@bot.message_handler(commands=["set"])
def set_cmd(message):
    if not is_owner(message):return
    try:
        user_id = int(message.text.split()[1])
        amount = float(message.text.split()[2])
    except:
        bot.reply_to(message, "⚠️ Usage: /set <id> <amount>")
        return
    new_bal = set_balance(user_id, amount)
    bot.send_message(
        message.chat.id,
        f"✅ Set balance of {user_id} to ${new_bal:.2f}"
    )

# ----------------- Run Bot -----------------
print("Bot running...")
bot.infinity_polling()