import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
WEEK = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Would you like to see data for Chicago, New York, or Washington?\n")
    while True:
        if city not in CITY_DATA.keys():
            city = input("Please select valid city name [%s]\n" % ', '.join(map(str, CITY_DATA.keys())))
        if city in CITY_DATA.keys():
            break

    data_filter = input("Would you like to filter the data by month, day, or not at all (yes or no)?\n")
    while True:
        if data_filter == "yes":
            # TO DO: get user input for month (all, january, february, ... , june)
            month = input("Which month - all, January, February, March, April, May, or June?\n")
            while True:
                if month.lower() not in MONTH:
                    month = input("Please select valid month name [%s]\n" % ', '.join(map(str, MONTH)))
                if month.lower() in MONTH:
                    break

            # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
            day = input("Which day - all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
            while True:
                if day.lower() not in WEEK:
                    day = input("Please select valid day name [%s]\n" % ', '.join(map(str, WEEK)))
                if day.lower() in WEEK:
                    break
            break
        elif data_filter == "no":
            month = 'all'
            day = 'all'
            break
        else:
            data_filter = input("Incorrect input provided. Please enter yes or no\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city_csv = CITY_DATA[city]
    df = pd.read_csv(city_csv)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['start_end_station'] = df['Start Station'] + df['End Station']
    if month != 'all':
        month = MONTH.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    display_raw_data = input("Would you like to see first 5 rows of raw data?\n")
    if display_raw_data == 'yes':
        print (df[:5])
        check = input("Continue to computations? Press Enter to continue\n")
    else:
        pass
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    # TO DO: display the most common day of week
    common_week = df['day_of_week'].mode()[0]
    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(common_month)
    print(common_week)
    print(common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]


    # TO DO: display most frequent combination of start station and end station trip
    common_station_trip = df['start_end_station'].mode()[0]
    print(common_start_station)
    print(common_end_station)
    print(common_station_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    days = total_travel_time //(24 * 3600)
    total_travel_time = total_travel_time % (24*3600)
    hours = total_travel_time // 3600
    total_travel_time%= 3600
    minutes = total_travel_time //60
    total_travel_time %= 60
    seconds = total_travel_time
    print("total travel time is %d days:%d hours:%d minutes:%d seconds" % (days, hours, minutes, seconds))

    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    avg_minutes = avg_travel_time //60
    avg_travel_time %= 60
    avg_seconds = avg_travel_time
    print("average travel time is %d minutes:%d seconds" % ( avg_minutes, avg_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print(count_user_types)

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        count_gender = df['Gender'].value_counts()
        print(count_gender)
    else:
        print("Gender column not available for this city\n")
    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earlist_birthyear= df['Birth Year'].min()
        recent_birthyear= df['Birth Year'].max()
        common_birthyear= df['Birth Year'].mode()[0]
        print(earlist_birthyear)
        print(recent_birthyear)
        print(common_birthyear)
    else:
        print("Birth Year column is not available\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
