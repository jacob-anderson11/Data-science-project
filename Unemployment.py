#Unemployment charts


#Below i will be importing the packages needed.


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap 
from matplotlib.dates import DateFormatter, MonthLocator
import matplotlib.dates as mdates


#Below i will be creating the functions used throughout


def customise_axes(ax): #This function is specifying desired parameters that can be called upon for charts
    ax.set_axisbelow(True) #This sets the axis lines below the data lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False) #These three remove the top, right and bottom boarders
    ax.grid(b=True, which = "major", axis = "x", color = "white")
    ax.grid(b=True, which = "major", axis = "y", color = "lightblue") #These two display just the horizontal gridlines
    plt.xlabel("") #Makes it so there is no x label (usually unneeded as it is just the date)


def indexed_time_series(data, start_period, series_name):
    data[series_name] = pd.to_numeric(data[series_name], errors='coerce')
    print(data["Time period and dataset code row"])
    start_value = pd.to_numeric(data[data["Time period and dataset code row"] == start_period][series_name].iloc[0], errors='coerce')
    data[series_name] = 100 * data[series_name] / start_value
    data["date time"] = data["Time period and dataset code row"].str.replace(" ", "-")
    start_period = start_period.replace(" ", "-")
    data["date time"] = pd.to_datetime(data["date time"])
    data = data[data["date time"] >= start_period]
    return data #This function is used on charts where indexed calculations need to be performed within python

requests.packages.urllib3.disable_warnings()
def ons_data_downloader(link, output_file_name, tab_name, skip_rows):
    response = requests.get(link, verify=False)
    with open('data/raw/' + output_file_name + '.xlsx', 'wb') as file:
        file.write(response.content)
    data_tab = pd.read_excel('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/raw/' + output_file_name + '.xlsx', sheet_name=tab_name, skiprows=skip_rows)
#UPDATE: CHANGE FILE PATH
    data_tab.to_csv('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/'  +  output_file_name + '.csv', index=False)
#UPDATE: CHANGE FILE PATH
    return    #This function allows us to download the data directly from the ONS website. It stores the original in the 'raw' and the data we will then use in 'processed'.



#Chart 1 -  Vacancies, unemployment, vacancy/unemployment ratio


vacancy_unemployment_link = "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/vacanciesandunemploymentvacs01/current/vacs01jun2024.xlsx" #This is the direct link to the data being used (not the URL)
#UPDATE - REPLACE WITH MOST UP-TO-DATE LINK FROM THE ONS WEBSITE
file_name = "vacancy_unemployment"  #This is how the file will be stored in the processed and raw data
ons_data_downloader(vacancy_unemployment_link, file_name, "VACS01", 4) #The first part of the function calls upon the link name, the second part calls the file_name directly, the third is the name of the data tab we will be using from the raw data, the last number is the number of rows being skipped to get to the relevant data (to the first row above the data)
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins. 

vacancy_unemployment = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/vacancy_unemployment.csv")  #This is reading in the data from you files and storing it as a dataframe
#UPDATE WITH LINK TO OWN FILE PATH
vacancy_unemployment_processed = vacancy_unemployment.iloc[239:276, [0,2,3]].reset_index() #The first numbers (239:276 in original) is the rows we are looking at. Alter this to change time series. Always +1 to the last number to update for latest data. Second numbers (0,2,3) is what columns we use. This should remain fixed unless order of raw data changes.
#UPDATE ROW NUMBERS TO ALTER TIME SERIES AND ADD MOST RECENT DATA
vacancy_unemployment_processed = vacancy_unemployment_processed.rename(columns={"AP2Y":"all vacancies", "MGSC":"unemployment", "Unnamed: 0":"date"}) #Renaming the column names to more desriable names 
vacancy_unemployment_processed['unemployment'] = pd.to_numeric(vacancy_unemployment_processed['unemployment']) #Converting the unemployment data to numeric so python can read it

