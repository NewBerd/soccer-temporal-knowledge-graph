import requests
from bs4 import BeautifulSoup
import json

def parser_player_inform(url, headers):
	response=requests.get(url,headers=headers)#提交请求
	if response.status_code==200:
	    response.encoding = 'utf-8'
	if response.status_code == 404:
		return None

	player_infos = {}
	player_infos["url"] = url
	print(url) 

	soup = BeautifulSoup(response.text, 'lxml')
	player_content = soup.find(name="div", class_="player-con")
	info_left = player_content.find(name="div", class_="info-left")

	#解析基本信息
	base_info = {}
	for item in info_left.find_all(name='li'):
	    children = item.contents
	    if len(children) == 2:
	    	base_info[children[0].string.rstrip("：")] = children[1]
	    else:
	    	base_info[children[0].string.rstrip("：")] = ""

	china_name = info_left.find(name="p", class_="china-name")
	if china_name:
	    base_info["中文名"] = china_name.contents[0]

	english_name = info_left.find(name="p", class_="en-name")
	if english_name:
	    base_info["英文名"] = english_name.string
	player_infos["base_info"] = base_info

	#解析比赛信息
	list_ = []
	player_left = player_content.find(name='div', class_='player-left')
	player_data = player_left.find(name="div", class_="player-data")
	match_data = player_data.find(name="div", class_="match-data")
	match_data_con = match_data.find(name='div', class_="match-data-con")
	try:
		table = match_data_con.div.div
		for row in table.find_all(name="p"):
		#     print(row)
		    l = []
		    for item in row.find_all(name="span"):
		        l.append(item.string)
		    list_.append(l)
	except:
		pass
	player_infos["match_data"] = list_

	#解析荣誉信息
	honor_data = player_data.find(name="div", class_="hornor-record")
	hd = []
	try:
		for item in honor_data.find_all(name='div', class_="hornor-list"):
		#     print(item.prettify())
		    l = []
		    l.append(item.find(name="span", class_="champion").string)
		    l.append(item.find(name="b").string)
		    hd.append(l)
	except:
		pass
	player_infos["honor_data"] = hd

	#解析转会信息
	transfer_data = player_data.find(name='div', class_="transfer-data")
	trans_table = []
	try:
		for item in transfer_data.find_all(name="div", class_="transfer"):
		#     print(item.prettify())
		    l = []
		    date = item.find(name="span", class_="date").string
		    l.append(date)
		    old = item.find(name="span", class_="team-icon team-a").b.string
		    l.append(old)
		    new = item.find(name="span", class_="team-icon team-b").b.string
		    l.append(new)
		    trans_table.append(l)
	except:
		pass
	player_infos["transfer_data"]=trans_table

	#解析受伤数据
	injured = player_data.find(name="div", class_="injured")
	injured_table = []
	try:
		for item in injured.find_all(name="p", class_="injured-item"):
		    # print(item)
		    row = []
		    for i in item.find_all(name="span"):
		        row.append(i.string)
		    injured_table.append(row)
	except:
		pass
	player_infos["injured_data"] = injured_table

	#解析能力数据
	cap_dic = {}
	player_right = player_content.find(name="div", class_="player-right")
	capability = player_right.find(name="div", class_="capability")
	if capability:
		average = capability.find(name="p", class_="average")
		box_chart = capability.find(name='div', class_="box_chart")
		aver = average.contents
		cap_dic[aver[0]] = aver[1].string
		first = True
		for item in box_chart.find_all(name="div"):
		    if first:
		        first = False
		    else:
		        ite = item.contents
		        cap_dic[ite[0]] = ite[1].string
	player_infos["capability_data"] = cap_dic

	return player_infos

