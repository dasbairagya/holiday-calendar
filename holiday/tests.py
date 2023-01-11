#!/usr/bin/python
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date

from . import views
from .models import Holiday, Admin, Cities


class PageHitTests(TestCase):
    # Get
    def test_holidays_page(self):
        response = self.client.get('/holidays/all/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/cities/')
        self.assertEquals(response.status_code, 200)

    # Post
    def test_create_page(self):
        response = self.client.get('/create/')
        self.assertEquals(response.status_code, 405)
        response_mon = self.client.get('/monthly/')
        self.assertEquals(response_mon.status_code, 405)
        response_day = self.client.get('/daily/')
        self.assertEquals(response_day.status_code, 405)
        response_upload = self.client.get('/upload/')
        self.assertEquals(response_upload.status_code, 405)


class HolidayModelTests(TestCase):
    def setUp(self):
        Holiday.objects.create(id=1, holidayName="testHoliday1", date="2018-01-05", city_name="chennai")
        Holiday.objects.create(id=2, holidayName="testHoliday2", date="2019-01-05", city_name="chennai")

    def test_holiday_text_content(self):
        holiday = Holiday.objects.get(id=1)
        expected_object_name = holiday.holidayName
        expected_date = holiday.date.strftime("%d/%m/%Y")
        expected_city = holiday.city_name
        self.assertEquals(expected_object_name, 'testHoliday1')
        self.assertEquals(expected_city, 'chennai')
        self.assertEquals(expected_date, '05/01/2018')


class AdminModelTests(TestCase):
    def setUp(self):
        Admin.objects.create(id=1, admin_name="admin", admin_email="test@admin.com", password="password")

    def test_admin_text_content(self):
        admin = Admin.objects.get(id=1)
        expected_email = admin.admin_email
        expected_password = admin.password
        self.assertEquals(expected_email, 'test@admin.com')
        self.assertEquals(expected_password, 'password')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Holiday.objects.create(id=11, holidayName="testHoliday1", date="2018-01-05", city_name="testcity1")
        Holiday.objects.create(id=12, holidayName="testHoliday2", date="2019-01-05", city_name="testcity2")
        Holiday.objects.create(id=13, holidayName="testHoliday3", date="2019-01-07", city_name="testcity2")
        Cities.objects.create(id=1, cityName="Hyderabad")
        Cities.objects.create(id=2, cityName="Chennai")
        Cities.objects.create(id=3, cityName="Pune")
        Admin.objects.create(id=1, admin_name="admin", admin_email="test@admin.com", password="password")

    def test_view_list_all_holidays(self):
        response = self.client.get('/holidays/all/')
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content,
                             [{"city_name": "testcity1", "date": "05/01/2018", "holidayName": "testHoliday1"},
                              {"city_name": "testcity2", "date": "05/01/2019", "holidayName": "testHoliday2"},
                              {"city_name": "testcity2", "date": "07/01/2019", "holidayName": "testHoliday3"}])

    def test_view_monthly(self):
        req_data = {
            "city_name": "testcity2",
            "year": 2019,
            "month": 1
        }
        response = self.client.post('/monthly/', req_data)
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content, [{"id": 12, "date": "05/01/2019", "holidayName": "testHoliday2"},
                                                {"id": 13, "date": "07/01/2019", "holidayName": "testHoliday3"}])

    def test_view_monthly_with_no_result(self):
        req_data_with_no_output = {"city_name": "testcity1", "year": 2019, "month": 1}
        response = self.client.post('/monthly/', req_data_with_no_output)
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content, {})

    def test_admin_login_view(self):
        req_data = {"admin_email": "test@admin.com", "password": "password"}
        response = self.client.post('/admin/login/', req_data)
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content, {"status": 1})

    def test_view_daily(self):
        req_data = {
            "city_name": "testcity2",
            "date": "05/01/2019"
        }
        response = self.client.post('/daily/', req_data)
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content, {"id": 12, "date": "05/01/2019", "holidayName": "testHoliday2"})

    def test_view_create(self):
        req_data = {"city_name": "testcity3", "date": "2022-10-30", "holidayName": "testHoliday3"}
        response = self.client.post('/create/', req_data)
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content, {"status": 1})

    def test_view_create_with_past_date(self):
        req_data = {"city_name": "testcity4", "date": "2016-10-30", "holidayName": "testHoliday4"}
        response = self.client.post('/create/', req_data)
        self.assertEqual(response.status_code, 400)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content, '{"date":["Date cannot be in the past"]}')

    def test_valid(self):
        with open('test_Valid.csv') as fp:
            response = self.client.post('/upload/', {'file': fp})
            self.assertEqual(response.status_code, 200)
            response_content = response.content.decode("utf-8")
            self.assertJSONEqual(response_content, {"status": 1})
            fp.close()

    def test_upload_invalid(self):
        with open('test_Invalid.csv') as fp:
            response = self.client.post('/upload/', {'file': fp})
            self.assertEqual(response.status_code, 200)
            response_content = response.content.decode("utf-8")
            self.assertJSONEqual(response_content, {"status": 0})
            fp.close()

    def test_upload_invalid_with_cities(self):
        with open('test_Invalid_with_cities.csv') as fp:
            response = self.client.post('/upload/', {'file': fp})
            self.assertEqual(response.status_code, 200)
            response_content = response.content.decode("utf-8")
            self.assertJSONEqual(response_content, {"status": 0})
            fp.close()

    def test_all_city_names(self):
        response = self.client.get('/cities/')
        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertJSONEqual(response_content,
                             [{"cityName": "Hyderabad"}, {"cityName": "Chennai"}, {"cityName": "Pune"}])

    def test_del_holiday_name(self):
        response = self.client.delete('/deleteholidayinfo/12/')
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        req_data = {"city_name": "testupdate", "date": "29/11/2029", "holidayName": "testupdate"}
        response = self.client.put('/updateholidayinfo/13/', req_data, content_type='application/json')
        response_content = response.content.decode("utf-8")
        # print(response_content)
        self.assertJSONEqual(response_content, {"status": 1})
        response = self.client.get('/holidays/all/')
        update_response = response.content.decode("utf-8")
        self.assertJSONEqual(update_response,
                             [{"city_name": "testcity1", "date": "05/01/2018", "holidayName": "testHoliday1"},
                              {"city_name": "testcity2", "date": "05/01/2019", "holidayName": "testHoliday2"},
                              {"city_name": "testupdate", "date": "29/11/2029", "holidayName": "testupdate"}])





