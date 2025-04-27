import requests
from bs4 import BeautifulSoup
from pprint import pprint
from operator import itemgetter
import json


res = requests.get("https://news.ycombinator.com/news")
res_two = requests.get("https://news.ycombinator.com/news?p=2")
parsed_data = BeautifulSoup(res.text, "html.parser")
parsed_data_two = BeautifulSoup(res_two.text, "html.parser")

story_links = parsed_data.select(".titleline")
story_links_two = parsed_data.select(".titleline")

mega_links = story_links + story_links_two
# print(story_links[0].find("a")["href"])

score = parsed_data.select(".score")

subtext = parsed_data.select(".subtext")
subtext_two = parsed_data_two.select(".subtext")

mega_subtext = subtext + subtext_two
print(subtext[0].select(".score"))


def sort_stories_by_votes(data: list[dict]):
    sorted_data = sorted(data, key=itemgetter("votes"), reverse=True)
    return sorted_data


def create_custom_hn(links: list[str], subtext) -> list[str]:
    hn: list[str] = []

    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].find("a")["href"]
        vote = subtext[idx].select(".score")
        if len(vote):
            # print("_____", vote)
            points = int(vote[0].getText().replace(" points", ""))
            # print(points)
        # print(vote)
        if points > 100:
            hn.append({"title": title, "link": href, "votes": points})
        sorted_data = sort_stories_by_votes(hn)

    with open("data.json", "w") as file:
        json.dump(sorted_data, file, indent=4)
    return sorted_data


pprint(create_custom_hn(mega_links, mega_subtext))
