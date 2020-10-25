from datetime import datetime, timedelta
from calendar import HTMLCalendar
from main.models import Pay

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# '일'을 td 태그로 변환하고 pays를 '일'순으로 필터
	def formatday(self, day, pays):
		pays_per_day = pays.filter(date__day=day)
		d = ''
		total = 0
		for pay in pays_per_day:
			total += pay.total
			d = str(total)+'원'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul class='pay_line'> {d} </ul></td>"
		return '<td></td>'

	# '주'를 tr 태그로 변환
	def formatweek(self, theweek, pays):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, pays)
		return f'<tr> {week} </tr>'

	# '월'을 테이블 태그로 변환
	# 각 '월'과 '연'으로 Pay 필터
	def formatmonth(self, withyear=True):
		pays = Pay.objects.filter(date__year=self.year, date__month=self.month)

		cal = f'<table class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, pays)}\n'
		return cal