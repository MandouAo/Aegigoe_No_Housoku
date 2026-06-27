#あえぎ声とフェラの図を出力する。3枚同時に出す
#Google Colaboratoryで使用

# 認証のためのコード
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

#描写関係
!apt install fonts-ipafont
from graphviz import Digraph
from IPython.display import Image, display
!mkdir images

#諸々
import pprint
from collections import defaultdict
import copy

#ここを変更する
filename = "全体"

site_number = "シート1"
titlemei = "：全体：累積"

#site_number = "シート2"
#titlemei = "：あえぎ声・破瓜：累積"

#site_number = "シート3"
#titlemei = "：フェラ・キス・舐める：累積"

#site_number = "シート4"
#titlemei = "：笑い声：累積"
#titlemei = "：男子：累積"

# スプレッドシートを開く（名前から）
ss = gc.open(filename)

# シート名からシートを取得する
ws = ss.worksheet(site_number)

# 指定列の値をリストで取得
col = ws.col_values(8) #1から数える
del col[0]

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

# 集計ルールにより削除
if '……' in freq:
  del freq['……']
if 'ーー' in freq:
  del freq['ーー']
if '～～' in freq:
  del freq['～～']

#pprint.pprint(freq)

#バイグラムの確率
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

#1次辞書に直して確率が大きい順に並び替え
ZentaiKakuritsuDic = {} #dic
for p in list(P):
  for q in list(P[p]):
    ZentaiKakuritsuDic[p+q] = P[p][q]
#pprint.pprint(ZentaiKakuritsuDic)
KoujyunList = sorted(ZentaiKakuritsuDic.items(), key=lambda x:x[1], reverse=True) #list

#累積確率がN割以上になったら削除
z = 0
List80 = copy.deepcopy(P0)
List85 = copy.deepcopy(P0)
List90 = copy.deepcopy(P0)
for row in KoujyunList:
  z = z + row[1]
  p = row[0][:1]
  q = row[0][1:]
  if z > 0.8:
    del List80[p][q]
  if z > 0.85:
    del List85[p][q]
  if z > 0.9:
    del List90[p][q]

#子が全部削除されたら削除
for p in list(List80):
  if not any(List80[p]):
    del List80[p]
for p in list(List85):
  if not any(List85[p]):
    del List85[p]
for p in list(List90):
  if not any(List90[p]):
    del List90[p]

#3回やる
title = filename + titlemei + "80%"
# 計算グラフの構造を定義
dot = Digraph(f'G_test', directory='./images',format='png', graph_attr={'rankdir': 'LR'})
dot.attr(label=title,labeljust="c",labelloc="b",splines="spline",fontsize="25",dpi="1200")

# ノードの追加
for m in List80.keys():
  m = str(m)
  dot.node('node'+ m, m)
  for s in List80[m].keys():
    s = str(s)
    dot.node('node'+ s, s)

# エッジの追加
for n in List80.keys():
  for o in List80[n].keys():
    Kakuritu = str(round(List80[n][o]*100,1)) + "%"
    dot.edge('node'+ str(n), 'node'+ str(o), label = Kakuritu)

# 計算グラフを画像として出力
display(Image(dot.render()))

title2 = filename + titlemei + "85%"
# 計算グラフの構造を定義
dot2 = Digraph(f'G_test', directory='./images',format='png', graph_attr={'rankdir': 'LR'})
dot2.attr(label=title2,labeljust="c",labelloc="b",splines="spline",fontsize="25",dpi="1200")

# ノードの追加
for m in List85.keys():
  m = str(m)
  dot2.node('node'+ m, m)
  for s in List85[m].keys():
    s = str(s)
    dot2.node('node'+ s, s)

# エッジの追加
for n in List85.keys():
  for o in List85[n].keys():
    Kakuritu2 = str(round(List85[n][o]*100,1)) + "%"
    dot2.edge('node'+ str(n), 'node'+ str(o), label = Kakuritu2)

# 計算グラフを画像として出力
display(Image(dot2.render()))

title3 = filename + titlemei + "90%"
# 計算グラフの構造を定義
dot3 = Digraph(f'G_test', directory='./images',format='png', graph_attr={'rankdir': 'LR'})
dot3.attr(label=title3,labeljust="c",labelloc="b",splines="spline",fontsize="25",dpi="1200")

# ノードの追加
for m in List90.keys():
  m = str(m)
  dot3.node('node'+ m, m)
  for s in List90[m].keys():
    s = str(s)
    dot3.node('node'+ s, s)

# エッジの追加
for n in List90.keys():
  for o in List90[n].keys():
    Kakuritu3 = str(round(List90[n][o]*100,1)) + "%"
    dot3.edge('node'+ str(n), 'node'+ str(o), label = Kakuritu3)

# 計算グラフを画像として出力
display(Image(dot3.render()))