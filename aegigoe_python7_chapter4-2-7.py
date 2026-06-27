# 音声記号の図示
#Visual Studio Codeで使用

# Gprahvizのダウンロード
# pip install graphviz

# 描写関係
from graphviz import Digraph

# データ
data_list = [
    ["i", "ç"],
    ["u", "ɸ"],
    ["e", "h"],
    ["k", "h"],
    ["g", "h"],
    ["k", "ç"],
    ["k", "ɡ"],
    ["s", "ɕ"],
    ["s", "ç"],
    ["ɕ", "ç"],
    ["dʑ", "ç"],
    ["s", "ɸ"],
    ["z", "ts"],
    ["s", "h"],
    ["t", "h"],
    ["d", "ɾ"],
    ["d", "ɾʲ"],
    ["tɕ", "dʑ"],
    ["tɕ", "ç"],
    ["d", "ɸ"],
    ["d", "h"],
    ["t", "ɾ"],
    ["n", "nʲ"],
    ["h", "ç"],
    ["m", "ç"],
    ["j", "ç"],
    ["ɾ", "ɾʲ"],
    ["ɾ", "e"],
]

# 計算グラフの構造を定義
dot = Digraph(directory="./images", format="png")
dot.attr(
    splines="spline",
    fontsize="25",
    dpi="1200",
)

# ノードの追加
for m in data_list:
    dot.node("node" + m[0], m[0])
    dot.node("node" + m[1], m[1])

# エッジの追加
for n in data_list:
    dot.edge("node" + n[0], "node" + n[1])

# 計算グラフを画像として出力
path = dot.render()
print(path)