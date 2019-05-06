import time
import pandas as pd
import numpy as np

""" The pupose of Bikeshare.py is to use data to analyse bikeshare trends in the Chicago, New York, and Washington"""

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city they want to investigate
    cities = ['Chicago', 'Washington', 'New York']
    city = input(
        'Would you like to see data from Chicago, New York, or Washington?\n').title()
    while city not in cities:
        print('That\'s not a valid response\n')
        city = input('Chicago, New York, or Washington?\n').title()


    # get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = input('Which month? (all, january, february, ... , june) \n').lower()
    while month not in months:
        month = input('Enter a valid month\n').lower()

    #  get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = input('Which day?\n').lower()
    while day not in days:
        day = input('Enter a valid day of the week\n').lower()

    print('-'*40)
    return (city, month, day)


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from Start Time
    df['month'] = df['Start Time'].dt.month
    # extract day of week from Start Time
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # extract hour from Start Time
    df['hour'] = df['Start Time'].dt.hour
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', df['month'].mode()[0])
    # display the most common day of week
    print('Most common day of week:',df['day_of_week'].mode()[0])
    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    print('Most common start hour:',df['hour'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station:',df['Start Station'].mode()[0])
    # display most commonly used end station
    print('Most common end station:',df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    df['start-end station'] = df['Start Station']+' and '+df['End Station']
    print('Most common combination of start station and end station trip:',df['start-end station'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
   
    print('The total travel time is:',df['Trip Duration'].sum(),'seconds')
    # display mean travel time
    print('The average travel time is:',df['Trip Duration'].mean(), 'seconds')
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)
    # Display counts of gender
    if city == 'Washington':
        print('We don\'t have gender or birth year data for Washington')
    else:
        gender = df['Gender'].value_counts()
        print(gender)
    # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('the earliest year of birth is {}, the most recent year of birth is {}, and the most common year of birth is {}.'.format(earliest, most_recent, most_common))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Offer to display 5 rows of raw data until user says no"""
    i=0
    while True:
        user_input = input('Would you like to see 5 rows of raw data?\n').lower()
        if user_input == "yes":
            print(df.iloc[i:i+5])
            i = i+5
            continue
        else:
            break
        
        
  
   

            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city, month, day)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
