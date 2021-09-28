import main
import time

start = time.perf_counter()
# all the states url listed twice for both doses
states = ["https://covidlive.com.au/", "https://covidlive.com.au/",
          "https://covidlive.com.au/nsw", "https://covidlive.com.au/nsw",
          "https://covidlive.com.au/vic", "https://covidlive.com.au/vic",
          "https://covidlive.com.au/qld", "https://covidlive.com.au/qld",
          "https://covidlive.com.au/wa", "https://covidlive.com.au/wa",
          "https://covidlive.com.au/sa", "https://covidlive.com.au/sa",
          "https://covidlive.com.au/tas", "https://covidlive.com.au/tas",
          "https://covidlive.com.au/act", "https://covidlive.com.au/act",
          "https://covidlive.com.au/nt", "https://covidlive.com.au/nt"]


# alternate list to select div tag for both doses
index = [None]*18
index[::2] = [0 for _ in range(9)]
index[1::2] = [1 for _ in range(9)]

dose_no = [None]*18
dose_no[::2] = ["First" for _ in range(9)]
dose_no[1::2] = ["Second" for _ in range(9)]


# creating instances of Dose class by zipping the arguments
for params in zip(states, index, dose_no):
    # creating an object of Dose class
    data = main.Dose(params[0], params[1], params[2])
    data.info()
    print()

main.csv_file.close()
end = time.perf_counter()
print(f"Executed in {end-start} seconds")
