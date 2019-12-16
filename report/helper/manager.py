from report.models import ReportDate

class ReportManager:

  def reportDates(self):
    return ReportDate.objects.all()
  
  def reportDatesByMonth(self,month):
    return self.reportDates().filter(month=month)
    
  def updateReportDate(self,month,start_date,end_date):
    ReportDate.objects.update_or_create(month=month,start_date=start_date,end_date=end_date)