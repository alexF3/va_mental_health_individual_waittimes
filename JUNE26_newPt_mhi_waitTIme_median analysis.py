import pandas as pd
import datetime as dt
"""
Author: Alex Rich
Date: 24 Jun 2026
Objective: Walk through median and mean analysis of New Patient MENTAL HEALTH INDIVIDUAL wait time data with a focus
on june 2026 
Input: csv of VA Access to Care wait times from https://github.com/alexF3/va_mental_health_individual_waittimes
Output: methodology and printouts of each result
"""
# Load the github csv of MHI wait time data
df = pd.read_parquet('20260622_VAaccessToCare_NewPt_MHI_wait_times.parquet')
df.ReportDate = pd.to_datetime(df.ReportDate)

# Deduplicate: where a facility has more than one row for the same date, keep the lower NewPatients value
df = df.groupby(
    ['facility_id', 'ReportDate', 'AppointmentType', 'VA Facility Location', 'state'],
    as_index=False, dropna=False
).agg(

    NewPatients=('NewPatients', 'min')
)

print('__________________')
print('1 - 22 June analysis')
print('__________________')
print('')
print('Analysis conducted 24 June 2026 using data that spans 25 Oct 2025 - 22 Jun 2026')
print("Analysis of VA-reported New Patient MENTAL HEALTH INDIVIDUAL wait times in June 2026 drawn from the VA Access to Care public site")
print('')
print("To establish the most conservative apporoach, this analysis uses only the lowest NewPatient wait time reported by a facility in a day in any instance in which multiple NewPatient values were recorded in a single day.")
print('')
# Count the number of facilities that reported at least one real MHI wait time in the dataset
print(f'{len(df.dropna(subset=["NewPatients"]).facility_id.unique())} total facilities that reported at least one real number new patient MENTAL HEALTH INDIVIDUAL wait time since 25 Oct 2025')
tot_mhi_reporters = len(df.dropna(subset=['NewPatients']).facility_id.unique())
# 957 facilities reported non-null NewPatients wait time for MENTAL HEALTH INDIVIDUAL appointments at least once since 25 Oct 25
# Filter for june
df = df[(df.ReportDate>=dt.datetime(2026,6,1,0,0))]
# drop the nulls (and thus drop all facilities that were null for all of june)
df = df[~df.NewPatients.isnull()]

# Make a new dataframe of facility averages for june (Note: those that reported null New Patient wait times for all of june will be missing)
june_avg = pd.DataFrame(df.groupby('facility_id').NewPatients.mean()).reset_index()
# Make a new dataframe of facility MEDIANS for june (Note: those that reported null New Patient wait times for all of june will be missing)
june_median = pd.DataFrame(df.groupby('facility_id').NewPatients.median()).reset_index()

# How many facilities failed to report real number new pt wait times in june but had done so before?
print(f'{tot_mhi_reporters - len(june_median.facility_id.unique())} facilities reported real number New Patient MENTAL HEALTH INDIVIDUAL wait times at least once since 25 Oct 2025 but failed to report real numbers in june')
# 122
print(f'The {tot_mhi_reporters - len(june_avg.facility_id.unique())} facilities that did not report real number New Patient MHI wait times in june, but did so at least once since October bear further analysis in the future.')

print('')
print(f'{len(june_avg.facility_id.unique())} unique facilities that reported at least one real number wait time for new patient MENTAL HEALTH INDIVIDUAL wait times in june')
# This yields 835 facilities with real wait times to average, which means that 122 of the 957 above were null for all of june

print('')



# Count and print out the buckets
print('Median analysis:')
print(f'{len(june_median[june_median.NewPatients<=20])} facilities at or under 20 days')
# 311

print(f'{len(june_median[(june_median.NewPatients > 20) & (june_median.NewPatients <= 30)])} facilities over 20 days and less than or equal to 30 days')
# 165

print(f'{len(june_median[(june_median.NewPatients>30) & (june_median.NewPatients<=60)])} facilities over 30 days and less than or equal to 60 days')
# 248

print(f'{len(june_median[(june_median.NewPatients>60) & (june_median.NewPatients<=90)])} facilities over 60 days and less than or equal to 90 days')
# 79 

print(f'{len(june_median[(june_median.NewPatients>90)])} facilities over 90 days')
# 32

print(f'{round(100*len(june_median[june_median.NewPatients>20])/(len(june_median)),1)}% of the {len(june_median)} facilities that reported real number New Patient MENTAL HEALTH INDIVIDUAL wait times in june had median reported wait time values over the 20-day target wait time')

print('')

# Count and print out the buckets
print('Average analysis:')
print(f'{len(june_avg[june_avg.NewPatients<=20])} facilities at or under 20 days')
# 291

print(f'{len(june_avg[(june_avg.NewPatients > 20) & (june_avg.NewPatients <= 30)])} facilities over 20 days and less than or equal to 30 days')
# 175

print(f'{len(june_avg[(june_avg.NewPatients>30) & (june_avg.NewPatients<=60)])} facilities over 30 days and less than or equal to 60 days')
# 253

print(f'{len(june_avg[(june_avg.NewPatients>60) & (june_avg.NewPatients<=90)])} facilities over 60 days and less than or equal to 90 days')
# 86

print(f'{len(june_avg[(june_avg.NewPatients>90)])} facilities over 90 days')
# 30


print(f'{round(100*len(june_avg[june_avg.NewPatients>20])/(len(june_avg)),1)}% of the {len(june_avg)} facilities that reported real number New Patient MENTAL HEALTH INDIVIDUAL wait times in june had average reported wait time values over the 20-day target wait time')


print('')

over_20 = len(df[(df.NewPatients > 20) & (~df.NewPatients.isnull())])
total_reported = len(df[~df.NewPatients.isnull()])
pct = int(round(100 * over_20 / total_reported, 0))
print(f'{pct}% of the real number New Patient MHI wait times reported by the VA on its own website in june were over the VA\'s 20-day target.')
