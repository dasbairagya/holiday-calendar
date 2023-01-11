import csv
from datetime import datetime
import datetime as dt
from .models import Holiday, Admin, Cities


# Method to return a upload flag based on the criteria to upload
def check_date(tmp_file):
    # Open the temp file for working on date
    with open(tmp_file, 'r+') as test:
        reader = csv.reader(test)
        next(test)
        included_cols = [1]
        included_cols_city = [0]
        date_content = []
        city_content = []
        # fetch all dates and store in a list
        for row in reader:
            content = list(row[i] for i in included_cols)
            citycontent = list(row[j] for j in included_cols_city)
            date_content.append(content[0])
            city_content.append(citycontent[0].lower())

        # get the current date and extract month and year
        today = dt.date(2019, 11, 25)
        current_month = today.month
        current_year = today.year
        upload_flag = 0

        # Logic for checking city
        queryset = Cities.objects.all()
        db_city_content = []
        for a in queryset:
            db_city_content.append(a.cityName.lower())

        city_flag = 0
        if (all(x in db_city_content for x in city_content)):
            city_flag = 1

        # Logic for the upload in the next year
        for a in date_content:
            a = datetime.strptime(a, "%d/%m/%Y").date()

            if a.year > current_year:
                if a.year - 1 == current_year and current_month == 11:
                    upload_flag = 1
            elif a.year == current_year:
                upload_flag = 1

        if city_flag == 1 and upload_flag == 1:
            return 1
        else:
            return 0
