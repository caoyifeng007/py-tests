import csv
import re
import os
import sys
import argparse


def getExtension(file):
    return str(os.path.basename(file)).split('.')[-1]


def getBareName(file):
    return str(os.path.basename(file)).split('.')[0]


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
                    inputFiles.append(os.path.join(root,  file))
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

    eFile = open(file)
    eReader = csv.reader(eFile)

    for row in eReader:

        date = getBareName(file).split('_')[-1]
        exchange = str(list(row)[6]).split('_')[0]
        product = str(list(row)[6]).split('_')[-1]
        pathArr = [exchange, date, 'snap', product]

        contract = str(list(row)[7])

        if ("-P-" in contract) or ("-C-" in contract):
            pathArr.append('opt')
        else:
            pathArr.append('ftr')

        mo = contractReg.search(contract)
        item, n = mo.groups()
        pathArr.append(item)

        outputPath = os.path.sep.join(pathArr)
        outputName = '_'.join(pathArr)+'.csv'

        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        outputFile = open(
            os.path.join(outputPath, outputName),
            'w',
            newline='')
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(row)
        outputFile.close()

    eFile.close()
