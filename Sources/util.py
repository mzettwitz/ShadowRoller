import numpy as np
import re
from collections import Counter


ini_storage = []

# roll x-times y
def roll_generic(x, y):
    return np.ndarray.astype(np.ceil(np.random.default_rng().random(x) * y), int)


def validate(message):
    message_strip = message.content.strip()
    if re.fullmatch('^(/?[0-9]+)([[dD][0-9]+]?)?$', message_strip) is not None:
        count, dice = process_roll(message_strip)
        return True, send_roll(count, dice, message)
    if re.match('ini[0-9]+\+[0-9]+', message_strip):
        base, count = process_ini(message_strip)
        return True, send_ini(base, count, message)
    if message_strip == "inishow":
        return True, send_ini_show(message)
    if message_strip == "iniclear":
        return True, send_ini_clear(message)
    elif re.match('[-]+help', message_strip) is not None:
        return True, send_help(message)
    else:
        return False, message.author.mention + "";


def process_ini(message):
    message = message.replace("ini", '')
    message = message.split('+')
    base = int(message[0])
    count = int(message[1])
    return base, count


def process_roll(message):
    # XDY
    if re.fullmatch('.*[dD].*', message) is not None:
        message = message.replace('/', '')
        message = re.split('[dD]', message)
        count = int(message[0])
        dice = int(message[1])
        return count, dice
    # 1DX
    elif message.startswith('/'):
        dice = int(message.replace('/', ''))
        return 1, dice
    # XD6
    else:
        count = int(message)
        return count, 6


def send_roll(count, dice, message):
    if count > 0:
        rolls = roll_generic(count, dice)
        # todo: replace by nice regex
        if message.content.find('d') != -1 or message.content.find('D') != -1 or message.content.find('/') != -1:
            return evaluate_roll(x_d_y, rolls, dice, message)
        else:
            return evaluate_roll(classic, rolls, count, message)


def send_ini(base, count, message):
    rolls = roll_generic(count, 6)
    ini_sum = sum(rolls) + base
    ini_storage.append((message.author, ini_sum))
    return message.author.mention + " Base: " + str(base) + " + " + str(rolls) + " = " + str(ini_sum)


def send_ini_show(message):
    ini_storage.sort(key=lambda ini: ini[1], reverse=True)
    ini_table = " ====Ini table====\n"
    for player in ini_storage:
        ini_passes = 1
        if player[1] > 30:
            ini_passes = 4
        if player[1] > 20:
            ini_passes = 3
        elif player[1] > 10:
            ini_passes = 2
        ini_table += player[0].mention + " " + str(player[1]) + " => " + str(ini_passes) + " Ini passes \n"
    return message.author.mention + ini_table


def send_ini_clear(message):
    ini_storage.clear()
    return message.author.mention + " Initiative cleared."


def send_help(msg):
    help_msg = "𝑥  \t \t \twhere 𝑥 ∈ ℕ, e.g., 6. Rolls 𝑥 D6 dices. \n" \
                "     \t \t \tRolls are evaluated with Shadowrun 4 rules.\n"
    help_msg += "/𝑦\t \t \twhere 𝑦 ∈ ℕ, e.g., /6. Rolls 1 D𝑦 dice.\n"
    help_msg += "𝑥d𝑦  \t \twhere 𝑥,𝑦 ∈ ℕ, e.g., 5d10. Rolls 𝑥 D𝑦 dices.\n"
    help_msg += "ini𝑥+𝑦  \t where 𝑥,𝑦 ∈ ℕ, e.g., ini7+2. Adds base Initiative 𝑥 to 𝑦 D6 dices.\n" \
                "     \t \t \tPlayers and Initiative values are stored and can be shown with \/inishow.\n"
    help_msg += "inishow \tprints the stored Initiative table and the resulting Initiative passes.\n"
    help_msg += "iniclear  \tclears the stored Initiative table."
    return msg.author.mention + "\nHow to use: \n" + help_msg


def evaluate_roll(func, rolls, dice, msg):
    # Shadowrun system
    distr = [Counter(rolls).get(x) for x in range(1, 7)]

    for i in range(6):
        distr[i] = 0 if distr[i] is None else distr[i]

    hits = distr[4] + distr[5]
    fails = distr[0]

    # Generic return
    return func(rolls, dice, hits, fails, msg)


def classic(rolls, dice, hits, fails, msg):
    count = len(rolls)
    rolls.sort()
    if fails >= np.ceil(count / 2.0):
        if hits == 0:
            return msg.author.mention + " " + str(rolls) + ' CRITICAL GLITCH with ' + str(fails) + ' fails!'
        else:
            return msg.author.mention + " " + str(rolls) + ' GLITCH with: ' + str(fails) + ' fails and ' + str(hits) + ' hits!'
    else:
        return msg.author.mention + " " + str(rolls) + ' with ' + str(hits) + ' hits!'


def x_d_y(rolls, dice, hits, fails, msg):
    return msg.author.mention + " " + str(len(rolls)) + "D" + str(dice) + ": " + str(rolls)


