import requests
import json
import csv
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


espn_url = "https://www.espn.com"

# week_element = {"Week": int, "Opponent": str, "Winning_Percent": int}

team_dict = {
"MICH" : [],
"MSU" : [],
"MD" : [],
"MINN" : [],
"PSU" :  [],
"IU" :  [],
"IOWA" :  [],
"ILL" :  [],
"NEB" :  [],
"RUTG" :  [],
"NU" :  [],
"WISC" :  [],
"PUR" :  [],
"OSU" :  []

}

week_team_ele = {"Team": str,  "Winning_Percent": int, "Opponent": str}

week_dict = {
1: [], 
2: [],
3: [],
4: [],
5: [],
6: [],
7: [],
8: [],
9: [],
10: [],
11: [],
12: [],
13: [],
14: [],
15: [] 
}
# TODO Loop for WEEK
# Query Week Var
week_num = 4
total_weeks = 16
for week_num in range(week_num,total_weeks):
    URL = f"https://www.espn.com/college-football/schedule/_/week/{week_num}/year/2022/seasontype/2/group/5"
    page_req = requests.get(URL)

    # D_Print URL Request for week x
    # print(page_req.text)


    soup = BeautifulSoup(page_req.content, "html.parser")
    week_sched_tables = soup.find_all("tbody", class_="Table__TBODY")

    # D_Print Table of Full Week Schedule 
    # print(week_sched_table.prettify())
    for week_sched_table in week_sched_tables:
        match_ups = week_sched_table.find_all("td",class_="date__col Table__TD")

        game_link_list = []

        for match_up in match_ups:
            # D_Print Match_up Links
            # print(match_up, end="\n"*2)
            for link in match_up.find_all('a'):
                game_link_list.append(link.get('href'))
        # D_Print print the list of game list
        print(game_link_list)



        for game_link in game_link_list:
            game_url = espn_url + game_link
            game_req = requests.get(game_url)
            soup_game = BeautifulSoup(game_req.content, "html.parser")
            
            away_team_txt = soup_game.find("span", class_="value-away")
            away_team_percent = away_team_txt.text.strip()
            away_team_percent = away_team_percent.replace("%","")
            away_team_percent = float(away_team_percent)
            # For some reason class name is flipped
            away_team_txt = soup_game.find("span", class_="home-team")
            away_team_abbrv = away_team_txt.text.strip()
            print(away_team_percent)
          
            home_team_txt = soup_game.find("span", class_="value-home")
            home_team_percent = home_team_txt.text.strip()
            home_team_percent = home_team_percent.replace("%","")
            home_team_percent = float(home_team_percent)
            # For some reason class name is flipped
            home_team_txt = soup_game.find("span", class_="away-team")
            home_team_abbrv = home_team_txt.text.strip()
            print(home_team_percent)
            
            #Away Team            
            week_element = {"Week": week_num, "Opponent": home_team_abbrv, "Winning_Percent": away_team_percent}
            if away_team_abbrv in team_dict.keys():
                team_dict[away_team_abbrv].append(week_element)
                # Week Dictionary 
                week_team_ele = {"Team": away_team_abbrv,  "Winning_Percent": away_team_percent, "Opponent": home_team_abbrv}
                week_dict[week_num].append(week_team_ele)
            
            # Home Team
            week_team_ele = {"Team": home_team_abbrv,  "Winning_Percent": home_team_percent, "Opponent": away_team_abbrv}
            week_dict[week_num].append(week_team_ele)
            
            week_element = {"Week": week_num, "Opponent": away_team_abbrv, "Winning_Percent": home_team_percent}
            if home_team_abbrv in team_dict.keys():
                team_dict[home_team_abbrv].append(week_element)
                # Week Dictionary 
                week_team_ele = {"Team": home_team_abbrv,  "Winning_Percent": home_team_percent, "Opponent": away_team_abbrv}
                week_dict[week_num].append(week_team_ele)

print(team_dict)
with open("big_ten_match_up_predictor.json","w") as outfile:
    json.dump(team_dict, outfile)
    
with open("big_ten_match_up_predictor_week_sched.json","w") as outfile:
    json.dump(week_dict, outfile)

f = open("big_ten_csv.csv", "w")
writer = csv.writer(f)
for team in team_dict.keys():
    row = [-1] * 15
    row.append(team)
    for week_info in team_dict[team]:
        row[week_info["Week"]-1] = (f'{week_info["Winning_Percent"]}')
    writer.writerow(row)
f.close()
#for week_num in range(week_num,total_weeks):
    