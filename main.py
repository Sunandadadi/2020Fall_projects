"""
Monte Carlo simulation on the number of prevented COVID-19 cases because of established testing centers
Sunanda Dadi (sdadi2)
IS 597 PRO FA20
"""

from sklearn import preprocessing
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random


def load_clean_data(file_name):
    """
    This function loads COVID 19 Case Surveillance data for different months
    It fetches data of only asymptotic cases.
    :param file_name: String value of the filename (expected to be in the same folder as this file)
    @return: dataframe containing the surveillance data
    """
    df = pd.read_csv(file_name)
    return df


def fetch_total_test_cases(data):
    """
    This function fetches the number of people who visited the test center from the loaded data frame.
    :param data: Dataframe of the loaded dataset
    @return: Total number of people tested for COVID 19

    >>> data = pd.DataFrame({'c1': [1, 2, 3], 'c2': ['a', 'b', 'c']})
    >>> fetch_total_test_cases(data)
    3
    >>> data = pd.DataFrame({'c1': [1], 'c2': [3]})
    >>> fetch_total_test_cases(data)
    1
    >>> data = pd.DataFrame({'c1': [], 'c2': []})
    >>> fetch_total_test_cases(data)
    0
    """
    return data.shape[0]


def fetch_positive_cases(data):
    """
    This function filters the loaded data to fetch data containing current status as Laboratory-confirmed case.
    :param data: Dataframe of the loaded dataset
    @return: Total number of people diagnosed as COVID 19 positive

    >>> data = pd.DataFrame({'current_status': ['Laboratory-confirmed case', 'Pending', 'Laboratory-confirmed case'], 'c2': ['a', 'b', 'c']})
    >>> fetch_positive_cases(data)
    2
    >>> data = pd.DataFrame({'current_status': ['Pending', 'Pending', 'Approved'], 'c2': ['a', 'b', 'c']})
    >>> fetch_positive_cases(data)
    0
    """
    return data.query('current_status == "Laboratory-confirmed case"').shape[0]


def fetch_probability_of_testing_positive(total_test_cases, positive_cases):
    """
    This function calculates the probability of getting tested COVID 19 positive based on the loaded data
    :param total_test_cases: Total number of people tested for COVID 19
    :param positive_cases: Total number of people diagnosed as COVID 19 positive
    @return: The probability of people getting diagnosed as COVID 19 positive

    >>> positive_cases, total_test_cases = 10, 234
    >>> fetch_probability_of_testing_positive(total_test_cases, positive_cases)
    0.04
    >>> positive_cases, total_test_cases = 234, 14
    >>> fetch_probability_of_testing_positive(total_test_cases, positive_cases)
    16.71
    >>> positive_cases, total_test_cases = 234, 0
    >>> fetch_probability_of_testing_positive(total_test_cases, positive_cases)
    Oops! Cannot divide by zero
    """
    try:
        return round(positive_cases/total_test_cases, 2)
    except ZeroDivisionError:
        print('Oops! Cannot divide by zero')
        return


def fetch_random_samples(max_spread_count, max_days_as_carrier, positive_cases):
    """
    The function constructs a randomly sampled data frame of spread counts and the number days of a person acting as a carrier
    :param max_spread_count: Randomized variable 1 - Total number of individuals an
        infected person is likely to spread per day being unaware of their infection
    :param max_days_as_carrier: Randomized variable 2 - Total number of days an
        infected person is likely to act as an active carrier of the virus
    :param positive_cases: Total number of people diagnosed as COVID 19 positive
    @return: Data frame of of randomly generated data for the columns "Spread Count" and "Days as carrier"
    """
    # Generating a random sample of the number of people each person may spread the virus
    random_spread_count_sample = random.choices(range(0, max_spread_count + 1), k=positive_cases)

    # Generating a random sample of the number of days each person can act as a carrier
    random_days_as_carrier_sample = random.choices(range(0, max_days_as_carrier + 1), k=positive_cases)

    # Created a data frame for faster calculation, given the enormous size of the data
    df = pd.DataFrame(
        {
            'Spread Count': random_spread_count_sample,
            'Days as carrier': random_days_as_carrier_sample
        }
    )
    return df