vacancy_unemployment_processed['all vacancies (millions)'] = vacancy_unemployment_processed['all vacancies'] / 1000
vacancy_unemployment_processed['unemployment (millions)'] = vacancy_unemployment_processed['unemployment'] / 1000
vacancy_unemployment_processed['vacancy/unemployment ratio'] = vacancy_unemployment_processed['all vacancies (millions)'] / vacancy_unemployment_processed['unemployment (millions)']
#Above is doing the calculations needed. Vacancies and unemployment are in thousands.

fig, ax1 = plt.subplots()
ax2 = ax1.twinx() #Here we are going to be using two y-axis, hence setting up ax1 and ax2 on the same chart

p1, = ax1.plot(vacancy_unemployment_processed["date"], vacancy_unemployment_processed["all vacancies (millions)"], color="#206095")
p2, = ax1.plot(vacancy_unemployment_processed["date"], vacancy_unemployment_processed["unemployment (millions)"], color="#2dd06b")
p3, = ax2.plot(vacancy_unemployment_processed["date"], vacancy_unemployment_processed["vacancy/unemployment ratio"], color="#871a5b", linestyle="dotted") #Here wer are creating the line plots, with each line being assigned a value so it can be called upon.
#Notice ax1 us for the vacancies and unemployment level, with ax2 being for the V/U.

ax1.set_axisbelow(True) #Setting ax1 lines below the chart lines
ax1.spines['top'].set_visible(False) 
ax1.spines['bottom'].set_visible(False) #Turning off the top and bottom border
ax1.grid(b=True, which = "major", axis = "x", color = "white")
ax1.grid(b=True, which = "major", axis = "y", color = "lightblue") #Setting gridlines for formatting

ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False) 
ax2.spines['bottom'].set_visible(False) #Repeating these steps for ax2
plt.title("Level of unemployment & vacancies, V/U ratio", fontweight="bold", fontname="Arial", fontsize="12") #Adding a title and changing the formatting
plt.legend([p1, p2, p3], ["Vacancies (LHS)", "Unemployment (LHS)", "V/U ratio (RHS)"], bbox_to_anchor=(1.1,-0.12), ncol=3, frameon=False) #Adding all the lines to the legend and changing the formatting
ax1.set_ylabel("Millions", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-45) #Adding a ax1 y-label and changing the formatting
ax1.yaxis.set_label_coords(0, 1.035) #Setting the ax1 label above the chart
ax1.set_ylim(bottom=0.5, top=1.9)
ax2.set_ylim(bottom=0.2, top=1.2) #Setting y-limits for both ax1 and ax2
desired_labels = ["Feb-Apr 2021", "Feb-Apr 2022", "Feb-Apr 2023", "Feb-Apr 2024"] #The labels to be shown on the x-axis
#UPDATE TO SHOW FOR THE LATEST QUARTER OR CHANGE LABELS AS WANTED
ax1.set_xticks([vacancy_unemployment_processed["date"].index[i] for i, label in enumerate(vacancy_unemployment_processed["date"]) if label in desired_labels])
ax1.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
desired_labels = ["Feb-Apr 2021", "Feb-Apr 2022", "Feb-Apr 2023", "Feb-Apr 2024"]
#UPDATE TO SHOW FOR THE LATEST QUARTER OR CHANGE LABELS AS WANTED
ax2.set_xticks([vacancy_unemployment_processed["date"].index[i] for i, label in enumerate(vacancy_unemployment_processed["date"]) if label in desired_labels])
ax2.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
#The labels have to be done for both ax1 and ax2 hence the repeat, so make sure to updated both

plt.show()



#Chart 2 - Month on month change in vacancies, vacancy/unemployment ratio


