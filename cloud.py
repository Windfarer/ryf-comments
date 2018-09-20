from wordcloud import WordCloud
import csv

wd = {}

with open("cut_result.csv") as f:
    reader = csv.DictReader(f)
    for i in reader:
        wd[i["word"]] = int(i["count"])

wordcloud = WordCloud(width=1024, height=1024, font_path="/Library/Fonts/华文黑体.ttf", color_func=lambda *args, **kwargs: (140,184,255)).generate_from_frequencies(wd)

image = wordcloud.to_image()
image.show()