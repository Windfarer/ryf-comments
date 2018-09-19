import biu
import csv

class RYFProject(biu.Project):
    def before(self):
        self.f = open("result.csv", 'w')
        self.csv_writer = csv.DictWriter(self.f, ["article_url", "user_name", "user_link", "content", "published_at"])
        self.csv_writer.writeheader()

    def after(self):
        self.csv_writer.writerows(self.results)
        self.f.close()

    def start_requests(self):
        self.results = []

        urls = """http://www.ruanyifeng.com/blog/essays/
http://www.ruanyifeng.com/blog/opinions/
http://www.ruanyifeng.com/blog/algorithm/
http://www.ruanyifeng.com/blog/developer/
http://www.ruanyifeng.com/blog/computer/
http://www.ruanyifeng.com/blog/javascript/
http://www.ruanyifeng.com/blog/startup/
http://www.ruanyifeng.com/blog/translations/
http://www.ruanyifeng.com/blog/sci-tech/
http://www.ruanyifeng.com/blog/literature/
http://www.ruanyifeng.com/blog/english/
http://www.ruanyifeng.com/blog/clipboard/
http://www.ruanyifeng.com/blog/notes/
http://www.ruanyifeng.com/blog/misc/
http://www.ruanyifeng.com/blog/mjos/
http://www.ruanyifeng.com/blog/usenet/""".split('\n')

        for url in urls:
            yield biu.Request(url, callback=self.parse_list)

    def parse_list(self, resp):
        urls = resp.xpath("/html/body/div/div/div[2]/div/div[1]/div/div/div/ul/li/a/@href").extract()
        for url in urls:
            yield biu.Request(url, callback=self.parse_detail)

    def parse_detail(self, resp):
        resp.encoding = 'utf-8'
        for comment in resp.xpath('//div[@class="comments-content"]/div[@class="comment"]'):
            name = comment.xpath("div[@class='inner']/div[@class='comment-header']/div[@class='asset-meta']/p/span[@class='byline']/span[@class='vcard author']/a/text()").get()
            if not name:
                name = comment.xpath("div[@class='inner']/div[@class='comment-header']/div[@class='asset-meta']/p/span[@class='byline']/span[@class='vcard author']/text()").get()
            user_link = comment.xpath("div[@class='inner']/div[@class='comment-header']/div[@class='asset-meta']/p/span[@class='byline']/span[@class='vcard author']/a/@href").get()
            content = comment.xpath("div[@class='inner']/div/p/text()").get()
            article_url = resp.url
            published_at = comment.xpath("div[@class='inner']/div[@class='comment-footer']/div[@class='comment-footer-inner']/p/abbr[@class='published']/text()").get()
            yield {
                "article_url": article_url,
                "user_name": name,
                "user_link": user_link,
                "published_at": published_at,
                "content": content,
            }

    def result_handler(self, rv):
        self.results.append(rv)

biu.run(RYFProject(concurrent=5, interval=0.5))