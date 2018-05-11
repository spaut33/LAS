import MySQLdb
from settings import Settings
from workcalendar import WorkCalendar
from datetime import datetime, timedelta


# Function to create etalon array of dates
def _dates_range(d1, d2):
    delta = d2 - d1  # assumes second date is always after first
    days_list = [d1 + timedelta(days=i) for i in range(delta.days)]
    return [d for d in days_list if not d.isoweekday() in [6, 7]]


w_calendar = WorkCalendar()
holidays = w_calendar.holidays
workdays = w_calendar.workdays
# print('# Holidays from working calendar:\n' + str(holidays))
# print('# Forced working days from working calendar: \n' + str(workdays))

# Start day of period
start_date = datetime.today().replace(year=datetime.today().year,
                                      month=1,
                                      day=1,
                                      hour=0,
                                      minute=0,
                                      second=0,
                                      microsecond=0)
# End day of period for
end_date = datetime.today().replace(year=datetime.today().year,
                                    month=12,
                                    day=31,
                                    hour=0,
                                    minute=0,
                                    second=0,
                                    microsecond=0)

# Let's create etalon array
date_set = _dates_range(start_date, end_date)
# print('# All calendar except days 6 and 7: \n' + str(date_set))
workdays_only = set(date_set) - set(holidays)
final_calendar = set(workdays_only) | set(workdays)
# Sort list by dates
final_calendar = sorted(final_calendar)
# print('# Final calendar: \n' + str(final_calendar))
date_strings = []
for dt in final_calendar:
    date_strings.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
# print(date_strings)
# Connection to DB
db = MySQLdb.connect(Settings.db_host, Settings.db_user,
                     Settings.db_pass, Settings.db_base, charset="utf8")
cursor = db.cursor()
cursor.execute("TRUNCATE TABLE work_calendar")
sql = """INSERT INTO work_calendar(workdate) VALUES (%s)"""
sql_query = cursor.executemany(sql, (date_strings))
print("Total workdays: " + str(sql_query))
db.commit()
db.close()
