#bi-gramの確率分布とジップの法則との比較
#Google Colaboratoryで使用

# 認証のためのコード
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

#描写関係
!pip install japanize-matplotlib
from matplotlib import pyplot
import japanize_matplotlib

#諸々
import pprint
from collections import defaultdict

# スプレッドシートを開く（名前から）
filename = "全体"
ss = gc.open(filename)

# シート名からシートを取得する
ws = ss.worksheet('シート1')

# 指定列の値をリストで取得
col = ws.col_values(8) #1から数える
del col[0]

#辞書型を宣言
freq = defaultdict(int)

for i in range(len(col)):
  Aegi = "^" + col[i] + "$"
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

#1次辞書に直して確率が大きい順に並び替え
ZentaiKakuritsuDic = {} #dic
for p in list(P):
  for q in list(P[p]):
    ZentaiKakuritsuDic[p+q] = P[p][q]
#pprint.pprint(ZentaiKakuritsuDic)

KoujyunList = sorted(ZentaiKakuritsuDic.items(), key=lambda x:x[1], reverse=True)

#確率分布を表示する
xlist = []
ylist = []
zlist = [] #累積確率
z = 0
j1list = []
j2list = [] #累積確率
j2 = 0
w1list = []
w2list = []
w2 = len(KoujyunList) * 0.2
w3list = []
for index,row in enumerate(KoujyunList):
  xlist.append(row[0])
  ylist.append(row[1])
  z = z + row[1]
  zlist.append(z)
  w1 = KoujyunList[0][1] / (index+1)
  j1list.append(w1)
  j2 = j2 + w1
  j2list.append(j2)
  if z <= 0.8:
    w1list.append(row[0])
  if w2 >= index+1:
    w2list.append(row[1])

pyplot.figure(dpi=1200)
pyplot.plot(xlist, ylist,linestyle="solid",label="bi-gramの確率分布")
pyplot.plot(xlist, j1list,linestyle="dashdot",label="ジップの法則")
pyplot.title("bi-gramの確率分布とジップの法則との比較",y=-0.2)
pyplot.xlabel('bi-gram')
pyplot.ylabel('確率')
pyplot.legend()
pyplot.show()
pyplot.figure(dpi=1200)
pyplot.plot(xlist, zlist,linestyle="solid",label="bi-gramの累積確率分布")
pyplot.plot(xlist, j2list,linestyle="dashdot",label="ジップの法則の累積")
pyplot.title("bi-gramの累積確率分布",y=-0.2)
pyplot.xlabel('bi-gram')
pyplot.ylabel('確率')
pyplot.legend()
pyplot.show()

w = len(w1list) / len(xlist)
print(len(w1list)) #線の数
print(len(xlist))
print(w) #全体の何割か
w2 = sum(w2list) #n割の場合何個か
print(len(w2list))
print(w2)