import argparse
import csv
import os
import re
import sys


def getExtension(f):
    return str(os.path.basename(f)).split('.')[-1]


def getBareName(f):
    return str(os.path.basename(f)).split('.')[0]


parser = argparse.ArgumentParser(description='行情云历史数据拆分脚本')
parser.add_argument("path", type=str, help="specify a full path. eg: a/b.csv")
parser.add_argument(
    "-d", "--folder", help="specify a folder.", action="store_true")
args = parser.parse_args()

inputFiles = []
if not args.path:
    print("Please specify a file or folder.")
    sys.exit()

if args.folder:
    if os.path.isdir(args.path):
        for root, _, fileNames in os.walk(args.path):
            for file in fileNames:
                if getExtension(file) == 'csv':
                    inputFiles.append(os.path.join(root, file))
    else:
        print(f"The {args.path} is not a folder")
        sys.exit()

else:
    if os.path.isfile(args.path):
        inputFiles.append(args.path)
    else:
        print(f"The {args.path} is not a file")
        sys.exit()

print("Input files:")
print(inputFiles)

# DCE 品种 才能用这个正则
contractReg = re.compile('([a-z]+)(\d{4})')
for file in inputFiles:

    eFile = open(file, encoding='utf-8')
    eReader = csv.reader(eFile)

    fileDict = dict()
    for row in eReader:

        contract = str(list(row)[7])
        date = getBareName(file).split('_')[-1]
        exchange = str(list(row)[6]).split('_')[0]
        product = str(list(row)[6]).split('_')[-1]
        pathArr = [exchange, date, 'day', product]

        if ("-P-" in contract) or ("-C-" in contract):
            pathArr.append('opt')
        else:
            pathArr.append('ftr')

        mo = contractReg.search(contract)
        item, n = mo.groups()
        pathArr.append(item)

        outputPath = os.path.abspath(os.path.sep.join(pathArr))
        outputName = '_'.join(pathArr) + '.csv'

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        writingFile = os.path.join(outputPath, outputName)
        if writingFile not in fileDict:
            fileDict[writingFile] = dict()

        fileDict[writingFile][contract] = row

    for f, cs in fileDict.items():
        outputFile = open(f, 'w', encoding='utf-8', newline='')
        outputWriter = csv.writer(outputFile)

        for r in cs.values():
            outputWriter.writerow(r)

        outputFile.close()

    eFile.close()
