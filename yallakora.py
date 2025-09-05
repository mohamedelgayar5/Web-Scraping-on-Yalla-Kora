import requests
from bs4 import BeautifulSoup 
import sys
import csv
sys.stdout.reconfigure(encoding='utf-8')


date = input("Enter date in that format yyyymmdd : ")
url = "https://www.yallakora.com/match-center?date=8/30/2025#days"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

def get_info(championships):

    championship_title = championships.contents[1].find("h2").text.strip()
    teams = championships.contents[3].find_all("div", class_ = "teamsData")

    match_detailes = []

    for match in teams:
        team_a = match.find("div", class_="teamA").text.strip()
        team_b = match.find("div", class_="teamB").text.strip()
        match_result = match.find("div", class_ = "MResult").find_all("span", class_ = "score")
        score = f"{match_result[0].text} - {match_result[1].text}"
        match_time = match.find("div", class_ = "MResult").find("span", class_ = "time").text.strip()

        match_detailes.append({"بطولة" : championship_title, "الفريق الاول" : team_a, "النتيجة" : score, "الفريق الثاني" : team_b, "ميعاد المباراة" : match_time})
    return match_detailes        

def main():

    match_detailes = []
    championships = soup.find_all("div", class_="matchCard")
    for champ in championships :
       match_detailes.extend(get_info(champ)) 
    
    keys = match_detailes[0].keys()
    with open('yallakora.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(match_detailes)
        print("file created")

main()
