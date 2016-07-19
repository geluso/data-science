'''
CLASS: Getting Data from APIs

Exercise 1 - retrieving US Census language use data

'''
# Link to the Census Bureau language stats API description page

# Look through the API description links and examples to see what use you have avaialble

# Use the requests library to interact with a URL

import requests
# Use a URL example in a browser to see the result returned and the use request to access with python
# http://api.census.gov/data/2013/language?get=EST,LANLABEL,NAME&for=state:06&LAN=625
r = requests.get('http://api.census.gov/data/2013/language?get=EST,LANLABEL,NAME&for=state:06&LAN=625')

# modify the request to get languges 625 through 650 so we can see a larger sample of what is returned from the request
# Hint the syntax for more than one language number is similar to one we use for multiple elements in a list
print(r.text)


url = "http://api.census.gov/data/2013/language?get=EST,LANLABEL,NAME&for=state:06&LAN=625:650"
r2 = requests.get(url)

# check the status: 200 means success, 4xx means error
if (r.status_code == 200):
    print("everything is ok!")
else:
    print("something went wrong")

# view the raw response text
print(r2.text)

# Convert to json()
jj = r2.json()

# 
#look at the contents of the output of the json() method.  It looks like it can easily become a list of lists

# Convert the jason() method output into a dataframe with the first list as the column header and the rest as rows of data
header = jj[0]
rest = jj[1:]

print(header)
print(len(jj), len(rest))

# Sort the dataframe decending by the number of people speaking the language
# Check the data type of 'EST', the number of people that speak the language
import pandas as pd
df = pd.DataFrame(columns=header, data=rest)
df

ss = df.sort_values("EST")
ss

nums = []
for num in df["EST"]:
    if num is None:
        num = 0
    num = int(num)
    nums.append(num)
nums

df["EST"] = nums
df

ss = df.sort_values("EST")
print(df)
print(ss)

# Now create a new request that brings in the stats for all the us and primary languages
# See the websites links for syntax for us and range of language nunbers



### Bonus
# Create a loop that will collect the counts of Spanish language speakers by state
states = "http://api.census.gov/data/2013/language?get=EST,LANLABEL,NAME&LAN=625&for=state:"
state_speakers = pd.DataFrame(index=["State", "Speakers"], data=[])

res = requests.get(url + "1")
print(res.text)

j2 = res.json()

print("columns:", j2[0])
print("data:", len(j2[1:]))
dd = pd.DataFrame(columns=j2[0], data=j2[1:])
dd.head()

dd.LAN
pop = dd[["NAME", "EST"]][dd.LAN == "625"]
pop

wash = pd.DataFrame([["Washington", 19191], ["Oregon", 27272]], columns=["NAME", "EST"])
wash

cali_start = ["California", 10105385]
empty_start = []
totals = pd.DataFrame(columns=["NAME", "EST"])
# totals = totals.append(wash, ignore_index=True)
totals


url = states + str(2)
state = requests.get(url)
j3 = state.json()
d3 = pd.DataFrame(columns=j3[0], data=j3[1:])
d3

d3 = d3[["NAME", "LAN"]][d3.LAN == "625"]
d3

totals = totals.append(d3)
totals

cols = ["NAME", "EST"]

for i in range(1, 51):
    url = states + str(i)
    print("fetching", url)
    state = requests.get(url)
    try:
        ji = state.json()
        di = pd.DataFrame(ji[1:], columns=ji[0])
        di = di[cols][di.LAN == "625"]
        
        totals = totals.append(di)
        print(di)
    except Exception as e:
        print("Error")
    
#totals
#
#                   NAME       EST
#0               Alabama    151385
#0                Alaska     22425
#0               Alabama    151385
#0                Alaska     22425
#0               Arizona   1230730
#0              Arkansas    143540
#0            California  10105385
#0              Colorado    565060
#0           Connecticut    371025
#0              Delaware     57255
#0  District of Columbia     44455
#0               Florida   3640735
#0               Georgia    709565
#0                Hawaii     25490
#0                 Idaho    114560
#0              Illinois   1570810
#0               Indiana    277380
#0                  Iowa    113175
#0                Kansas    195105
#0              Kentucky    104470
#0             Louisiana    150415
#0                 Maine     11600
#0              Maryland    378010
#0         Massachusetts    502615
#0              Michigan    270695
#0             Minnesota    192115
#0           Mississippi     65295
#0              Missouri    148040
#0               Montana     13930
#0              Nebraska    119505
#0                Nevada    517935
#0         New Hampshire     26815
#0            New Jersey   1277000
#0            New Mexico    553050
#0              New York   2705225
#0        North Carolina    658940
#0          North Dakota      9190
#0                  Ohio    241650
#0              Oklahoma    224325
#0                Oregon    319160
#0          Pennsylvania    525220
#0          Rhode Island    109455
#0        South Carolina    195870
#0          South Dakota     16215
#0             Tennessee    232395
#0                 Texas   6983380
#0                  Utah    245945
#0               Vermont      6180

totals["EST"].astype(int).sum()

# 36316530