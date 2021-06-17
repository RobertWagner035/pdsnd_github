import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user if he first wants to see some lines of rwa data and if so, pulls it from the chicago.csv file.
    Then asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for 20 lines of raw data and 20 more lines any time, the user wants to see more raw data
    raw_data = input('\nWould you like to see 20 lines of raw data? Please insert yes or no:\n').lower()
    #check if user inserts an invalid value
    while raw_data != 'yes' and raw_data != 'no':
        raw_data = input('\nPlease insert only yes or no:\n').lower()

    #if user inserts "yes", 20 lines of raw data are shown. inserting "no" leads directly to line 38
    i=0
    while raw_data == 'yes':
        i += 1
        raw = pd.read_csv('./chicago.csv')
        print(raw.head(i*20))
        raw_data = input('\nWould you like to see 5 more lines of raw data? Please insert yes or no:\n')
        while raw_data != 'yes' and raw_data != 'no':
            raw_data = input('\nPlease insert yes or no. Would you like to see 5 more lines of raw data?\n').lower()

    # get user input for city (chicago, new york city, washington).
    city = input('\nThank you! Which city do you now want to see statistics from: Chicago, Washington or New York? \nPlease insert the city:\n').lower()
    #check if user inserts an invalid value
    while city != 'chicago' and city != 'new york' and city != 'washington':
        city = input('\nSorry, your input is not valid. Please insert one of the three cities Chicago, Washington or New York and care for spelling:\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nWhat month are you interested in? We have data for months January to June. Do you want to see data from all months or from a specific month? \nPlease insert a month:\n').lower()
    #check if user inserts an invalid value
    while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june' and month != 'all':
        month = input('\nSorry, your input is not valid. Please insert "all" or a specific month between January and June and care for spelling:\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWhat day are you interested in? Do you want to see data from all weekdays or from a specific day of the week? \nPlease insert a weekday:\n').lower()
    #check if user inserts an invalid value
    while day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday' and day != 'all':
        day = input('\nSorry, your input is not valid. Please insert "all" or a specific weekday like Monday and care for spelling:\n').lower()

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
    # load data for selected city
    df = pd.read_csv(CITY_DATA[city])

    #convert start time and end time to endtime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter for month
    if month != 'all':
        # using month indices via list of months to apply a filter
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter for weekday
    if day != 'all':
        df = df[df['day of week'] == day.title()]

    print('-'*40)
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for your selection of month(s)({}) and day(s)({})...\n'.format(month, day))
    start_time = time.time()



    # display most common month only, if the user didn't filter for a specific month
    if month == 'all':
        most_common_month = df['month'].mode()[0]

        # getting the name of a month
        if most_common_month == 1:
            month_name = "January"
        elif most_common_month == 2:
            month_name = "February"
        elif most_common_month == 3:
            month_name = "March"
        elif most_common_month == 4:
            month_name = "April"
        elif most_common_month == 5:
            month_name = "May"
        elif most_common_month == 6:
            month_name = "June"

        print('The most common month for bikeshares in {} was: {}.'.format(city.title(), month_name))
    else:
        print('Since you filtered for {}, no data for the most common month is displayed here! Please enter "all" in the question for months to see this data.'.format(month))

    # display the most common day of week only, if user didn't filter for a specific day
    if day == 'all':
        most_common_day = df['day of week'].mode()[0]
        print('The most common day of the week for bikeshares in {} was: {}.'.format(city.title(), most_common_day))
    else:
        print('Since you filtered for {}, no data for the most common day of the week is displayed here! Please enter "all" in the question for days to see this data.'.format(day))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    # variable to be more precise in the statement
    precision_variable = most_common_start_hour + 1
    print('The most common start hour for bikeshares in {} was between {}:00 o\'clock and {}:00 o\'clock.'.format(city.title(), most_common_start_hour, precision_variable))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip for your selection of month(s)({}) and day(s)({})...\n'.format(month, day))
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station for bikeshares in {} was: {}.'.format(city.title(), most_start_station))

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('The most common end station for bikeshares in {} was: {}.'.format(city.title(), most_end_station))

    # display most frequent combination of start station and end station trip
    df['most_frequent_combination'] = df['Start Station'] + " / " + df['End Station']
    most_frequent_combination = df['most_frequent_combination'].mode()[0]
    print('The most frequent combination of start and end station for bikeshares in {} was: {}.'.format(city.title(), most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration for your selection of month(s)({}) and day(s)({})...\n'.format(month, day))
    start_time = time.time()

    # display total travel time in hours (rounded to one decimal), therefore we need to divide the total travel time because it is stored in seconds
    total_travel_time = df['Trip Duration'].sum() / 3600
    print('\nThe total travel time for bikeshares in {} was: {} hours.'.format(city.title(), round(total_travel_time, 1)))

    # display mean travel time in minutes (rounded to one decimal), therefore we need to divide the total travel time because it is stored in seconds
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('The mean travel time for bikeshares in {} was: {} minutes.'.format(city.title(), round(mean_travel_time, 1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for your selection of month(s)({}) and day(s)({})...\n'.format(month, day))
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The following user types were bikesharing in {}:\n{}.'.format(city.title(), user_types))

    # Display counts of gender
    if city == 'washington':
        print('\nThere\'s no data available for gender in {}.'.format(city.title()))
    else:
        gender = df['Gender'].value_counts()
        print('\nThe following gender were bikesharing in {}:\n{}.'.format(city.title(), gender))

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nThere\'s no data available for year of birth in {}.'.format(city.title()))
    else:
        year_of_birth_max = df['Birth Year'].max()
        year_of_birth_min = df['Birth Year'].min()
        year_of_birth_most = df['Birth Year'].mode()[0]
        print('\nThe youngest person using bikesharing in {} was born in the year: {}.'.format(city.title(), int(year_of_birth_max)))
        print('The oldest person using bikesharing in {} was born in the year: {}.'.format(city.title(), int(year_of_birth_min)))
        print('The largest group of people using bikesharing in {} were born in the year: {}.'.format(city.title(), int(year_of_birth_most)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)

        # ask for raw data again
        raw_data = input('Would you like to see 20 lines of raw data? Please insert yes or no:\n').lower()
        #check if user inserts an invalid value
        while raw_data != 'yes' and raw_data != 'no':
            raw_data = input('\nPlease insert yes or no:\n').lower()

        #if user inserts yes, 20 lines of raw data are shown, now from the filtered city
        i=0
        while raw_data == 'yes':
            i += 1
            print(df.head(i*20))
            raw_data = input('\nWould you like to see 20 more lines of raw data from the filtered dataset? Please insert yes or no:\n')
            while raw_data != 'yes' and raw_data != 'no':
                raw_data = input('\nPlease insert yes or no. Would you like to see 20 more lines of raw data from the filtered dataset?\n').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThank you for exploring bikesharing data with us. Goodbye!\n')
            break


if __name__ == "__main__":
	main()
