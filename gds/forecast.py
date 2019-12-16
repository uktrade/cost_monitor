from gds.helper.manager import GDSRecordManager
from report.helper.reportMonths import ReportMonths
from report.helper.reportForecast import Forecast as ForecastAlgo

class Forecast:

    def __init__(self):

        self.gdsManager = GDSRecordManager()
        currentMonthBill = {}
        previousMonthsBill = {}
        forecastData = []
    
        for bill in self.gdsManager.getCostByMonth(month=ReportMonths.CURRENT_MONTH.value):
            currentMonthBill.update({bill.space_id.id: bill.amount})
        
        for bill in self.gdsManager.getCostByMonth(month=ReportMonths.PREVIOUS_MONTH.value):
            previousMonthsBill.update({bill.space_id.id: bill.amount})


        forecastData = ForecastAlgo(currentMonthBill=currentMonthBill,previousMonthBill=previousMonthsBill).forecastData
        self.gdsManager.updateForecast(forecastData=forecastData)