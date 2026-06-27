#特定の文章を渡すとn-gramの図を出す
#Google Colaboratoryで使用

#描写関係
!apt install fonts-ipafont
from graphviz import Digraph
from IPython.display import Image, display
!mkdir images

#諸々
import pprint
from collections import defaultdict

col = ["きしゃのきしゃがきしゃできしゃする"]

#しかのこのこのここしたんたん
#きしゃのきしゃがきしゃできしゃする

#辞書型を宣言
freq = defaultdict(int)

for i in range(len(col)):
  Aegi = "^" + col[i] + "$"
  #print(Aegi)
  L = len(Aegi)
  L -= 1
  for j in range(L):
    b = Aegi[j:j+2]
    freq[b] += 1

#pprint.pprint(freq)
#「'^あ': 41,」が出力される

#バイグラムの確率 これだと全体
P = {}
N = sum(freq.values())
for(b,n) in freq.items():
  x = b[0]
  y = b[1]
  if not(x in P):
    P[x] = {}
  P[x][y] = n/N

#pprint.pprint(P)
#辞書P。'^': {'あ': 0.031037093111279335}などが出力。これは全体の％

#条件付き確率
Pc = {}
chars = P.keys()
for c in chars:
  Pc[c] = sum(P[c].values())

P0 ={}
for k in chars:
  P0[k] = {}
  for l in P[k]:
    P0[k][l] = P[k][l]/Pc[k]

#pprint.pprint(P0)

# 計算グラフの構造を定義
g = Digraph(f'G_test', directory='./images',format='png', graph_attr={'rankdir': 'LR'})
g.attr(dpi="1200")

# ノードの追加
for m in P0.keys():
  m = str(m)
  g.node('node'+ m, m)
g.node('node$', '$')

# エッジの追加
for n in P0.keys():
  for o in P0[n].keys():
    Kakuritu = str(round(P0[n][o]*100)) + "%"
    g.edge('node'+ str(n), 'node'+ str(o), label = Kakuritu)

# 計算グラフを画像として出力
display(Image(g.render()))