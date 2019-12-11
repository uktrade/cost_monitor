from datetime import date
from dateutil.relativedelta import relativedelta
import calendar


class Ranges(object):

    def __init__(self):
        self.today = date.today()

    # def current_month(self, aws=False):
    #     if aws:
    #         return self.__aws_date()
    #     return self.__date()

    # def previous_month(self, aws=False):
    #     return self.__date(month=1)

    def past_6_months(self, aws=False):

        # current month is 0 and, past 6 months is -1 to -6
        months = [0, -1, -2, -3, -4, -5, -6]
        dates_list = []

        for month in months:
            dates = {}
            if aws:
                dates = self.__aws_date(month=month)
            else:
                dates = self.__date(month=month)

            dates_list.append(dates)

        return dates_list

    def day(self):
        return self.today.day

    def number_of_days_in_current_month(self):
        return calendar.monthrange(self.today.year, self.today.month)[1]

    def __date(self, month=0):
        month = abs(month)
        start_date = date(self.today.year, self.today.month,
                          1) - relativedelta(months=month)
        end_date = start_date.replace(day=calendar.monthrange(
            start_date.year, start_date.month)[1])

        return tuple([month, start_date, end_date])

    def __aws_date(self, month=0):
        month = abs(month)
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
