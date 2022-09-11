import requests
from bs4 import BeautifulSoup


''' Notes
* Table of Intrest : 
 - Table__TBODY : <tbody class="Table__TBODY">
 - Table__TR Table__TR--sm Table__even
 - date__col Table__TD: <td class="date__col Table__TD">
 - AnchorLink ... get herf link from here


TODO: 
    * Handle multiple Table__TBODY (Thrus/Sat weeks)
    * store meta info on number of data_col links recovered for debuging 
    * Store data of match_ups in:
        * Week x: [links..]
    * Go to each links in the week and recover both team:
        * 

'''

# Todo Update for x Week in Url
URL = "https://www.espn.com/college-football/schedule/_/week/3/year/2022/seasontype/2/group/5"
page_req = requests.get(URL)

# D_Print URL Request for week x
# print(page_req.text)


soup = BeautifulSoup(page_req.content, "html.parser")
week_sched_table = soup.find("tbody", class_="Table__TBODY")

# D_Print Table of Full Week Schedule 
# print(week_sched_table.prettify())

match_ups = week_sched_table.find_all("td",class_="date__col Table__TD")

game_link_list = []

for match_up in match_ups:
    # D_Print Match_up Links
    # print(match_up, end="\n"*2)
    for link in match_up.find_all('a'):
        game_link_list.append(link.get('href'))
# D_Print print the list of game list
print(game_link_list)

