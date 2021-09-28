from bs4 import BeautifulSoup
import requests
import csv
import datetime
import os


# local date as the csv filename
t_day = datetime.date.today().strftime("%d-%m-%Y ")
csv_file = open(os.path.join("Daily Update", f"{t_day}.csv"), 'w', newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["States", "First Dose", "Second Dose", "60% On", "70% On",
                     "80% On", "90% On"])


class Dose:
    """ The Dose class will create an object for each url and dose number """

    # class variable count, keeps track of the execution of vaccinated() method
    count = 1

    def __init__(self, url, index, dose_no):
        self.soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        self.index = index  # 0- first dose; 1- second dose
        self.dose_no = dose_no
        # variables to access from the csv_file_ method
        self.state, self.first_done, self.second_done = [None, None, None]
        self.days_to = []

        Dose.count += 1
        if Dose.count % 2 == 0:
            self.vaccinated()

    def info(self):
        """ The info method parse and print the data for each percentage goal """

        print(f"\n{self.dose_no} Dose Prediction:")
        # goals is the class name for each div tag of percentage data
        goals = ["info-item info-item-1 DAYS", "info-item info-item-2 DAYS",
                 "info-item info-item-3 DAYS", "info-item info-item-4 DAYS"]

        for goal in goals:
            box = self.soup.findAll('div', class_=goal)
            percentage = box[self.index].a.text
            # the length of the text of p tag with a child span tag: <p> days <span> date </span> </p>
            len_ = len(box[self.index].p.text)
            days = box[self.index].p.text[:len_ - 9]
            date_ = box[self.index].p.span.text
            # if the goal is already reached
            if days.isspace() or days == "":
                days = 0
                date_ = None
            print(f"{percentage} vaccination in {days} days on {date_}")
            # a list of all the predicted date for csv file
            self.days_to.append(date_)
        self.csv_file_()

    def vaccinated(self):
        """ The vaccinated method prints the sate name along with vaccination
        update of both doses. This method only executes once for a
        certain state, since each url used twice for two different instances"""

        state = self.soup.findAll('div', class_="box box1")[2].h2.text
        track = self.soup.findAll('a', href="/vaccinations")
        self.state = state[:3]
        print(f"{self.state} vaccination update")
        self.first_done, self.second_done = track[0].text, track[1].text
        print(f"First dose: {self.first_done} \tSecond dose: {self.second_done}")

    def csv_file_(self):
        """Creating a csv file called from "info" method"""
        csv_writer.writerow([self.state, self.first_done, self.second_done, self.days_to[0],
                            self.days_to[1], self.days_to[2], self.days_to[3]])
