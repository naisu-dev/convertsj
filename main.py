import ast
import re

def Give_H(text):
    output = {}
    if "/" in text:
        text = text.replace("/", "")
        output["slash"] = True
    else:
        output["slash"] = False
    if "give " in text:
        text = text.replace("give ", "")
    else:
        output = "No! Give!"
        return output
    output["selector"] = text[0:text.find(" ")]
    text = text.replace(output["selector"]+" ", "")
    if "{" in text and "}" in text:
        output["NBT"] = text[text.find("{"):text.rfind("}")+1]
        output["item"] = text.replace(output["NBT"], "")
    else:
        output = "No! NBT!"
        return output
    return output

def ConvertSJ(minecraft_json):
    test_pattern = re.compile(r'-*[0-9]+[bBslLfFdD]')
    r_json = test_pattern.findall(minecraft_json)
    for i in range(len(r_json)):
        minecraft_json = (minecraft_json.replace(r_json[i], (r_json[i])[:-1]))
    minecraft_json = minecraft_json.replace("\"", "").replace("'", "")
    pattern = re.compile(r'\b([a-zA-Z_]{2,})\b')
    standard_json = pattern.sub(r'"\1"', minecraft_json)
    return standard_json

MotoText = '/give @p diamond_axe{"BlockEntityTag": {"Lock": "2b4b"}}'
MotoText = MotoText.replace("minecraft:", "")

OutputList = []
KaisekiText = Give_H(MotoText)

nbt_data = ast.literal_eval(ConvertSJ(KaisekiText["NBT"]))

if "Damage" in nbt_data:
    OutputList.append("minecraft:damage="+ str(nbt_data["Damage"]))
if "CanPlaceOn" in nbt_data:
    OutputList.append("minecraft:can_place_on={blocks:"+ str(nbt_data["CanPlaceOn"])+ "}")
if "CanDestroy" in nbt_data:
    OutputList.append("minecraft:can_break={blocks:"+ str(nbt_data["CanDestroy"])+ "}")
if "RepairCost" in nbt_data:
    OutputList.append("minecraft:repair_cost="+ str(nbt_data["RepairCost"]))
if "Unbreakable" in nbt_data:
    if nbt_data["Unbreakable"] or nbt_data["Unbreakable"] == 1:
        OutputList.append("minecraft:unbreakable={}")
if "ChargedProjectiles" in nbt_data:
    OutputList.append("minecraft:charged_projectiles="+str(nbt_data["ChargedProjectiles"]))
if "display" in nbt_data:
    display = nbt_data["display"]
    if "color" in display:
        OutputList.append("minecraft:dyed_color="+ str(display["color"]))
    # if "Name" in display:
    #     OutputList.append("minecraft:custom_name"* str(display["Name"]))
    # if "Lore" in display:
    #     OutputList.append("minecraft:lore"* str(display["Lore"]))
if "StoredEnchantments" in nbt_data:
    enchant = {}
    for i in range(len(nbt_data["StoredEnchantments"])):
        enchant[nbt_data["StoredEnchantments"][i]["id"]] = nbt_data["StoredEnchantments"][i]["lvl"]
    OutputList.append("minecraft:stored_enchantments={levels:{"+ str(enchant).replace("{", "").replace("}", "")+ "}}")
if "Enchantments" in nbt_data:
    enchant = {}
    for i in range(len(nbt_data["Enchantments"])):
        enchant[nbt_data["Enchantments"][i]["id"]] = nbt_data["Enchantments"][i]["lvl"]
    OutputList.append("minecraft:enchantments={levels:{"+ str(enchant).replace("{", "").replace("}", "")+ "}}")
if "BlockEntityTag" in nbt_data:
    OutputList.append("minecraft:lock="+ str(nbt_data["BlockEntityTag"]["Lock"])+ "\"")

if KaisekiText["slash"]:
    OutputCommand = "/give "+ KaisekiText["selector"]+ " "+ KaisekiText["item"]+ str(OutputList).replace("'", "").replace('"', "")
else:
    OutputCommand = "give "+ KaisekiText["selector"]+ " "+ KaisekiText["item"]+ str(OutputList).replace("'", "").replace('"', "")

print(OutputCommand)

# {display:{Name:$(STR or LIST)}} → [minecraft:custom_name=$(STR or LIST)]
