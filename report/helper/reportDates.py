from datetime import date
from dateutil.relativedelta import relativedelta
import calendar

class ReportDates:

    def __init__(self):
        self.today = date.today()

    def __date(self, month=0):
        start_date = date(self.today.year, self.today.month,
                          1) - relativedelta(months=month)
        end_date = start_date.replace(day=calendar.monthrange(
            start_date.year, start_date.month)[1])

        return tuple([month, start_date, end_date])

    def __aws_date(self, month=0):
        if self.today.day == 1:
            start_date = date(self.today.year, self.today.month,
                              self.today.day) - relativedelta(days=1)
        else:
            start_date = date(self.today.year, self.today.month,
                              1) - relativedelta(months=month)

        if month == 0:
            end_date = self.today
        else:
            end_date = start_date.replace(day=calendar.monthrange(
                start_date.year, start_date.month)[1])

        return tuple([month, start_date, end_date])

    def day(self):
        return self.today.day

    def number_of_days_in_current_month(self):
        return calendar.monthrange(self.today.year, self.today.month)[1]

    def startAndendDateForMonth(self,month,aws=False):
    
        if aws:
            return self.__aws_date(month=month)
            
        return self.__date(month=month)
