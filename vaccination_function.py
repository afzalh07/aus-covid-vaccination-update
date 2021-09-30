import time
from bs4 import BeautifulSoup
import requests
import datetime
import csv
import os

start = time.time()
# local date as the csv filename
t_day = datetime.date.today().strftime("%d-%m-%Y ")
csv_file = open(os.path.join("Daily Update", f"{t_day}.csv"), 'w', newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["States", "First Dose", "Second Dose", "60% First", "70% First",
                     "80% First", "90% First", "60% Second", "70% Second",
                     "80% Second", "90% Second"])


def dose(url):
    """dose function takes the url for each state and parse the html"""
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    city = soup.findAll('div', class_="box box1")[2].h2.text
    track = soup.findAll('a', href="/vaccinations")
    print(f"{city[:3]} vaccination update")
    print(f"first dose: {track[0].text}\tSecond dose:{track[1].text}")

    index = 0
    dose_no = "First"
    days_to = []

    def info(index, dose_no):
        print(f"\n{dose_no} Dose Prediction:")
        goals = ["info-item info-item-1 DAYS", "info-item info-item-2 DAYS",
                 "info-item info-item-3 DAYS", "info-item info-item-4 DAYS"]

        for goal in goals:
            box = soup.findAll('div', class_=goal)
            percentage = box[index].a.text
            # the length of the text of p tag with a child span tag: <p> days <span> date </span> </p>
            len_ = len(box[index].p.text)
            days = box[index].p.text[:len_ - 9]
            date_ = box[index].p.span.text
            # if the goal is already reached
            if days.isspace() or days == "":
                days = 0
                date_ = None
            print(f"{percentage} vaccination in {days} days on {date_}")
            # a list of all the predicted date for csv file
            days_to.append(date_)

        # calling the function again for second dose prediction data
        if index == 0:
            info(1, "Second")
            # create a new row only after collecting data for both doses for a certain city
            csv_writer.writerow([city, track[0].text, track[1].text, days_to[0],
                                 days_to[1], days_to[2], days_to[3], days_to[4],
                                 days_to[5], days_to[6], days_to[7]])

    return info


states = ["https://covidlive.com.au/", "https://covidlive.com.au/nsw",
          "https://covidlive.com.au/vic", "https://covidlive.com.au/qld",
          "https://covidlive.com.au/wa", "https://covidlive.com.au/sa",
          "https://covidlive.com.au/tas", "https://covidlive.com.au/act",
          "https://covidlive.com.au/nt"]

for state in states:
    vaccination = dose(state)
    # calling info function for second dose information
    vaccination(0, "First")
    print()

csv_file.close()

print(f"executed in {(time.time()) - start}")
