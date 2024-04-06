# みんなへ
## 使い方
MotoTextに前までのバージョンのコマンドをいれる
printされる
## 対応してるコンポーネント
- Damage
- CanPlaceOn
- CanDestroy
- RepairCost
- Unbreakble
- ChargedProjectiles
- display(color only)
- StoredEnchantments
- Enchantments
- AttributeModifiers ←←←new まじで頑張ったから褒めて！

これから追加していく予定

# 開発者へ
## 関数
### Give_H
giveコマンドの解析前のバージョンのコマンドを入力するとdictで返される<br>
- NBT str NBT
- slash bool スラッシュが先頭にあるかないか
- selector str セレクター
- item str アイテム
### ConvertSJ
NBTをわかりやすくする。strで返される<br>
## 変数
### MotoText
入力
### OutputList
NBTのリスト（仮）
### KaisekiText
入力をGive_Hに通したもの
### nbt_data
astでNBTをdictに変形したもの
### OutputCommand
出力

# 連絡
twitter @naisu_dayo
