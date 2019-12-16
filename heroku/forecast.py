from heroku.helper.manager import HerokuRecordManager
from report.helper.reportMonths import ReportMonths
from report.helper.reportForecast import Forecast as ForecastAlgo

class Forecast:

    def __init__(self):

        self.herokuManager = HerokuRecordManager()
        currentMonthBill = {}
        previousMonthsBill = {}
        forecastData = []
    
        for bill in self.herokuManager.getCostByMonth(month=ReportMonths.CURRENT_MONTH.value):
            currentMonthBill.update({bill.team.id: bill.amount})
        
        for bill in self.herokuManager.getCostByMonth(month=ReportMonths.PREVIOUS_MONTH.value):
            previousMonthsBill.update({bill.team.id: bill.amount})


        forecastData = ForecastAlgo(currentMonthBill=currentMonthBill,previousMonthBill=previousMonthsBill).forecastData
    
        self.herokuManager.updateForecast(forecastData=forecastData)