def parser_team_inform(url, headers):
	response=requests.get(url,headers=headers)#提交请求
	if response.status_code==200:
	    response.encoding = 'utf-8'
	if response.status_code == 404:
		return None

	team_infos = {"url": url}
	print(url)

	soup = BeautifulSoup(response.text, 'lxml')
	_layout = soup.find(name="div", id="__layout")
	team_data_wrap = _layout.find(name="div", class_="team-data-wrap")
	team_con = team_data_wrap.find(name="div", class_="team-con")
	team_left = team_con.find(name="div", class_="team-left")
	team_right = team_con.find(name="div", class_="team-right")
	team_info = team_left.find(name="div", class_="team-info")
	team_relate_info = team_left.find(name="div", class_="team-relate-info")
	team_info_con = team_info.find(name="div", class_="info-con")

	#解析基本信息
	team_base_info = {}
	for spn in team_info_con.find_all(name="span"):
	    # print(spn)
	    con = spn.contents
	    team_base_info[con[0].string.strip("：").replace(" ", "")] = con[1]
	team_name = team_info_con.find(name="p", class_="team-name").contents[0]
	team_base_info["team_name"] = team_name
	english_name = team_info_con.find(name="p", class_="en-name").contents[0]
	team_base_info["english_name"] = english_name
	address = team_info_con.find(name="p", class_="address").contents
	team_base_info[address[0].string.strip("：").replace(" ", "")] = address[1]
	team_infos["team_base_info"] = team_base_info

	#解析球队的运动员
	team_player = []
	item_th = []
	for item in team_relate_info.find(name="p", class_="item-th").find_all(name="span"):
	    # print(item)
	    item_th.append(item.string)
	team_player.append(item_th)
	team_related_player = team_relate_info.find(name="div", class_="team-player-data")
	for item in team_related_player.find_all(name="p"):
	#     print(item)
	    player_info = []
	#     item1 = item.find(name="span", class_="item1")
	#     player_info.append(item1.string)
	#     item2 = item.find(name="span", class_="item2")
	#     player_info.append(item2.string)
	#     item3 = item.find(name="span", class_="item3")
	#     player_info.append(item3.)
	    for it in item.find_all(name="span"):
	#         print(it)
	        player_info.append(it.find_all(text=True))
	    team_player.append(player_info)
	team_infos["team_related_player"] = team_player

	#解析球队荣誉数据
	hornor = team_relate_info.find(name="div", class_="hornor-record")
	hornor_dict = {}
	for item in hornor.find_all(name="div", class_="hornor-list"):
	#     print(item.prettify())
	    champion = item.find(name="span", class_="champion", text=True)
	    time = item.find_all(name="b")
	    hornor_dict[champion.string.split("X")[0].strip()] = [e.string for e in time]
	team_infos["honor_record"] = hornor_dict

	return team_infos

def get_players():
	url_ = "https://www.dongqiudi.com/player/"
	headers={
            'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3) \
            AppleWebKit/537.36(KHTML,like Gecko) \
            Chrome/65.0.3325.162 Safari/537.36'
    }#设置代理浏览器
	players = []
	with open("players_url", "r", encoding="utf-8") as f:
		for url in f.readlines():
			player = parser_player_inform(url, headers)
			if player:
				players.append(player)
	# for i in range(1, 50000):
	# 	url = url_ + "{}.html".format(i)
	# 	player = parser_player_inform(url, headers)
	# 	if player:
	# 		players.append(player)
	return players

def get_teams():
	url_ = "https://www.dongqiudi.com/team/"
	headers={
            'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3) \
            AppleWebKit/537.36(KHTML,like Gecko) \
            Chrome/65.0.3325.162 Safari/537.36'
    }#设置代理浏览器
	teams = []
	# for i in range(1, 1000):
	# 	url = url_ + "{}.html".format(i)
	# 	team = parser_team_inform(url, headers)
	# 	if team:
	# 		teams.append(team)
	url = "https://www.dongqiudi.com/team/50004829.html"
	team = parser_team_inform(url, headers)
	if team:
		teams.append(team)
	return teams

def save(list_, filename):
	with open(filename, "w", encoding="utf-8") as f:
		for li in list_:
			li = json.dumps(li)
			f.write(li+"\n")
		# f.writelines(list)

def main():
	players = get_players()
	players_file = "players.txt"
	save(players, players_file)

	teams = get_teams()
	teams_file = "teams.txt"
	save(teams, teams_file)


if __name__ == '__main__':
	main()







