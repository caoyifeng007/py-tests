import os
import sqlite3
import argparse
import sys
import re
import datetime


def getExtension(file):
    return str(os.path.basename(file)).split('.')[-1]


def getBareName(file):
    return str(os.path.basename(file)).split('.')[0]


parser = argparse.ArgumentParser(description='品种路径写入脚本')
parser.add_argument(
    "-f", "--file",  help="specify a full path of sqlite3 db file. eg: a/b.db")
parser.add_argument(
    "-d", "--folder", help="specify a parent folder of time. eg: x => x/20220906/.")
args = parser.parse_args()


if args.file:
    if os.path.isfile(args.file):
        args.file = os.path.abspath(args.file)
    else:
        print(f"The {args.file} is not a file")
        sys.exit()
else:
    print("Please specify an file.")
    sys.exit()

if args.folder:
    if os.path.isdir(args.folder):
        if not os.path.isabs(args.folder):
            args.folder = os.path.abspath(args.folder)
    else:
        print(f"The {args.folder} is not a folder")
        sys.exit()
else:
    print("Please specify an folder.")
    sys.exit()

exchangeReg = '(DCE)'
timelvReg = '(snap|min|day)'
productReg = '(L1|L2|IDX|OTC)'
categoryReg = '(ftr|opt|arbi)'
itemReg = '(jd|p|pp|m)'
filenameReg = re.compile(
    '%s_\d{8}_%s_%s_%s_%s.csv$' % (exchangeReg, timelvReg, productReg, categoryReg, itemReg))

rawPaths = []
for root, subfolders, filenames in os.walk(args.folder, topdown=False):
    for file in filenames:
        rawPaths.append(os.path.join(root, file))

filePaths = []
for f in rawPaths:
    if filenameReg.search(f):
        filePaths.append(f)

valList = []
for f in filePaths:
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    vals = [dt, dt]
    vals += getBareName(f).split('_')
    vals.append(f)
    valList.append(tuple(vals))

# print(valList)

print("writing to db.")
conn = sqlite3.connect(args.file)
cur = conn.cursor()

# 考虑一下重复执行的情况
cur.executemany(
    "insert into goods_models (created_at, updated_at,exchange, date, time_level, product, category, item, path) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", valList)
conn.commit()
