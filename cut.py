import jieba
import csv
import jieba.analyse
jieba.analyse.set_stop_words("stopwords.txt")

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