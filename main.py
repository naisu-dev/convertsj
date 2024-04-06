import re
import ast

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

def ConvertSJ(text):
    find = re.sub(r"[^{}\[\]\":,'\s]+", r'"\g<0>"', text).replace('""', '"').replace("'\"", "\"").replace("\"'", "\"")
    return find

def nise_int(n_int):
    if re.match(r"[0-9]+.?[0-9]*[bBslLfFdD]", n_int) is not None:
        return float(n_int[:-1])
    else:
        if re.match(r"[0-9]+[bBslLfFdD]", n_int) is not None:
            return int(n_int[:-1])
        else:
            if "." in n_int:
                return float(n_int)
            else:
                return int(n_int)

command = '/give @p diamond{AttributeModifiers:[{AttributeName:"generic.scale",amount:-0.95,operation:0,UUID:[1,1,1,1],Slot:"offhand"}]}' ## ←←ここにコマンドを入力
data = Give_H(command)

OutputList = []

nbt_data = ast.literal_eval(ConvertSJ(data["NBT"]))

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
        enchant[nbt_data["StoredEnchantments"][i]["id"]] = nise_int(nbt_data["StoredEnchantments"][i]["lvl"])
    OutputList.append("minecraft:stored_enchantments={\"levels\":{"+ str(enchant).replace("'","\"").replace("{", "").replace("}", "")+ "}}")
if "Enchantments" in nbt_data:
    enchant = {}
    for i in range(len(nbt_data["Enchantments"])):
        enchant[nbt_data["Enchantments"][i]["id"]] = int(nbt_data["Enchantments"][i]["lvl"])
    OutputList.append("minecraft:enchantments={\"levels\":{"+ str(enchant).replace("'","\"").replace("{", "").replace("}", "")+ "}}")
if "BlockEntityTag" in nbt_data:
    if "Lock" in nbt_data["BlockEntityTag"]:
        OutputList.append("minecraft:lock=\""+ str(nbt_data["BlockEntityTag"]["Lock"]) + "\"")
if "AttributeModifiers" in nbt_data:
    kari_output = "minecraft:attribute_modifiers={\"modifiers\":[{\"type\":\""+nbt_data["AttributeModifiers"][0]["AttributeName"]+"\",\"amount\":"+str(nise_int(nbt_data["AttributeModifiers"][0]["amount"]))+",\"uuid\":"+str(nbt_data["AttributeModifiers"][0]["UUID"]).replace("'","")
    if "Name" in nbt_data["AttributeModifiers"][0]:
        kari_output = kari_output + ",\"name\":" + nbt_data["AttributeModifiers"][0]["Name"] + "\","
    else:
        kari_output = kari_output + ",\"name\":\"\","
    kari_output = kari_output + "\"operation\":"
    if nise_int(nbt_data["AttributeModifiers"][0]["operation"]) == 0:
        kari_output = kari_output + "\"add_value\""
    elif nise_int(nbt_data["AttributeModifiers"][0]["operation"]) == 1:
        kari_output = kari_output + "\"add_multiplied_base\""
    else:
        kari_output = kari_output + "\"add_multiplied_total\""
    if "Slot" in nbt_data["AttributeModifiers"][0]:
        kari_output = kari_output + ",\"slot\":\"" + nbt_data["AttributeModifiers"][0]["Slot"] + "\""
    else:
        kari_output = kari_output + ",\"slot\":\"any\""
    kari_output = kari_output + "}]}"
    OutputList.append(kari_output)

output_str = ""
for i in range(len(OutputList)):
    if i == 0:
        output_str = output_str+ ("[")
    output_str = output_str+ (OutputList[i])
    if len(OutputList) - 1 != i:
        output_str = output_str+(",")
    if len(OutputList) - 1 == i:
        output_str = output_str+("]")

if data["slash"]:
    OutputCommand = "/give "+ data["selector"]+ " "+ data["item"]+ output_str
else:
    OutputCommand = "give "+ data["selector"]+ " "+ data["item"]+ output_str

print(OutputCommand)
