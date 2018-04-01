import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


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

class SorosPlot(object):

    def __init__(self, df_object):
        self.df_object = df_object

    def filter_to_quarter(self, article_quarter):
        quarterly_articles = self.df_object.df[self.df_object.df.index.quarter == article_quarter]
        return quarterly_articles.sum(axis=1).plot(x='Dátum', y='Cikkek', title='Negyedévi Cikkek')
        
    def filter_to_month(self, article_month):
        monthly_articles = self.df_object.df[self.df_object.df.index.month == article_month]
        return monthly_articles.sum(axis=1).plot(x='Dátum', y='Cikkek', title='Havi Cikkek')

    def save_plot_image(self, dataframe, name, show=False):
        dataframe.plot()
        plt.savefig(name+'.png')
        if show == True: plt.show()		
		
if __name__ == '__main__':
    obj = Table('tweet_log.json')
    plot_obj = SorosPlot(obj)
    print(obj.sum_all_columns(month=2))
    plot_obj.save_plot_image(plot_obj.filter_to_quarter(1), '2018Q1', True)

