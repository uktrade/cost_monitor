from report.models import ReportDate

class ReportManager:

  def reportDates(self):
    return ReportDate.objects.all()
  
  def reportDatesByMonth(self,month):
    return self.reportDates().filter(month=month)
    
  def updateReportDate(self,month,start_date,end_date):
    pk_exist = ReportDate.objects.filter(pk=month)

    if pk_exist:
          pk_exist.update(start_date=start_date,end_date=end_date)
    
    else:
      ReportDate.objects.update_or_create(month=month,start_date=start_date,end_date=end_date)