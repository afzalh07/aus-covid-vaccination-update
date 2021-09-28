from bs4 import BeautifulSoup
import requests

url = "https://covidlive.com.au/"
# retrieve the html using the request library
html = requests.get(url)

# creating an object of modified html document
soup = BeautifulSoup(html.text, 'html.parser')


def first_dose(goal_):
    box = soup.findAll('div', class_=goal_)
    percentage = box[0].a.text
    len_ = len(box[0].p.text)
    days = box[0].p.text[:len_ - 9]
    if days.isspace() or days == "":
        days = 0
    date_ = box[0].p.span.text
    print(f"{percentage} vaccination in {days} days on {date_}")


def second_dose(goal_):
    box = soup.findAll('div', class_=goal_)
    percentage = box[1].a.text
    len_ = len(box[1].p.text)
    days = box[1].p.text[:len_ - 9]
    if days.isspace() or days == "":
        days = 0
    date_ = box[1].p.span.text

    print(f"{percentage} vaccination in {days} days on {date_}")


def vaccinated():
    state = soup.findAll('div', class_="box box1")[2].h2.text
    track = soup.findAll('a', href="/vaccinations")
    print(f"{state[:3]} vaccination update")
    print(f"first dose: {track[0].text}\tSecond dose:{track[1].text}")


goals = ["info-item info-item-1 DAYS", "info-item info-item-2 DAYS",
         "info-item info-item-3 DAYS", "info-item info-item-4 DAYS"]

vaccinated()
print()

for goal in goals:
    first_dose(goal)