def simulate_transmitted_cases(df, probability_of_testing_positive):
    """
    This function calculates the number of individuals COVID 19 is transmitted to, because of comming in contact
    with an infected person (unware of their infection)
    :param df: DataFrame containing a random spread count sample and a random days acting as carrier
    :param probability_of_testing_positive: The probability of people getting diagnosed as COVID 19 positive
    @return: Total number of new infected people that are likely to spread the virus and diagnosed COVID 19 positive

    >>> df = pd.DataFrame({'Spread Count': [1, 2, 3], 'Days as carrier': [1, 1, 3]})
    >>> simulate_transmitted_cases(df, 1.0)
    12
    >>> df = pd.DataFrame({'Spread Count': [3, 4, 10], 'Days as carrier': [3, 0, 10]})
    >>> simulate_transmitted_cases(df, 0.5)
    54
    """
    # Total new cases is the number of people an infected person spreads the virus
    # for the days they act as carriers of the virus
    df['New Cases'] = df['Spread Count'] * df['Days as carrier']
    total_new_cases = df['New Cases'].sum()

    # The probability of getting tested as COVID 19 positive w.r.t to the above calculated probability
    # for the given dataset
    return int(total_new_cases * probability_of_testing_positive)


def calculate_rate_of_growth(positive_cases, new_positive_cases):
    """
    The function calculates the rate of growth in the number of positive COVID 19 cases
    :param positive_cases: Total number of people diagnosed as COVID 19 positive
    :param new_positive_cases: Total number of non infected people infected people are likely
        to spread the virus and diagnosed COVID 19 positive
    @return: Total rate of growth in the number of cases

    >>> positive_cases, new_positive_cases = 100, 3
    >>> calculate_rate_of_growth(positive_cases, new_positive_cases)
    -97.0
    >>> positive_cases, new_positive_cases = 0, 10
    >>> calculate_rate_of_growth(positive_cases, new_positive_cases)
    Oops! Cannot divide by zero
    >>> positive_cases, new_positive_cases = 10, 10
    >>> calculate_rate_of_growth(positive_cases, new_positive_cases)
    0.0
    >>> positive_cases, new_positive_cases = 10, 20
    >>> calculate_rate_of_growth(positive_cases, new_positive_cases)
    100.0
    """
    try:
        return round(((new_positive_cases - positive_cases)/positive_cases)*100, 2)
    except ZeroDivisionError:
        print('Oops! Cannot divide by zero')
        return


def run_simulation(max_spread_count_per_individual_per_day, max_days_individual_acts_as_carrier, simulation_data, curr_month, next_month):
    """
    This is the starting function that runs the simulation
    :param max_spread_count_per_individual_per_day: Randomized variable 1
    :param max_days_individual_acts_as_carrier: Randomized variable 2
    :param simulation_data: A dictionary containing various data points(like total test cases, positive cases, simulated new positive cases etc) for each month.
        These are generated from the csv files for each month and using Monte Carlo Simulation to get new cases
    :param curr_month: Current month for which data is loaded
    :param next_month: Next month to which new cases are forwarded
    @return: None Type
    """
    surveillance_data_file_name = curr_month + '_cases.csv'

    surveillance_data = load_clean_data(surveillance_data_file_name)
    simulation_data[curr_month]['total_test_cases'] = fetch_total_test_cases(surveillance_data)
    simulation_data[curr_month]['positive_cases'] = fetch_positive_cases(surveillance_data)
    probability_of_testing_positive = fetch_probability_of_testing_positive(\
                                            simulation_data[curr_month]['total_test_cases'], \
                                            simulation_data[curr_month]['positive_cases']
                                        )
    simulation_data[curr_month]['probability_of_testing_positive'] = probability_of_testing_positive
    print("probability_of_testing_positive ",curr_month, "is: ", probability_of_testing_positive)

    df = fetch_random_samples(max_spread_count_per_individual_per_day, \
                              max_days_individual_acts_as_carrier, \
                              simulation_data[curr_month]['positive_cases']
                              )

    simulated_new_positive_cases = simulate_transmitted_cases(df, probability_of_testing_positive)

    simulation_data[next_month]['simulated_new_positive_cases'] = simulated_new_positive_cases
    simulation_data[next_month]['expected_rate_of_growth'] = calculate_rate_of_growth( \
                                                                simulation_data[curr_month]['positive_cases'], \
                                                                simulated_new_positive_cases \
                                                            )
    print("rate_of_growth in ",next_month, "is: ", simulation_data[next_month]['expected_rate_of_growth'])
    return


