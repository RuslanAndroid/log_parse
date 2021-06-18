# coding=utf-8
import argparse
import re
import json

parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
args = parser.parse_args()


class Item:
    count = 0
    time = 0
    ip = ""
    url = ""
    post = 0
    get = 0


# я в общем не очень понял как работать с сортировкой в dict, и сделал массив обычный
dict_ip = []

with open(args.file) as file:
    idx = 0
    for line in file:
        # Перебор по массиву работает довольно долго, поставил лимит
        if idx == 10000:
            break
        ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)

        if ip_match is not None:
            ip = ip_match.group()
            element = [x for x in dict_ip if x.ip == ip]
            if element:
                element = element[0]
            else:
                element = Item()
                dict_ip.append(element)
            element.ip = ip
            method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line)
            if method is not None:
                method = method.groups()[0]
            element.count += 1

            # Я не знаю где там длительность, допустим что в конце строки
            time = int(re.match('.*?([0-9]+)$', line).group(1))
            if element.time < time:
                element.time = time
                url = re.search("(?P<url>https?://[^\s]+)", line)
                if url is not None:
                    element.url = url.group("url")

            if method == 'POST':
                element.post += 1
            if method == 'GET':
                element.get += 1

            idx += 1
print(json.dumps([ob.__dict__ for ob in dict_ip], indent=4))
print("Больше всего запросов: ")
most_callable = sorted(dict_ip, key=lambda x: x.count, reverse=True)[:3]
print([ob.ip + ' => ' + str(ob.count) for ob in most_callable])
print("Самые долгие запросы: ")
longest = sorted(dict_ip, key=lambda x: x.time, reverse=True)[:3]
print(json.dumps([ob.__dict__ for ob in longest], indent=4))