monthly_vacancies = vacancy_unemployment_processed.iloc[:,[0,1,2,6]] #Using the data from above, but this time using a different set of columns
monthly_vacancies["all vacancies"] = monthly_vacancies["all vacancies"] * 1000 #originally data is stored in thousands, expanding it out to a normal form
monthly_vacancies['monthly change in vacancies'] = monthly_vacancies['all vacancies'].diff() #works out the monthly change in vacancies, and stores the number under a new variable
monthly_vacancies_processed = pd.merge(monthly_vacancies, vacancy_unemployment_processed, on="date") #merging the two data frames to have all the data accessible

fig, ax1 = plt.subplots() #Again, setting it up so we have two y-axis

ax1.set_axisbelow(True)
ax1.bar(monthly_vacancies_processed['date'], monthly_vacancies_processed['monthly change in vacancies'], color='#206095') #Having our change in vacancies as a barplot
ax1.spines['top'].set_visible(False) 
ax1.spines['bottom'].set_visible(False) 
ax1.grid(b=True, which = "major", axis = "x", color = "white")
ax1.grid(b=True, which = "major", axis = "y", color = "lightblue")
plt.legend(["Monthly changes in vacancies (LHS)"], bbox_to_anchor=(1,-0.12), ncol=2, frameon=False)
desired_labels = ["Feb-Apr 2021", "Feb-Apr 2022", "Feb-Apr 2023", "Feb-Apr 2024"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST DATA
ax1.set_xticks([monthly_vacancies_processed["date"].index[i] for i, label in enumerate(monthly_vacancies_processed["date"]) if label in desired_labels])
ax1.set_xticklabels(desired_labels, rotation=0)
ax1.yaxis.set_ticks(np.linspace(-120000, 120000, 7)) #Alternate way of setting the y-limits, as well as '7' being the number of ticks

ax2 = ax1.twinx()

ax2.set_axisbelow(True)
ax2.plot(monthly_vacancies_processed['date'], monthly_vacancies_processed['vacancy/unemployment ratio_y'], color='#27a0cc') #The V/U ratio is a line plot
ax2.yaxis.set_label_coords(1.05, 1.05)
ax2.set_ylim(bottom= -1.2, top=1.2)
ax2.spines['top'].set_visible(False) 
ax2.spines['bottom'].set_visible(False)  
plt.title('M-M changes in vacancies, V/U ratio', fontweight="bold", fontname="Arial", fontsize="12")
plt.legend(["V/U ratio (RHS)"], bbox_to_anchor=(0.3,-0.12), ncol=2, frameon=False)
desired_labels = ["Feb-Apr 2021", "Feb-Apr 2022", "Feb-Apr 2023", "Feb-Apr 2024"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST DATA
ax2.set_xticks([monthly_vacancies_processed["date"].index[i] for i, label in enumerate(monthly_vacancies_processed["date"]) if label in desired_labels])
ax2.set_xticklabels(desired_labels, rotation=0)
ax2.yaxis.set_ticks(np.linspace(-1.2, 1.2, 7))

plt.show()


#Chart 3 - Job adverts index


job_adverts_link = "https://www.ons.gov.uk/file?uri=/economy/economicoutputandproductivity/output/datasets/onlinejobadvertestimates/2024/onlinejobadvertestimatesdataset050724.xlsx"
#UPDATE WITH LATEST LINK DIRECTLY TO THE NEW DATA
file_name = "job_adverts"
ons_data_downloader(job_adverts_link, file_name, "Adverts by region Feb 2020", 6)
#Usually won't need updating, but if an error occurs check the tab name of the number of rows needing to be skipped hasn't changed

job_adverts = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/job_adverts.csv")
#UPDATE WITH LINK TO OWN FILE PATH
job_adverts_processed = job_adverts.iloc[71:334,[0,1]].reset_index() 
#UPDATE ILOC FUNCTION AS REQUIRED. ROW NUMBERS (70:333 IN ORIGINAL) WILL NEED UPDATING AS TIME SERIES UPDATES

fig,ax = plt.subplots()
plt.plot(job_adverts_processed["Date"], job_adverts_processed["All Regions"], color="#206095", linewidth="2.0")
plt.title("Online job adverts (Feb 2020 = 100)", fontweight="bold", fontname="Arial", fontsize="12")
customise_axes(ax)
# Format the x-axis to show dates
job_adverts_processed["Date"] = pd.to_datetime(job_adverts_processed["Date"], dayfirst=True)
job_adverts_processed["Date"] = job_adverts_processed["Date"].dt.strftime("%d %b %Y")
plt.ylim(bottom=30, top=150)
desired_labels = ["26 Jun 2020", "24 Jun 2022", "28 Jun 2024"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([job_adverts_processed["Date"].index[i] for i, label in enumerate(job_adverts_processed["Date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0, ha="center") #Above we have set what desired labels we would like to show on the x-axis

plt.show()


#Chart 4 - Cumulative change in economic inactivity by reason


inactivity_link = "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peoplenotinwork/economicinactivity/datasets/economicinactivitybyreasonseasonallyadjustedinac01sa/current/inac01sajun2024.xls"
file_name = "inactivity"
ons_data_downloader(inactivity_link, file_name, "People", 7)

inactivity = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/inactivity.csv") 
inactivity = inactivity.iloc[336:385, [0,1,2,3,4,5,6,7,8]].reset_index()
inactivity = inactivity.rename(columns={"Dataset identifier code":"Date", "Unnamed: 1": "total", "LF63":"student","LF65":"looking after family/home",
                                        "LF67":"temp sick","LF69":"long-term sick","LFL8":"discouraged workers","LF6B":"retired","LF6D":"other"})

inactivity[['total', 'student', 'looking after family/home', 'temp sick', 'long-term sick', 
            'discouraged workers', 'retired', 'other']] = inactivity[['total', 'student', 'looking after family/home',
            'temp sick', 'long-term sick', 'discouraged workers', 'retired', 'other']].apply(pd.to_numeric, errors='coerce')  
                                                                                                                         
                                                                      
inactivity_processed = inactivity.copy()
inactivity_processed.iloc[:, 2:] = inactivity.iloc[:, 2:].subtract(inactivity.iloc[0, 2:]) / 1000
inactivity_processed.columns = inactivity.columns
                              
fig, ax = plt.subplots()                        
plt.plot(inactivity_processed["Date"], inactivity_processed["total"], color="#f66068")
inactivity_processed.set_index("Date")[['student', 'looking after family/home', 'temp sick', 'long-term sick', 'discouraged workers', 'retired', 'other']].plot(kind="bar", stacked=True, ax=ax, color=["#206095","#2dd06b", "#746cb1","#27a0cc","#871a5b","#118c7b","#a8bd3a"])          
#nominal_real_income_processed.set_index("date")[["implied deflator", "nominal income"]].plot(kind="bar", ax=ax, stacked=True, color=["#27a0cc","#003c57"]) #Creating the bar plots for nominal income and the implied deflator
customise_axes(ax)
plt.title("Reasons for economic inactivity, cumulative change, thousands",  fontweight="bold", fontname="Arial", fontsize="12")
plt.legend(['Total', 'Student', 'Looking after family/home', 'Temp sick', 'Long-term sick', 
            'Discouraged workers', 'Retired', 'Other'], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False)
plt.axhline(0, color="black", linewidth="2.0")
#plt.ylim(bottom="")
desired_labels = ["Feb-Apr 2020", "Feb-Apr 2021", "Feb-Apr 2022", "Feb-Apr 2023", "Feb-Apr 2024"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([inactivity_processed["Date"].index[i] for i, label in enumerate(inactivity_processed["Date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis

plt.show()


# Chart 5 - labour demand vs labour supply

employment_link = "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/summaryoflabourmarketstatistics/current/a01jun2024.xls"
file_name = "employment"
ons_data_downloader(employment_link, file_name, "1", 7)

employment = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/employment.csv")
employment_processed = employment.iloc[602:639, [0,3]].reset_index()
#Here, in the original code, i am looking at rows 602:639 in the employment data frame. This looks at Feb-Apr 2021-2024. This is because it is the same time frame i am looking at 
#in chart 2 & 3. These charts are interlinked, as i have merged them together because they use common data. Therefore, ensure all the data frames have the same time frame.
#As usual, to change this, change the row numbers we are looking at, by looking at the non-processed data frame in the variable explorer.
employment_processed = employment_processed.rename(columns={"Dataset identifier code":"date", "MGRZ":"employment"})
employment_processed = employment_processed["employment"] / 1000

demand_and_supply = pd.concat([employment_processed, vacancy_unemployment_processed], axis=1)

demand_and_supply = demand_and_supply.iloc[:, [0,1,2,3,4]]

demand_and_supply['labour demand'] = demand_and_supply.iloc[:, 0] + demand_and_supply.iloc[:, 3]
demand_and_supply['labour supply'] = demand_and_supply.iloc[:, 0] + demand_and_supply.iloc[:, 4]

fig, ax = plt.subplots()

plt.plot(demand_and_supply["date"], demand_and_supply["labour demand"], color="#206095", linewidth="2.0")
plt.plot(demand_and_supply["date"], demand_and_supply["labour supply"], color="#27a0cc", linewidth="2.0")
customise_axes(ax)
plt.title("Labour demand vs Labour supply (thousands)", fontweight="bold", fontname="Arial", fontsize="12")
plt.legend(["Labour demand", "Labour supply"], bbox_to_anchor=(0.9,-0.12), ncol=2, frameon=False)
plt.ylim(bottom=32499, top=35000)
desired_labels = ["Feb-Apr 2021", "Feb-Apr 2022", "Feb-Apr 2023", "Feb-Apr 2024"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([demand_and_supply["date"].index[i] for i, label in enumerate(demand_and_supply["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis

plt.show()


#Chart 6 - Output per hour worked

output_per_hour_link = "https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/labourproductivity/current/prdy.xlsx"
#UPDATE WITH LATEST LINK
file_name = "output_per_hour"
ons_data_downloader(output_per_hour_link, file_name, "data", 0)  

output_per_hour = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/output_per_hour.csv")
output_per_hour_processed = output_per_hour.iloc[273:, [0,-6]].reset_index()
#UPDATE: THIS WILL REQUIRE YOU LOOKING IN THE RAW DATA (output_per_hour dataframe in python), TO CHECK THE COLUMNS NEEDED. IN ORIGINAL FILE, THE RELEVANT DATA (CDID: LZVD) IS IN THE 6TH COLUMN FROM THE RIGHT (HENCE COUNTING BACKWARDS, IT IS COLUMN -6). THIS MAY CHANGE. ROWS '273:' IN ORIGINAL FILE LOOKS FROM Q1 2010 ONWARDS.

output_per_hour_processed = output_per_hour_processed.rename(columns={"Title":"date", "UK Whole Economy: Output per hour worked % change per annum SA":"output"})#If the columns are incorrect, this will error.

fig,ax = plt.subplots()

output_per_hour_processed["output"] = pd.to_numeric(output_per_hour_processed["output"])
output_per_hour_processed.set_index("date")[["output"]].plot(kind="bar", ax=ax, stacked=True, color=["#206095"])
customise_axes(ax)
plt.title("Output per hour worked, year-on-year change", fontweight="bold", fontname="Arial", fontsize="12")
plt.ylim(bottom=-6, top=8)
plt.legend("", frameon=False)
desired_labels = ["2010 Q1","2015 Q2", "2019 Q3", "2023 Q4"]
ax.set_xticks([output_per_hour_processed["date"].index[i] for i, label in enumerate(output_per_hour_processed["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis

plt.show()

