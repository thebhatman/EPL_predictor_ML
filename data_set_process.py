import numpy as np
import pandas as pd
from datetime import datetime as dt
import itertools

season_data_18 = pd.read_csv('E0.csv')
season_data_17 = pd.read_csv('E0(1).csv')
season_data_16 = pd.read_csv('E0(2).csv')
season_data_15 = pd.read_csv('E0(3).csv')
season_data_14 = pd.read_csv('E0(4).csv')
season_data_13 = pd.read_csv('E0(5).csv')
season_data_12 = pd.read_csv('E0(6).csv')
season_data_11 = pd.read_csv('E0(7).csv')
season_data_10 = pd.read_csv('E0(8).csv')
season_data_09 = pd.read_csv('E0(9).csv')
season_data_08 = pd.read_csv('E0(10).csv')
season_data_07 = pd.read_csv('E0(11).csv')
season_data_06 = pd.read_csv('E0(12).csv')
season_data_05 = pd.read_csv('E0(13).csv')
season_data_04 = pd.read_csv('E0(14).csv')
season_data_03 = pd.read_csv('E0(15).csv')
season_data_02 = pd.read_csv('E0(16).csv')
season_data_01 = pd.read_csv('E0(17).csv')

def parse_date(date):
	#print(date,type(date))  
	if date == '' or type(date) != str :
		return None
	else:
		return dt.strptime((date), '%d/%m/%y').date()
	

def parse_date_other(date):
	if date == '':
		return None
	else:
		return dt.strptime((date), '%d/%m/%Y').date()

season_data_01.Date = season_data_01.Date.apply(parse_date)    
season_data_02.Date = season_data_02.Date.apply(parse_date)    
season_data_03.Date = season_data_03.Date.apply(parse_date_other)         # The date format for this dataset is different  
season_data_04.Date = season_data_04.Date.apply(parse_date)    
season_data_05.Date = season_data_05.Date.apply(parse_date)    
season_data_06.Date = season_data_06.Date.apply(parse_date)    
season_data_07.Date = season_data_07.Date.apply(parse_date)    
season_data_08.Date = season_data_08.Date.apply(parse_date)    
season_data_09.Date = season_data_09.Date.apply(parse_date)    
season_data_10.Date = season_data_10.Date.apply(parse_date)
season_data_11.Date = season_data_11.Date.apply(parse_date)
season_data_12.Date = season_data_12.Date.apply(parse_date)
season_data_13.Date = season_data_13.Date.apply(parse_date)
season_data_14.Date = season_data_14.Date.apply(parse_date)
season_data_15.Date = season_data_15.Date.apply(parse_date)
season_data_16.Date = season_data_16.Date.apply(parse_date)
season_data_17.Date = season_data_17.Date.apply(parse_date)
season_data_18.Date = season_data_18.Date.apply(parse_date)

columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HST','AST','HC','AC']

season_stats_01 = season_data_01[columns_req]                      
season_stats_02 = season_data_02[columns_req]
season_stats_03 = season_data_03[columns_req]
season_stats_04 = season_data_04[columns_req]
season_stats_05 = season_data_05[columns_req]
season_stats_06 = season_data_06[columns_req]
season_stats_07 = season_data_07[columns_req]
season_stats_08 = season_data_08[columns_req]
season_stats_09 = season_data_09[columns_req]
season_stats_10 = season_data_10[columns_req]
season_stats_11 = season_data_11[columns_req]   
season_stats_12 = season_data_12[columns_req]
season_stats_13 = season_data_13[columns_req]
season_stats_14 = season_data_14[columns_req]
season_stats_15 = season_data_15[columns_req]
season_stats_16 = season_data_16[columns_req]
season_stats_17 = season_data_17[columns_req]
season_stats_18 = season_data_18[columns_req]

def create_team_dict(season_stats):
	teams = {}
	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = []
	return teams

def goals_scored_till_matchweek(season_stats):
	teams = create_team_dict(season_stats)
	#print(len(season_stats))
	for i in range(len(season_stats)):
		teams[season_stats.iloc[i].HomeTeam].append(season_stats.iloc[i].FTHG)
		teams[season_stats.iloc[i].AwayTeam].append(season_stats.iloc[i].FTAG)

	Cumu_scored_till_matchweek = pd.DataFrame(data = teams, index = [i for i in range(1,39)]).T
	Cumu_scored_till_matchweek[0] = 0
	for i in range(2,39):
		Cumu_scored_till_matchweek[i] = Cumu_scored_till_matchweek[i] + Cumu_scored_till_matchweek[i-1]
	return Cumu_scored_till_matchweek

def goals_conceded_till_matchweek(season_stats):
	teams = create_team_dict(season_stats)
	for i in range(len(season_stats)):
		teams[season_stats.iloc[i].HomeTeam].append(season_stats.iloc[i].FTAG)
		teams[season_stats.iloc[i].AwayTeam].append(season_stats.iloc[i].FTHG)

	Cumu_conceded_till_matchweek = pd.DataFrame(data = teams, index = [i for i in range(1,39)]).T
	Cumu_conceded_till_matchweek[0] = 0
	for i in range(2,39):
		Cumu_conceded_till_matchweek[i] = Cumu_conceded_till_matchweek[i] + Cumu_conceded_till_matchweek[i-1]
	return Cumu_conceded_till_matchweek

