import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


# create the function to display the city matching the city with the character which the user typed
def get_city():

    while True:
            city = input('Would you like to select data for Chicago(type \'c\'), New York (type \'n\'), or Washington(type \'w\')? ').lower().strip()

            cityList = ['c', 'n', 'w']

            if city not in cityList:
                print('Invalid input, please try it again.')
            else:
                break
    if city == 'c':
        city = 'chicago'
    elif city == 'n':
        city = 'new york'
    else:
        city = 'washington'

    return city


# create the function to display the month matching the month with the number 0 -6 which the user typed
def get_month():

    while True:
    #month = str(input('Which month - All(type '0'), January(type '1'), February(type '2'), March(type '3'), April(type '4'), May(type '5'), June(type '6')? ')).strip()

        month = input('Which month - All(type \'0\'), January(type \'1\'), February(type \'2\'), March(type \'3\'), April(type \'4\'), May(type \'5\'), June(type \'6\')? ').strip()

        month_list = ['0', '1', '2', '3', '4', '5', '6']
        if month not in month_list:
            print('Invalid input, please try it again.')
        else:
            break
    if month == '0':
        month = 'all'
    elif month == '1':
        month = 'january'
    elif month == '2':
        month = 'february'
    elif month == '3':
        month = 'march'
    elif month == '4':
        month = 'april'
    elif month == '5':
        month = 'may'
    else:
        month = 'june'

    return month


# create the function to display the day matching the day with the number 0 -7 which the user typed
def get_day():
    while True:
        day = input('Which day - All(type \'0\'), Monday(type: \'1\'), Tuesday(type: \'2\'), Wednesday(type: \'3\'), Thursday(type: \'4\'), Friday(type: \'5\'), Saturday(type: \'6\'), Sunday(type: \'7\')? ').strip()

        day_list = ['0', '1', '2', '3', '4', '5', '6', '7']
        if day not in day_list:
            print('Invalid input, please try it again.')
        else:
            break

    if day == '0':
        day = 'all'
    elif day == '1':
        day = 'monday'
    elif day == '2':
        day = 'tuesday'
    elif day == '3':
        day = 'wednesday'
    elif day == '4':
        day = 'thursday'
    elif day == '5':
        day = 'friday'
    elif day == '6':
        day = 'saturday'
    else:
        day = 'sunday'

    return day


# create this function to ask user to specify a city, month, and day to analyze.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()
    print()

    # get user input for month (all, january, february, ... , june)
    month = get_month()
    print()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

    print('-'*40)

    return city, month, day


# create this function to loads data for the specified city and filters by month and day if applicable.
def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


# create a method to ask to view row of data
def view_city_data(df, city):

    # start by viewing the first five rows of the dataset
    city_data = input('\nWould you like to view the raw data for selected city \'{}\'? (Type \'y\' or \'n\') '.format(city.title())).lower().strip()

    c = 0         # set count to zero
    while True:
        if city_data == 'y':

            c += 1

            print('\nThe 5 {} rows of data for \'{}\': \n'.format(top_some(c), city.title()))
            print(df.iloc[(c - 1)*5 : c*5])

            # want to see 5 more row of data
            city_data = input('Would you like to see 5 more rows of data for \'{}\'? (Type \'y\' or \'n\' ) '.format(city.title())).lower().strip()

        elif city_data == 'n':       # don't want to see more row of data
            print('No more rows of data to be displayed')
            break
        else:           # repeatly ask for enter correct character if entering wrong one
            city_data = input('Type \'y\' or \'n\' to view rows of data for \'{}\': '.format(city.title())).lower().strip()

    return city_data


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datatime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract day_of_week from the Start Time column to create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # display the most common month:  (from 1 to 12 replaced with work month)
    print('Most popular month:', replace_num_month(df['month'].mode()[0]))

    # display the most common day of week
    print('Most popular day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most popular start hours: %s.' % df['hour'].mode()[0])

    # count total numbers
    print('Count: {}'.format(df['hour'].value_counts().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# create this function to replace number of month to word of month (because the input is in number of month)
def replace_num_month(month):

    if month == 0:
        month = 'All'
    elif month == 1:
        month = 'January'
    elif month == 2:
        month = 'February'
    elif month == 3:
        month = 'March'
    elif month == 4:
        month = 'April'
    elif month == 5:
        month = 'May'
    elif month == 6:
        month = 'June'

    return month


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Start station: {}.'.format(df['Start Station'].mode()[0]))

    # count total numbers
    print('Count: {}'.format(df['Start Station'].value_counts().max()))

    # display most commonly used end station
    print('End station: {}.'.format(df['End Station'].mode()[0]))

    # count total numbers
    print('Count: {}'.format(df['End Station'].value_counts().max()))

    # display most frequent combination of start station and end station trip
    df['combine_trip'] = '\"' + df['Start Station'] + '\"' + ' and ' + '\"' + df['End Station'] + '\"'
    print('Combination of start station and end station: {}.'.format(df['combine_trip'].mode()[0]))

    # count total numbers
    print('Count: {}'.format(df['combine_trip'].value_counts().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):        # test working
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total duration: {} seconds.'.format(df['Trip Duration'].sum()))

    # count total numbers
    print('Count: {}'.format(df['Trip Duration'].count()))

    # display mean travel time
    print('Average duration: {} seconds.'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Count user types:')
    print(count_user_types)

    # Display 'None' for no 'Gender' title in the file
    if 'Gender' not in df.columns:
        print('\nCount gender: None')

    # Display 'Gender' value counts if finding it in the titile columns of the file
    else:
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print('\nCount gender:')
        print(count_gender)

    # Display 'None' for no 'Birth Year' title in the file
    if 'Birth Year' not in df.columns:
        print('\nThe earliest year of birth: None')
        print('The most recent year of birth: None')
        print('The most common year of birth: None')

    # Display 'Birth Year' value counts if finding it in the titile columns of the file
    else:
        # Display earliest, most recent, and most common year of birth
        print('\nThe earliest year of birth: ', df['Birth Year'].min())
        print('The most recent year of birth: ', df['Birth Year'].max())
        print('The most common year of birth: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# create the function to disply either 'top' or 'some' word
def top_some(count):

    top_some = ''
    if count == 1:
        top_some = 'top'
    else:
        top_some = 'more'
    return top_some


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # check the data entered correct or not
        print('\nThe data you selected:')
        print('City: {}      Month: {}       Day: {}'.format(city, month, day))

        while True:
            check_data = input('\nIf data is correct, please continue(type \'c\'), otherwise go back to re-enter the data(type \'r\'): ').lower().strip()

            if check_data == 'c':
                break
            elif check_data == 'r':
                main()
            else:
                print('Invalid input, please try it again.')

        # call view_city_data to view the city data for the selected city
        view_city_data(df, city)

        # print out selected city, month and day on the output
        print()
        print('             CITY: {}'.format(city.title()))
        print('Filter - Month: {}      Day: {}'.format(month.title(), day.title()))

        # call these functions to display the information accordingly to
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # ask to choose either restart or exit the program
        restart_quit = input('\nWould you like to restart (type \'r\') or quit the program (type any character)? ').lower().strip()

        # if user type not 'r' then the program is going to quit
        if restart_quit != 'r':
            print("Thanks for using \'Bikeshare\'. You have a good day.")
            exit()
        print()     # print one line space

        # else if user type 'r' then the program is going back to restart the program
        main()

if __name__ == "__main__":
        main()
