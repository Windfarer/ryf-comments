import jieba
import csv
import jieba.analyse
import unicodedata

stopwords = set()

for i in open("stopwords.txt").read().split('\n'):
    stopwords.add(unicodedata.normalize('NFC', i))

def main():
    words = {}

    # count = 0
    with open("result.csv") as f:
        reader = csv.DictReader(f)
        for i in reader:
            # count += 1
            # if count > 100:
            #     break
            content = i["content"]
            for w in jieba.cut(content, cut_all=False):
                w = unicodedata.normalize('NFC', w)
                w = w.strip()
                if not w:
                    continue
                if w in stopwords:
                    continue
                if w not in words:
                    words[w] = 1
                    print(w)
                else:
                    words[w] += 1
    with open('cut_result.csv', 'w') as cf:
        writer = csv.DictWriter(cf, ["word", "count"])
        writer.writeheader()
        for w in sorted(words, key=words.get, reverse=True):
            writer.writerow({"word": w, "count": words[w]})
    # print(jieba.analyse.extract_tags(content, topK=10))

if __name__ == '__main__':
    main()