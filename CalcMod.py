import random, math

generator = {
    "Tempura":14,
    "Sashimi":14,
    "Dumpling":14,
    "Maki":15,
    "Nigiri_Salmon":10,
    "Nigiri_Squid":6,
    "Nigiri_Egg":6,
    "Pudding":10,
    "Wasabi":6
}

def GenerateDeck():
    final = []
    for name, number in generator.items():
        for x in range(number):
            final.append(name)
    random.shuffle(final)
    return final

nigiriPoints = {"Nigiri_Squid":3, "Nigiri_Salmon":2, "Nigiri_Egg":1}
sashimiPoints = [1, 3, 5, 10, 15]

def PointCalculation(hand):
    handInDic = {}
    points = 0
    for item in hand: #adds
        handInDic[item] = handInDic.get(item, 0) + 1
    
    points += (handInDic.get("Tempura", 0) // 2) * 5 #tempura calc

    points += (handInDic.get("Sashimi", 0) // 3) * 10 #sashimi calc

    wasabiToggle = 0 #nigiri + wasabi calc
    for food in hand:
        toAdd = 0
        if food == "Wasabi":
            wasabiToggle += 1
        elif "Nigiri" in food:
            toAdd += nigiriPoints[food]
            if wasabiToggle >= 1:
                toAdd *= 3
                wasabiToggle -= 1
        points += toAdd
    
    dumplings = handInDic.get("Dumpling", 0) #dumpling calc
    if dumplings > 5:
        points += 15        
    elif dumplings > 0:
        points += sashimiPoints[dumplings - 1]

    return points

Mod = {}
Mod["GenerateDeck"] = GenerateDeck
Mod["PointCalculation"] = PointCalculation