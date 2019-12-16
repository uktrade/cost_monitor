from aws.helper.manager import AwsRecordManager
from report.helper.reportMonths import ReportMonths
from report.helper.reportForecast import Forecast as ForecastAlgo

class Forecast:

    def __init__(self):

        self.awsManager = AwsRecordManager()
        currentMonthBill = {}
        previousMonthsBill = {}
        forecastData = []
    
        for bill in self.awsManager.getCostByMonth(month=ReportMonths.CURRENT_MONTH.value):
            currentMonthBill.update({bill.account.id: bill.amount})
        
        for bill in self.awsManager.getCostByMonth(month=ReportMonths.PREVIOUS_MONTH.value):
            previousMonthsBill.update({bill.account.id: bill.amount})


        forecastData = ForecastAlgo(currentMonthBill=currentMonthBill,previousMonthBill=previousMonthsBill).forecastData
        self.awsManager.updateForecast(forecastData=forecastData)