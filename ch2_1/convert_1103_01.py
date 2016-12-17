# -*- coding: utf-8 -*-
f1 = open('data1_utf8.dat', 'r')  # data1.dat を入力のためにopen
f2 = open('data2.dat', 'w')  # data2.dat を出力のためにopen
content = f1.read()  # ファイル全てをstrタイプで読み込み
contents = content.split(';')  # セミコロンで区切る
for kk in contents:
    k1, k2 = kk.split(',')  # カンマを区切りとしてリストに分割
    k1, k2 = int(k1), float(k2)  # 各要素を数値に変換
    f2.write(str(k1) + ' ' + str(k2**2) + '\n')  # 2乗値と空白，改行コードを書き込み
f1.close()  # data1.dat をクローズ
f2.close()  # data2.dat をクローズ
