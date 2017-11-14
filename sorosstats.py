import json
import pandas as pd


class Table(object):
	
	
	def __init__(self, logfile, df=pd.DataFrame()):
		self.logfile = logfile
		self.df = df
		with open(logfile, 'r+') as f: tweet_log = json.load(f)
		for date, results in tweet_log.items():
			for source, links in results.items():
				tweet_log[date][source] = len(links)
		
		self.df = pd.DataFrame(tweet_log).T
		self.df.index = pd.to_datetime(self.df.index)
		self.df.fillna(0, inplace=True)
		#print(type(self.df['Origo.hu'][0]))
		self.df = self.df.astype('int64', inplace=True)
		
	def show_all(self):
		return print(self.df)
		
	def sum_all_columns(self, week='all', month='all'):
	
		if week == 'all' and month == 'all':
			return self.df.sum()
		elif week == 'all' and month != 'all':
			try:
				int(month)
			except ValueError:
				return 'Incorrect month number.'
			else:
				return self.df[self.df.index.month == int(month)].sum()
		elif week != 'all' and month == 'all':
			try:
				int(week)
			except ValueError:
				return 'Incorrect week number.'
			else:
				return self.df[self.df.index.week == int(week)].sum()
		else:
			return None
	def sum_today(self):
		return self.df[self.df.index == pd.Timestamp("today").strftime("%Y-%m-%d")].sum()
			
	def todays_most(self):
		'''Returns the name of the source and the number of articles posted today'''
				
		today = pd.Timestamp("today").strftime("%Y-%m-%d")	
		return (self.df[self.df.index == today].max().idxmax(), self.df[self.df.index == today].max().max())
		
		
if __name__ == '__main__':
	obj = Table('tweet_log.json')
	print(obj.sum_today())
