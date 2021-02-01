# Conceptual Modelling

## Questions to be Answered

1. What were the trends, in terms of the number of cases, over time? (Our aim is
obtaining profiles of individuals, by age and gender, who tested positive for
Covid-19; distinguishing between travel-related and other cases (if known);
tracking outbreaks; exploring the types and availability of testing facilities; etc.)

2. Was there any interplay between special events (e.g., Thanksgiving or Canada
Day) and the number of cases? (It should be noted that there is typically a delay
between increased social interactions and an upsurge in positive Covid-19 tests.)

3. How did lockdown measures, such as stay at home orders or school closures,
affect the number of cases? Did specific government announcements or
restrictions lead to downward trends in the number of cases? (The effectiveness
of specific government measures on the outbreak is of importance here. It should
again be noted that there is typically a delay between restrictions and a
decreased in positive Covid-19 tests.)

4. What were the trends in behaviours, in terms of the locations people visited and
the duration they stayed? Did the weather have any impact on these trends? For
instance, studies suggested that many Canadians started bicycling, walking, or
visiting parks during the summer. (This question speaks to the mapping of
potential changes in citizens’ lifestyles. Note that mobility data are available
online from e.g., the google mobility repository and that weather data may be
obtained from Environment and Climate Change Canada.) 



## Consumer Habit Fact table

### Dimensions

- Sector 


### DataSets Used 

## Lifestyle Fact table

### Dimensions

- Weather
- Public Events
- Data (Conformed)


### DataSets Used 

## Covid Related Fact table

### Grain

Per day

### Fact Table Attributes

#### Foreign KeysZZ
- DateKey (FK)

#### Facts/Measures

- Number of Cases
- Number Recovered
- total tests/test outcomes


### Dimensions 

- Date Related(Conformed)
  - Date Stamp
  - Day of the week
  - Month
  - Festivities (y/n)
- Location Dimension (Conformed)
  - Median Income
  - Population Density
  - Available Testing Locations
  - Public Health Units
- Individual Profile
  - Age Group
  - Gender
  - Case Acquisition
- Government Restrictions


### DataSets Used 

- (Status of COVID-19)[https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario]

reporting date
daily tests completed
total tests completed
test outcomes
total case outcomes (resolutions and deaths)
current tests under investigation
current hospitalizations
current patients in Intensive Care Units (ICUs)
current patients in Intensive Care Units (ICUs) on ventilators
change in number of cases from previous day by Public Health Unit (PHU)

- (COVID-19 testing locations)[https://data.ontario.ca/dataset/covid-19-assessment-centre-locations]

Location name
Location operator
Physical address
Phone number
Website
Public Health Unit (PHU)
Latitude
Longitude
Physical address
Phone number
Hours of operation
Age restrictions
Appointment requested
Drive through availability
Walk in availability
Temporary closure
Active centre (indefinite closures

- (Confirmed positive cases of COVID-19 in Ontario)[https://data.ontario.ca/en/dataset/confirmed-positive-cases-of-covid-19-in-ontario]

approximation of onset date
age group
patient gender
case acquisition information
patient outcome
reporting Public Health Unit (PHU)
postal code, website, longitude, and latitude of PHU

- (COVID-19 Vaccine Data in Ontario)[https://data.ontario.ca/dataset/covid-19-vaccine-data-in-ontario]

daily doses administered
total doses administered
individuals fully vaccinated
total doses given to fully vaccinated individuals


