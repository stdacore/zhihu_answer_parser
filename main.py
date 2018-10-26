import requests
import json
import time
import argparse
import warnings
warnings.simplefilter('ignore')

p = argparse.ArgumentParser()
p.add_argument("--qid", help="question id")
p.add_argument("--content-only", action='store_true')
args = p.parse_args()

# qid = "297717658"
qid = args.qid
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}
isEnd = False
count = 0

qurl = "https://www.zhihu.com/api/v4/questions/%s"%qid
r = requests.get(qurl, verify=False, headers=headers)
content = r.content.decode("utf-8")
data = json.loads(content)
fo = open(data['title']+".txt", "w")
qurl = qurl.replace("questions", "question")
qurl = qurl.replace("/api/v4", "")
created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['created'])) 
export_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
fo.write("%s\ncreated time: %s\nexport time: %s\n=============\n"%(qurl, created_time, export_time))

while not isEnd:
    url = "https://www.zhihu.com/api/v4/questions/%s/answers?include=content,voteup_count,comment_count&offset=%d&limit=20&sort_by=default"%(qid, count*20)
    r = requests.get(url, verify=False, headers=headers)
    content = r.content.decode("utf-8")
    data = json.loads(content)
    for i in range(len(data['data'])):
        answer = data['data'][i]
        vote = answer['voteup_count']
        content = answer['content']
        comment_count = answer['comment_count']
        updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(answer['updated_time'])) 
        answer_url = qurl + "/answer/" + answer['url'].split("answers/")[1]
        author_url = answer['author']['url'].replace("/api/v4", "")
        
        content = content.replace("<p>", "")
        content = content.replace("</p>", "\n")
        content = content.replace("<br>", "\n")
        content = content.replace("<b>", "")
        content = content.replace("</b>", "")
        
        fo.write("vote: %d\n\n%s\n\ncomment_count: %d\nupdated_time: %s\n%s\n%s\n----------\n"%(vote, content, comment_count, updated_time, answer_url, author_url))
        
    count += 1
    isEnd = data['paging']["is_end"]
fo.close()