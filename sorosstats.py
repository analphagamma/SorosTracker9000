import json
import pandas as pd

def init_dataframe(logfile):
	'''loads the json logfile
	   creates a dataframe
	   In -> json filename in string format
	   Out -> pandas dataframe'''
	   
	with open(logfile, 'r+') as f: tweet_log = json.load(f)
	
	for date, results in tweet_log.items():
		for source, links in results.items():
			tweet_log[date][source] = len(links)
	
	df = pd.DataFrame(tweet_log).T
	df.index = pd.to_datetime(df.index)
	
	return df

def sum_all_columns(dataframe, week='all', month='all'):
	
	if week == 'all' and month == 'all':
		return dataframe.sum()
	elif week == 'all' and month != 'all':
		try:
			int(month)
		except ValueError:
			return 'Incorrect month number.'
		else:
			return dataframe[dataframe.index.month == int(month)].sum()
	elif week != 'all' and month == 'all':
		try:
			int(week)
		except ValueError:
			return 'Incorrect week number.'
		else:
			return dataframe[dataframe.index.week == int(week)].sum()
	else:
		return None

df = init_dataframe('tweet_log.json')
print(sum_all_columns(df))
print(sum_all_columns(df, week='44'))