def calculate_for_actual_growth_rate(simulated_data, months):
    """
    This function fetches the actual rate of growth in the number of cases that is recorded in the simulated data dictionary
    :param simulated_data: A dictionary containing various data points(like total test cases, positive cases, simulated new positive cases etc) for each month.
        These are generated from the csv files for each month and using Monte Carlo Simulation to get new cases
    :param months: A list containing months of the year
    @return: None Type
    """
    for i in range(1, len(months) - 1):
        simulated_data[months[i]]['actual_rate_of_growth'] = calculate_rate_of_growth( \
                                                                simulated_data[months[i-1]]['positive_cases'], \
                                                                simulated_data[months[i]]['positive_cases'] \
                                                            )
    return


def plot_rate_of_growth(months, expected_rate_of_growth, actual_rate_of_growth):
    """
    This function generates a matplotlib plot to compare expected rate of growth with the actual rate of growth
    :param expected_rate_of_growth: The expected rate of growth in the number of positive cases (generated from the simulation)
    :param actual_rate_of_growth: The actual rate of growth in the number of positive cases (calculated from the data source)
    :param months: A list containing months of the year
    @return: None Type
    """
    plt.plot(months, expected_rate_of_growth, label='Estimated rate of growth', color='red', marker='o')
    plt.plot(months, actual_rate_of_growth, label='Actual rate of growth', color='black', marker='o')
    plt.title('Monthly growth rate of positives case')
    plt.xlabel('Month')
    plt.ylabel('Normalized rate of growth')
    plt.legend(loc="upper right")
    plt.show()


def plot_new_cases(months, simulated_new_cases, actual_new_cases):
    """
    This function generates a matplotlib plot to compare expected new cases with the actual new cases
    :param simulated_new_cases: The expected number of new positive cases (generated from the simulation)
    :param actual_new_cases: The actual number of new positive cases (calculated from the data source)
    :param months: A list containing months of the year
    @return: None Type
    """
    plt.plot(months, simulated_new_cases, label='Estimated new cases', color='red', marker='o')
    plt.plot(months, actual_new_cases, label='Actual new cases', color='black', marker='o')
    plt.title('Monthly growth of positives case')
    plt.xlabel('Month')
    plt.ylabel('Normalized New cases')
    plt.legend(loc="upper left")
    plt.show()


def fetch_normalize_data(data):
    """
    This function normalizes a list of data values
    :param data: list of values that need to be normalized
    @return: normalized data

    >>> data = [1, 2, 3]
    >>> fetch_normalize_data(data)
    array([0.26726124, 0.53452248, 0.80178373])
    >>> data = [1, 1, 1]
    >>> fetch_normalize_data(data)
    array([0.57735027, 0.57735027, 0.57735027])
    """
    data = np.array(data)
    return preprocessing.normalize([data])[0]


def plot_visualizations(data):
    """
    This function generates differnt visualizations for this project
    :param data: A dictionary containing calculated values
    @return: None
    """
    plot_rate_of_growth(months, \
        fetch_normalize_data(list(map(lambda x: simulation_data[x].get('expected_rate_of_growth', 0), simulation_data))), \
        fetch_normalize_data(list(map(lambda x: simulation_data[x].get('actual_rate_of_growth', 0), simulation_data))) \
    )

    plot_new_cases(months, \
        list(map(lambda x: simulation_data[x].get('simulated_new_positive_cases', None), simulation_data)), \
        list(map(lambda x: simulation_data[x].get('positive_cases', None), simulation_data)) \
    )
    return


if __name__ == '__main__':
    # Randomized variable 1: Total number of individuals an infected person is likely to spread per day being unaware of their infection
    max_spread_count_per_individual_per_day = 3
    # Randomized variable 2: Total number of days an infected person is likely to act as an active carrier of the virus
    max_days_individual_acts_as_carrier = 7
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    simulation_data = {}
    list(map(lambda x: simulation_data.update({x: {}}), months))

    for i in range(0, len(months)-1):
        run_simulation(
                        max_spread_count_per_individual_per_day, \
                        max_days_individual_acts_as_carrier, \
                        simulation_data, \
                        months[i],
                        months[i+1]
                    )
    calculate_for_actual_growth_rate(simulation_data, months)
    plot_visualizations(simulation_data)
