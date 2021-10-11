import time
from bs4 import BeautifulSoup
import requests
import csv
import datetime
import os

start = time.time()
# local date as the csv filename
t_day = datetime.date.today().strftime("%d-%m-%Y ")
csv_file = open(os.path.join("Daily Update", f"{t_day}.csv"), 'w', newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["States", "First Dose", "Second Dose", "60% First", "70% First",
                     "80% First", "90% First", "60% Second", "70% Second",
                     "80% Second", "90% Second"])


class Dose:
    """ The Dose class will create an instance for each url"""

    def __init__(self, url):
        self.soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # variables to access from info method
        self.state = self.soup.findAll('div', class_="box box1")[2].h2.text[:3]
        self.track = self.soup.findAll('a', href="/vaccinations")
        self.days_to = []
        # state name and vaccinated data
        print(f"{self.state} vaccination update")
        print(f"First dose: {self.track[0].text} \tSecond dose: {self.track[1].text}")

    def info(self, index, dose_no):
        """ The info method parse and print the data for each percentage goal """

        print(f"\n{dose_no} Dose Prediction:")
        # goals is the class name for each div tag of percentage data
        goals = ["info-item info-item-1 DAYS", "info-item info-item-2 DAYS",
                 "info-item info-item-3 DAYS", "info-item info-item-4 DAYS"]

        for goal in goals:
            box = self.soup.findAll('div', class_=goal)
            percentage = box[index].a.text
            # the length of the text of p tag with a child span tag: <p> days <span> date </span> </p>
            len_ = len(box[index].p.text)
            days = box[index].p.text[:len_ - 9]
            try:
                date_ = box[index].p.span.text
            except AttributeError:
                date_ = None
            # if the goal is already reached
            if days.isspace() or days == "":
                days = 0
                date_ = None
            print(f"{percentage} vaccination in {days} days on {date_}")
            # a list of all the predicted date for csv file
            self.days_to.append(date_)
        # calling the function again for second dose prediction data
        if index == 0:
            self.info(1, "Second")
            # create a new row only after collecting data for both doses for a certain city
            csv_writer.writerow([self.state, self.track[0].text, self.track[1].text, self.days_to[0],
                                 self.days_to[1], self.days_to[2], self.days_to[3], self.days_to[4],
                                 self.days_to[5], self.days_to[6], self.days_to[7]])


states = ["https://covidlive.com.au/", "https://covidlive.com.au/nsw",
          "https://covidlive.com.au/vic", "https://covidlive.com.au/qld",
          "https://covidlive.com.au/wa", "https://covidlive.com.au/sa",
          "https://covidlive.com.au/tas", "https://covidlive.com.au/act",
          "https://covidlive.com.au/nt"]

for state in states:
    vaccination = Dose(state)
    # calling the info method for first dose information
    vaccination.info(0, "First")
    print()

csv_file.close()
print(f"executed in {(time.time()) - start}")
