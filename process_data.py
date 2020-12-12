# Pre processing data to fetch filtered data of required columns
import pandas as pd

# COVID-19_Case_Surveillance_Public_Use_Data_All_Months.csv contains data from CDC where onset_dt is not registered
df = pd.read_csv('COVID-19_Case_Surveillance_Public_Use_Data_All_Months.csv', \
    usecols = ['cdc_report_dt', 'onset_dt','current_status', 'sex', 'age_group'])
df = df[df['onset_dt'].isnull()]

df['month'] = pd.DatetimeIndex(df['cdc_report_dt']).month
months = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov'
    }

# Building independent files for each month
columns = ['current_status', 'sex', 'age_group']
for key, val in months.items():
    temp = df.query('month=='+str(key))
    temp.to_csv(val+'_cases.csv' , columns = columns, index = False)