def apply_map(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0

def team_result(season_stats):
	teams =  create_team_dict(season_stats)
	for i in range(len(season_stats)):
		if season_stats.iloc[i].FTR == 'H':
			teams[season_stats.iloc[i].HomeTeam].append('W')
			teams[season_stats.iloc[i].AwayTeam].append('L')
		elif season_stats.iloc[i].FTR == 'A':
			teams[season_stats.iloc[i].HomeTeam].append('L')
			teams[season_stats.iloc[i].AwayTeam].append('W')
		else:
			teams[season_stats.iloc[i].HomeTeam].append('D')
			teams[season_stats.iloc[i].AwayTeam].append('D')

	return pd.DataFrame(data = teams, index = [i for i in range(1,39)]).T

def points_till_matchweek(matchres):
	matchres_points = matchres.applymap(apply_map)
	for i in range(2,39):
		matchres_points[i] = matchres_points[i] + matchres_points[i-1]
	#print(season_point_stats)
	matchres_points.insert(column = 0, loc = 0, value = [0*i for i in range(20)])
	#print("new")
	#print(season_point_stats)
	return matchres_points

#print(points_till_matchweek(team_result(season_data_15)))

def update_sheet (season_stats):
	scored = goals_scored_till_matchweek(season_stats)
	conceded = goals_conceded_till_matchweek(season_stats)
	points_so_far = points_till_matchweek(team_result(season_stats))
	row = 0
	HTGS = []
	HTGC = []
	ATGS = []
	ATGC = []
	HTP = []
	ATP = []

	for i in range(380):
		HTGS.append(scored.loc[season_stats.iloc[i].HomeTeam][row])
		HTGC.append(conceded.loc[season_stats.iloc[i].HomeTeam][row])
		ATGS.append(scored.loc[season_stats.iloc[i].AwayTeam][row])
		ATGC.append(conceded.loc[season_stats.iloc[i].AwayTeam][row])
		HTP.append(points_so_far.loc[season_stats.iloc[i].HomeTeam][row])
		ATP.append(points_so_far.loc[season_stats.iloc[i].AwayTeam][row])
		if ( (i+1)%10 == 0 ):
			row+=1

	season_stats['HTGS'] = HTGS
	season_stats['ATGS'] = ATGS
	season_stats['HTGC'] = HTGC
	season_stats['ATGC'] = ATGC
	season_stats['HTP'] = HTP
	season_stats['ATP'] = ATP

	return season_stats

season_data_18 = update_sheet(season_data_18)
season_data_17 = update_sheet(season_data_17)
season_data_16 = update_sheet(season_data_16)
season_data_15 = update_sheet(season_data_15)
season_data_14 = update_sheet(season_data_14)
season_data_13 = update_sheet(season_data_13)
season_data_12 = update_sheet(season_data_12)
season_data_11 = update_sheet(season_data_11)
season_data_10 = update_sheet(season_data_10)
season_data_09 = update_sheet(season_data_09)
season_data_08 = update_sheet(season_data_08)
season_data_07 = update_sheet(season_data_07)
season_data_06 = update_sheet(season_data_06)
season_data_05 = update_sheet(season_data_05)
season_data_04 = update_sheet(season_data_04)
season_data_03 = update_sheet(season_data_03)
season_data_02 = update_sheet(season_data_02)
season_data_01 = update_sheet(season_data_01)

def get_form(playing_stat,num):
	form = team_result(playing_stat)
	form_final = form.copy()
	for i in range(num,39):
		form_final[i] = ''
		j = 0
		while j < num:
			#print(form[i])
			#print(type(form[i]))
			form_final[i] += form[i-j]
			j += 1           
	return form_final

def add_form(playing_stat,num):
	form = get_form(playing_stat,num)
	h = ['M' for i in range(num * 10)]  # since form is not available for n MW (n*10)
	a = ['M' for i in range(num * 10)]
	
	j = num
	for i in range((num*10),380):
		ht = playing_stat.iloc[i].HomeTeam
		at = playing_stat.iloc[i].AwayTeam

		past = form.loc[ht][j]               # get past num results
		h.append(past[num-1])                    #recent result
		
		#print('past')
		#print(past)
		#print('past-N')
		#print(past[num-1])

		past = form.loc[at][j]               # get past n results.
		a.append(past[num-1])                   # 0 index is most recent
		
		if ((i + 1)% 10) == 0:
			j = j + 1

	playing_stat['HM' + str(num)] = h                 
	playing_stat['AM' + str(num)] = a

	#print('new')
	
	return playing_stat


def add_form_df(season_stats):
	season_stats = add_form(season_stats,1)
	season_stats = add_form(season_stats,2)
	season_stats = add_form(season_stats,3)
	season_stats = add_form(season_stats,4)
	season_stats = add_form(season_stats,5)
	return season_stats  

#print(add_form(season_data_01,3))


season_data_01 = add_form_df(season_data_01)
season_data_02 = add_form_df(season_data_02)
season_data_03 = add_form_df(season_data_03)
season_data_04 = add_form_df(season_data_04)
season_data_05 = add_form_df(season_data_05)
season_data_06 = add_form_df(season_data_06)
season_data_07 = add_form_df(season_data_07)
season_data_08 = add_form_df(season_data_08)
season_data_09 = add_form_df(season_data_09)
season_data_10 = add_form_df(season_data_10)
season_data_11 = add_form_df(season_data_11)
season_data_12 = add_form_df(season_data_12)
season_data_13 = add_form_df(season_data_13)
season_data_14 = add_form_df(season_data_14)
season_data_15 = add_form_df(season_data_15)    
season_data_16 = add_form_df(season_data_16)

	