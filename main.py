"""
Monte Carlo simulation on the number of prevented COVID-19 cases because of established testing centers
Sunanda Dadi (sdadi2)
IS 597 PRO FA20
"""

import pandas as pd
import numpy as np
import random


def load_clean_data(file_name):
    """
    The function loads COVID 19 Case Surveillance data for the month of Nov'2020.
    It fetches data of only asymptotic cases.
    :param file_name: String value of the filename (expected to be in the same folder as this file)
    @return: dataframe containing the surveillance data
    """
    df = pd.read_csv(file_name)
    df = df[df['onset_dt'].isnull()]
    return df

def fetch_total_test_cases(data):
    """
    The function fetches the number of people who visited the test center.
    :param data: Dataframe of the loaded dataset
    @return: Total number of people tested for COVID 19
    """
    # TODO: Add doctests
    return data.shape[0]

def fetch_positive_cases(data):
    """
    The function filters COVID 19 Cases with current status as Laboratory-confirmed case.
    :param data: Dataframe of the loaded dataset
    @return: Total number of people diagnosed as COVID 19 positive
    """
    # TODO: Add doctests
    return data.query('current_status == "Laboratory-confirmed case"').shape[0]

def fetch_probability_of_testing_positive(total_test_cases, positive_cases):
    """
    The function filters COVID 19 Cases with current status as Laboratory-confirmed case.
    :param total_test_cases: Total number of people tested for COVID 19
    :param positive_cases: Total number of people diagnosed as COVID 19 positive
    @return: The probability of people getting diagnosed as COVID 19 positive
    """
    # TODO: Add doctests
    return (positive_cases/total_test_cases)*100

def simulate_transmitted_cases(max_spread_count, max_days_as_carrier, positive_cases, probability_of_testing_positive):
    """
    The function calculates the number of individuals COVID 19 is transmitted to, because of comming in contact
    with an infected person (unware of his infection)
    :param spread_count_per_individual_per_day: Randomized variable 1 - Total number of individuals an
        infected person is likely to spread per day being unaware of their infection
    :param days_individual_acts_as_carrier: Randomized variable 2 - Total number of days an
        infected person is likely to act as an active carrier of the virus
    :param positive_cases: Total number of people diagnosed as COVID 19 positive
    :param probability_of_testing_positive: The probability of people getting diagnosed as COVID 19 positive
    @return: Total number of non infectedpeople infected people are likely to spread the virus and diagnosed COVID 19 positive
    """
    # TODO: Add doctests
    # TODO: Try to generate random spreads for each day

    # Generating a random sample of the number of people each person may spread the virus
    random_spread_count_sample = random.choices(range(0, max_spread_count + 1), k=positive_cases)

    # Generating a random sample of the number of days each person can act as a carrier
    random_days_as_carrier_sample = random.choices(range(0, max_days_as_carrier + 1),k=positive_cases)

    # Created a dataframe for faster calculation, given the enormous size of the data
    df = pd.DataFrame(
            {
                'Spread Count': random_spread_count_sample,
                'Days as carrier': random_days_as_carrier_sample
            }
        )

    # Total new cases is the number of people an infected person spreads the virus
    # for the days they act as carriers of the virus
    df['New Cases'] = df['Spread Count'] * df['Days as carrier']
    total_new_cases = df['New Cases'].sum()

    # The probability of getting tested as COVID 19 positive w.r.t to the above calculated probability
    # for the given dataset
    new_positive_cases = int(total_new_cases * probability_of_testing_positive)

    return new_positive_cases

def calculate_rate_of_growth(positive_cases, simulated_new_positive_cases):
    """
    The function calculates the rate of growth in the number of positive COVID 19 cases
    :param positive_cases: Total number of people diagnosed as COVID 19 positive
    :param simulated_new_positive_cases: Total number of non infected people infected people are likely
        to spread the virus and diagnosed COVID 19 positive
    @return: Total rate of growth in the number of cases
    """
    # TODO: Add doctests
    return ((simulated_new_positive_cases - positive_cases)/positive_cases)*100

if __name__ == '__main__':
    # Randomized variable 1: Total number of individuals an infected person is likely to spread per day being unaware of their infection
    max_spread_count_per_individual_per_day = 3
    # Randomized variable 2: Total number of days an infected person is likely to act as an active carrier of the virus
    max_days_individual_acts_as_carrier = 7

    surveillance_data_file_name = 'COVID-19_Case_Surveillance_Public_Use_Data.csv'
    surveillance_data = load_clean_data(surveillance_data_file_name)
    total_test_cases = fetch_total_test_cases(surveillance_data)
    positive_cases = fetch_positive_cases(surveillance_data)
    probability_of_testing_positive = fetch_probability_of_testing_positive(total_test_cases, positive_cases)
    print("probability_of_testing_positive", probability_of_testing_positive)

    simulated_new_positive_cases = simulate_transmitted_cases(max_spread_count_per_individual_per_day, \
            max_days_individual_acts_as_carrier, \
            positive_cases, \
            probability_of_testing_positive
        )
    rate_of_growth = calculate_rate_of_growth(positive_cases, simulated_new_positive_cases)
    print("rate_of_growth", rate_of_growth)
    # TODO: Add visualizations
    # TODO: Read surveillance_data via API (unable to push on git due to large size)
