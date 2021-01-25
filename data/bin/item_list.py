
    # Zero: item ID
    # First: item name
    # Second: Item classification, and the type
    # Third: REQUIRED LEVEL NEEDED TO USE IT
    # ----ALWAYS INDEX NUMBER 4------
    # Fourth: The specific status of it.

    # Equipment specific statuses go like this:
    # [Attack,Defense,Health,Speed]

    #  could include:
    #    Critical Strike?


    # Fifth: [Buy Price, Sell Price]
    # Sixth: Description of item

class AllItems():
    def __init__(self):
        self.item_list =[
        [0, "Small Health Potion",["Consumable", "Health"], [1,"Potion"], 10,  [10,5], ["This restores 10 HP to a character."]],
        [1, "Large Health Potion",["Consumable", "Health"], [1,"Potion"], 50,  [25,10],["This restores 50 HP to a character."]],
        [2, "Super Health Potion",["Consumable", "Health"], [1,"Potion"], 100, [50,20],["This restores 100 HP to a character."]],

        [3, "Small Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 10,  [10,5], ["This restores 10 MP to a character."]],
        [4, "Large Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 50,  [25,10], ["This restores 50 MP to a character."]],
        [5, "Super Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 100, [50,20], ["This restores 100 MP to a character."]],

        [6, "Small Dagger"    ,["Equipment","Weapon"], [1,"Dagger"], [1,-2,0,3],  [1,8],  ["A small, yet effective weapon."]],
        [7, "Bronze Sword"    ,["Equipment","Weapon"], [3,"Sword"], [2,1,0,2],  [50,25], ["What squires swing at eachother trying to be knights."]],
        [8, "Iron Sword"      ,["Equipment","Weapon"], [5,"Sword"], [3,1,0,1],  [100,50],["Brave and noble nights wield these."]],

        [9,  "Cloth Hat"      ,["Equipment","Helm"], [1, "Cloth"], [0,1,2,3],  [15,8],["Farmhands use these to protect from the sun, and you wanna protect from a sword."]],
        [10, "Bronze Helm"    ,["Equipment","Helm"], [3, "Plate"], [0,2,3,2],  [50,25],["Made with the finest bronze the local towns have to offer."]],
        [11, "Iron Helm"      ,["Equipment","Helm"], [5, "Plate"],[0,3,5,1],  [75,25], ["Many of these are scattered in deserts."]],


        [12, "Cloth Armor"    ,["Equipment","Chest"],[1, "Cloth"],[0,1,2,2], [15,8], ["Taken from a practice dummy, this hopefully will keep you alive."]],
        [13, "Bronze Armor"   ,["Equipment","Chest"],[3, "Plate"],[0,2,3,1], [50,25],["Guards wear it, and now you!"]],
        [14, "Iron Armor"     ,["Equipment","Chest"],[5, "Plate"],[0,3,5,1], [75,25], ["You can take an arrow to the gut with this and make it away."]]

        ]