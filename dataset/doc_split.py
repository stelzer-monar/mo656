import os
import sys
import json
import random

with open(sys.argv[1], encoding="utf8") as jsonfile:
        file = json.load(jsonfile)[0]["paragraphs"]
        for i in range(len(file)-1, 0, -1):
                j = random.randint(0, i + 1)
                file[i], file[j] = file[j], file[i]
        print(len(file))
        with open('train_ner.json', 'w') as f1:
            json.dump(file[:24], f1)
        with open('test_ner.json', 'w') as f2:
            json.dump(file[24:29], f2)
        with open('dev_ner.json', 'w') as f3:
            json.dump(file[29:], f3)