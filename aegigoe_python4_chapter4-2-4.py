#文字数の分布（複数ある場合）
#Google Colaboratoryで使用

# 認証のためのコード
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

#諸々
import pprint
import collections
import statistics

#描写関係
!pip install japanize-matplotlib
from matplotlib import pyplot
import japanize_matplotlib

# スプレッドシートを開く（名前から）
#ここを変える
filename = "ぬきたし：文乃"
ss = gc.open(filename)

for sheetname in ["シート2","シート3"]:
  print("")
  print(sheetname)

  # シート名からシートを取得する
  ws = ss.worksheet(sheetname)

  # 指定列の値をリストで取得
  col = ws.col_values(8) #1から数える
  del col[0]

  a = len(col)
  c = collections.Counter(col)
  b = 0

  #pprint.pprint(c.most_common(10))
  for i in c.most_common(20):
    x = i[1]/a
    b += x
    print(i[0] + "：" + str(round(x*100,1))+ "％")
  print(str(round(b*100,1))+ "％")

  mojiList = []
  for i in col:
    mojiList.append(len(i))
  c = collections.Counter(mojiList)
  #pprint.pprint(c.most_common())
  a = len(mojiList)
  mojisuuList = []
  mojikosuuList = []
  for i in c.most_common():
    print(str(i[0]) + "文字：" + str(i[1]) + "個：" + str(round((i[1]/a)*100,1))+ "％")

  for i in sorted(c.items()):
    mojisuuList.append(i[0])
    mojikosuuList.append(round((i[1]/a)*100,1))

  print("平均：" + str(round(statistics.mean(mojiList),1)))
  print("中央値：" + str(round(statistics.median(mojiList),1)))
  print("最頻値：" + str(round(statistics.mode(mojiList),1)))
  print("標本標準偏差：" + str(round(statistics.stdev(mojiList),1)))

  pyplot.figure(dpi=1200)
  pyplot.bar(mojisuuList,mojikosuuList)
  pyplot.xlabel('文字数')
  pyplot.ylabel('割合（％）')
  if sheetname == "シート2":
    titlename = filename + "　あえぎ声・破瓜"
    #titlename = "あえぎ声・破瓜　文字数"
  elif sheetname == "シート3":
    titlename = filename + "　フェラ・キス・舐める"
    #titlename = "フェラ・キス・舐める　文字数"
  pyplot.title(titlename,y=-0.2)
  pyplot.figure(dpi=1200)
  pyplot.show()