from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from .models import Admin, Holiday, Cities


# Holiday serializer with id, cityname , date and holidayname
# Name ----> HolidaySerializer
class HolidaySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # city_name=serializers.CharField(max_length=50)
    # date = serializers.DateField(format="%Y-%m-%d")
    # holidayName=serializers.CharField(max_length=50)

    class Meta:
        model = Holiday
        fields = '__all__'


# holidaylistserializer with cityname, date and holidayname
# Name ----->HolidayListSerializer
class HolidayListSerializer(serializers.ModelSerializer):
    # cityname=serializers.CharField(max_length=50)
    date = serializers.DateField(format="%d/%m/%Y")

    # holidayname=serializers.CharField(max_length=50)

    class Meta:
        model = Holiday
        fields = ["city_name", "date", "holidayName"]


# uploadserializer with a field --> file which is not present in the holiday model
# Name---->UploadSerializer
class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Holiday
        # fields = '__all__'
        fields = ["file"]


# citylistserializer with cityname
# Name ----->CityListSerializer
class CityListSerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(max_length=50)

    class Meta:
        model = Cities
        fields = ["cityName"]


# monthserializer with fields cityname and year, month which are not present in the model
# Name -----> MonthSerializer
class MonthSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(max_length=50, write_only=True)
    year = serializers.CharField(max_length=50, write_only=True)
    month = serializers.CharField(max_length=50, write_only=True)
    date = serializers.DateField(format="%d/%m/%Y", read_only=True)

    # if validation requred
    # def validate(self, data):
    #     city_name = data.get('city_name')
    #     year = data.get('year')
    #     month = data.get('month')
    #     holiday = None
    #     if city_name and year and month:
    #         holiday = Holiday.objects.filter(city_name__iexact=city_name, date__year=year, date__month=month)
    #
    #         # holiday = get_object_or_404(Holiday, city_name=city_name, date__year=year, date__month=month)
    #         if not holiday:
    #             msg = 'No holiday found'
    #             raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = 'Invalid inputs.'
    #         raise serializers.ValidationError(msg, code='authorization')
    #
    #     data['holiday'] = holiday
    #     return data

    class Meta:
        model = Holiday
        fields = '__all__'
        read_only_fields = ["date", "holidayName", ]  # to skip providing data as request for this two fields


# dailyserializer with date field
# Name -----> DailySerializer
class DailySerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(max_length=50, write_only=True)
    date = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Holiday
        fields = '__all__'
        read_only_fields = ["date", "holidayName"]


# adminloginserializer with adminemail and password
# Name -----> AdminLoginSerializer
class AdminLoginSerializer(serializers.ModelSerializer):
    admin_email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, data):
        admin_email = data.get('admin_email')
        password = data.get('password')
        user = None
        if admin_email and password:
            # user = authenticate(user_email=user_email, password=password)  # use this if you have hashed the password during registration
            # user = self.authenticate(user_email=user_email, password=password)
            user = get_object_or_404(Admin, admin_email=admin_email, password=password)  # additional import
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Email not provided".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

    class Meta:
        model = Admin
        fields = ['admin_email', 'password']
