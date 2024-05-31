import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap 
from matplotlib.dates import DateFormatter, MonthLocator #Importing the packages needed throughout

def wrap_ylabels(ax, width, break_long_words=False):
 labels = []
 for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=break_long_words))
 ax.set_yticklabels(labels) #A function that allows labels to be wrapped when they are long

def create_fmt(date_str): 
    year = date_str[:4]   
    month = date_str[4:].upper() 
    return f"{year}-{month}-01"  
def convert_ONS_date_to_date_time(data):
    data['Date_time'] = pd.to_datetime(data['Month'].apply(create_fmt))
    return data #This code is defining a function, converting the date/time within any dataset to one that is readable by python

def customise_axes(ax):
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False) 
    ax.grid(b=True, which = "major", axis = "x", color = "white")
    ax.grid(b=True, which = "major", axis = "y", color = "lightblue")
    plt.xlabel("") #This code is defining a function, specifying desired parameters that can be called upon for charts
    
def indexed_time_series(data, start_period, series_name): 
    data[series_name] = 100 * data[series_name] / (data[data["Time period"] == start_period][series_name].iloc[0])
    data["date time"] = data["Time period"].str.replace(" ", "-")
    start_period = start_period.replace(" ", "-")
    data["date time"] = pd.to_datetime(data["date time"])
    data = data[data["date time"] >= start_period]
    return data #A function created to index raw data

requests.packages.urllib3.disable_warnings()
def ons_data_downloader(link, output_file_name, tab_name, skip_rows):
    response = requests.get(link, verify=False)
    with open('data/raw/' + output_file_name + '.xlsx', 'wb') as file:
        file.write(response.content)
    data_tab = pd.read_excel('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/raw/' + output_file_name + '.xlsx', sheet_name=tab_name, skiprows=skip_rows)
#UPDATE: change file path to own computer. Create folders as such for ease
    data_tab.to_csv('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/'  +  output_file_name + '.csv', index=False)
#UPDATE: change file path to own computer. Create folders as such for ease
    return    #This function allows us to download the data directly from the ONS website. It stores the original in the 'raw' and the data we will then use in 'processed'.


#GDP SECTION:
    
#Chart 1 - An index of monthly GDP and the four main sectors
gdp_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/monthlygdpandmainsectorstofourdecimalplaces/1997tocurrent/monthlygdpto4dp.xlsx" 
#UPDATE: Make sure link is up-to-date to the latest dataset available 
file_name = "gdp_by_sector" #how the file name will be stored in your files
ons_data_downloader(gdp_link, file_name, "Data_table", 3) #This code downloads the data from the ONS website, saves it under a specific name, with the last number being the number of rows skipped so only the necessary data is processed. 'Data_table' is the name of the tab the data is downloaded from

GDP_data_sectors = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/gdp_by_sector.csv") #Saving the data in this specific folder
GDP_data_sectors = GDP_data_sectors[["Month","Monthly GDP (A-T)", "Agriculture (A)", "Construction (F) [note1],[note 2]", "Production (B-E)", "Services (G-T)"]] #This is a list of the column names used. Ensure they are exactly the same as those being downloaded in the data (check for spaces and capital letters)

GDP_data_sectors = convert_ONS_date_to_date_time(GDP_data_sectors)
GDP_data_sectors = GDP_data_sectors.loc[GDP_data_sectors["Date_time"] > "2022-DEC-01", : ] #This is converting the 'month' column in the excel sheet to a format that python can read, as well as specifying from where we want the time series to start
#UPDATE the above date to show the range of data wanted. To then change the x-ticks, change MaxNLocator number at the bottom

fig,ax = plt.subplots() #This is a function used in matplot lib to allow plots to be created
plt.plot(GDP_data_sectors["Month"],GDP_data_sectors["Monthly GDP (A-T)"], color="#206095", linewidth="2.0")
plt.plot(GDP_data_sectors["Month"],GDP_data_sectors["Agriculture (A)"], color="#27a0cc", linewidth="2.0")
plt.plot(GDP_data_sectors["Month"],GDP_data_sectors["Construction (F) [note1],[note 2]"], color="#003c57", linewidth="2.0")
plt.plot(GDP_data_sectors["Month"],GDP_data_sectors["Production (B-E)"] ,color="#118c7b", linewidth="2.0")
plt.plot(GDP_data_sectors["Month"],GDP_data_sectors["Services (G-T)"], color="#a8bd3a", linewidth="2.0") #This is all plotting the different variables (Y axis) against the month (x axis). Ensure the names exactly match those in the excel document.

plt.title('Main GDP contributors (2019=100)', fontweight="bold", fontname="Arial", fontsize="12") #Title label
plt.legend(["Monthly GDP","Agriculture","Construction","Production","Services"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=3, frameon=False) #Setting the legend as well as the location of it, the number of columns and whether there is a frame on the legend
customise_axes(ax) #calling upon the second function specified, which just has a common set of parameters used throughout to save time
ax.set_ylim(bottom=79.5, top=110); #The y-axis scale
ax.xaxis.set_major_locator(plt.MaxNLocator(4)) #The number of x labels wanted, change the number as desired

#Chart 2 - Just the index of monthly GDP
fig,ax = plt.subplots()
plt.plot(GDP_data_sectors["Month"],GDP_data_sectors["Monthly GDP (A-T)"], color="#206095", linewidth="2.0") #Plotting just the monthly GDP against the month

plt.title('Monthly GDP (2019=100)', fontweight="bold", fontname="Arial", fontsize="12") #Title for the chart
customise_axes(ax) #Calling in the function defined for chart paramaters
ax.set_ylim(bottom=99.5, top=105); #y axis scale
ax.xaxis.set_major_locator(plt.MaxNLocator(4)) #The number of x labels wanted, change the number as desired
plt.show() #Nothing needs updating in chart 2, unless parameters are being changed

#Chart 3 - The change in monthly GDP, month-month and 3month-3month growth
GDP_data_m_3m = pd.read_excel("//NDATA9/anderj3$/My Documents/Data Science Project/Master file.xlsx", sheet_name="GDP_1.2")
#UPDATE with latest link
GDP_data_m_3m = GDP_data_m_3m[["Time period","Month/Month","3m/3m"]]

fig,ax =plt.subplots()
plt.plot(GDP_data_m_3m["Time period"],GDP_data_m_3m["Month/Month"], color="#206095", linewidth="2.0") #Line plot of the month/month change against the time period

plt.bar(GDP_data_m_3m["Time period"],GDP_data_m_3m["3m/3m"], color='#27a0cc', width=0.8) #Adding a bar plot of 3month/3month change
plt.legend(["Month/Month","3month/3month"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Adding a legend and setting the location
customise_axes(ax) #Calling upon this function again
plt.axhline(0, color="black", linewidth=0.5) #For formatting - put a line through the x axis
ax.set_ylim(bottom=-1.05, top=1); #Setting the y-axis parameters
ax.xaxis.set_major_locator(plt.MaxNLocator(5)) #Setting the number of ticks on the x-axis
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-45) #y-axis label
plt.title("Changes in monthly GDP", fontweight="bold", fontname="Arial", fontsize="12") #Title for the chart
plt.show()

#Chart 4 and 5 started in notes - Uses calculations so will wait till we get to this

#Chart 6 - Contributions to changes in monthly GDP by sector 

gdp_link_sector_changes  = "https://www.ons.gov.uk/generator?uri=/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/march2024/332c4b4f&format=xls"
#UPDATE with latest link, from figure 2 in the GDP bulletin (linked below chart)
file_name = "gdp_by_sector_monthly" #How the file name will be stored in your files
ons_data_downloader(gdp_link_sector_changes, file_name, "data", 6) #downloading the data from the ONS website. Again, 'data' is the name of the tab being used, with 6 being the number of rows being skipped

GDP_sectors_month = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/gdp_by_sector_monthly.csv")
#UPDATE with file path to your own computer, again ensuring the necessary folders are set up to store the raw and processed data 
GDP_sectors_month = GDP_sectors_month[["Date", "GDP", "Services", "Production", "Construction"]] #Ensure these variable names match those in the dataset (be careful of capital letters and spaces)

fig, ax =plt.subplots()
plt.plot(GDP_sectors_month["Date"], GDP_sectors_month["GDP"], color="#206095") #Plotting the line graph of GDP first

GDP_sectors_month[["Date", "Services", "Construction", "Production"]].plot("Date",kind="bar", stacked=True, ax=ax, color=["#27a0cc","#003c57", "#118c7b"]) #Now creating a stacked barplot with the rest of the variables
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-45) #y-axis label
plt.title("Contributions to monthly GDP growth, Feb 23-Feb 24", fontweight="bold", fontname="Arial", fontsize="12") #Title for the chart
plt.legend(["GDP","Services","Production","Construction"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=4, frameon=False) #change loc to change the position of the legend
customise_axes(ax) #Calling upon this function again
ax.set_ylim(bottom=-1.05, top=1); #y-axis scale
plt.axhline(0, color="black", linewidth=0.5) #A black line through the x-axis for formatting
ax.xaxis.set_major_locator(plt.MaxNLocator(4)) #Setting the number of ticks on the x-axis
ax.xaxis.set_tick_params(rotation=360)
plt.show()

#Chart 7 - Contributions to changes in monthly GDP, month-month
Contributions_to_monthly_changes_link  = "https://www.ons.gov.uk/generator?uri=/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/march2024/fcab48fd&format=xls"
#UPDATE with latest link, figure 3 in GDP bulletin (link below chart)
file_name = "contributions_to_monthly_changes"
ons_data_downloader(Contributions_to_monthly_changes_link, file_name, "data", 6) #This is doing the same things as previously mentioned. Only need to check the tab is still called 'data', and that we want to skip 6 rows

GDP_contributions = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/contributions_to_monthly_changes.csv")
#UPDATE with your own file path, again, make sure necessary file paths are created
GDP_contributions = GDP_contributions[["Unnamed: 0","Monthly","Three-month"]]

fig, ax=plt.subplots()
plt.barh(GDP_contributions["Unnamed: 0"], GDP_contributions["Monthly"], color="#206095")  #Creating a barplot of the monthly data. Unnamed: 0 is the default for the processed data when it is orignally blank in the excel raw data.

plt.xlabel("Percentage points") #x-axis label
ax.set_frame_on(False) #Removes frame off the chart
plt.title("Contributions to changes in Feb GDP", fontweight="bold", fontname="Arial", fontsize="12") #Title
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-1, color="black", linewidth=0.5) #Both lines for formatting
ax.set_xlim(left=-0.102, right=0.102); #x-axis scale
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue") #Grid lines for formatting
ax.set_axisbelow(True) #Setting the axis lines below chart lines
plt.ylabel("") #No y-label needed hence left blank
wrap_ylabels(ax, 50)
ax.tick_params(axis='y', labelsize=8)
plt.show()

#Chart 8 - Contributions to changes in monthly GDP, month-month and 3month-3month

fig, ax=plt.subplots()
GDP_contributions.plot("Unnamed: 0",kind="barh", stacked=False, ax=ax, color=["#206095","#27a0cc"]) #Now creating a barplot for month and 3 month changes

plt.xlabel("Percentage points") #x-axis label
ax.set_frame_on(False) #Removing chart frame
plt.ylabel("") #No y-label needed hence left blank
plt.title("Contributions to changes in Feb GDP", fontweight="bold", fontname="Arial", fontsize="12") #Title
ax.set_xlim(left=-0.102, right=0.102); #y-axis scale
plt.legend(["Monthly", "Three month"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False)#Altering the legend
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.5, color="black") #Grid lines for formatting
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue") #Gridlines for formatting
ax.set_axisbelow(True) #Setting axis below frame
wrap_ylabels(ax, 50)
ax.tick_params(axis='y', labelsize=8)
plt.show()


#Chart 9 - Uses calcs so will wait 

#Chart 10 - Quarterly change in GDP per capita

PC_quarterly = pd.read_excel("//NDATA9/anderj3$/My Documents/Data Science Project/Master file.xlsx", sheet_name="GDP_1.7")
PC_quarterly = PC_quarterly[["Time period","Gross domestic product per head"]]

fig,ax=plt.subplots()
plt.bar(PC_quarterly["Time period"], PC_quarterly["Gross domestic product per head"], color="#206095") #Plotting a barplot

plt.ylabel("%", rotation=0, loc="top", labelpad=-35) #y-axis label: rotating it so it reads horizontal, at the top of the axis, and above the axis
#ax.set_ylabel("% change", rotation=0, location="top")
plt.title("Quarterly change in GDP per capita", fontweight="bold", fontname="Arial", fontsize="12") #Title
plt.axhline(0, color="black", linewidth=0.5) #Line for formatting
customise_axes(ax) #Calling upon this common function
plt.show()

#Chart 11 - GDP per capita indexed

GDP_per_capita = pd.read_excel("//NDATA9/anderj3$/My Documents/Data Science Project/Master file.xlsx", sheet_name="GDP_1.8")
GDP_per_capita = GDP_per_capita[["Time period", "Gross domestic product per head: Chained volume measures"]]

GDP_per_capita_processed = indexed_time_series(GDP_per_capita, "2012 Q1", "Gross domestic product per head: Chained volume measures") #Using the function created at the top to index the GDP per capita raw data

fig,ax = plt.subplots()
plt.plot(GDP_per_capita_processed["Time period"], GDP_per_capita_processed["Gross domestic product per head: Chained volume measures"], color="#206095") #Creating a time series of the indexed GDP per capita data
plt.title("GDP per capita (2012 Q1 = 100)", fontweight="bold", fontname="Arial", fontsize="12") #Creating a title and changing the parameters
desired_labels = ["2012 Q1", "2014 Q4", "2017 Q4", "2020 Q4", "2023 Q4"]
ax.set_xticks([GDP_per_capita_processed["Time period"].index[i] for i, label in enumerate(GDP_per_capita_processed["Time period"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.axhline(100, color="black", linewidth=0.5) #Line for formatting
ax.set_ylim(bottom=83, top=115); #Setting the y-axis parameters
customise_axes(ax) #Calling upon this function
plt.show()

#Chart 12 - Public sector net debt as a percentage of GDP

Debt_GDP_link  = "https://www.ons.gov.uk/generator?format=xls&uri=/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ruto/pusf"
#UPDATE with latest link, figure 3 in GDP bulletin (link below chart)
file_name = "Public_debt_%_GDP"
ons_data_downloader(Debt_GDP_link, file_name, "data", 253)

Debt_GDP = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/Public_debt_%_GDP.csv")
Debt_GDP = Debt_GDP[["2024 Q1", "111.8"]]

fig,ax=plt.subplots()
plt.plot(Debt_GDP["2024 Q1"], Debt_GDP["111.8"], color="#206095") #Creating a plot of net debt as a % of GDP across time (when downloading data from the ONS website, after we skip rows to get to the )

plt.ylabel("%", rotation=0, loc="top", labelpad=-35) #y-axis label
plt.title("Net debt as a percentage of GDP", fontweight="bold", fontname="Arial", fontsize="12") #Title
customise_axes(ax) #Calling upon the function again to set chart parameters
desired_labels = ["1993 MAR", "2001 MAR", "2009 MAR", "2017 MAR", "2024 MAR"]
ax.set_xticks([Debt_GDP["2024 Q1"].index[i] for i, label in enumerate(Debt_GDP["2024 Q1"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
ax.set_ylim(bottom=20, top=163) #Setting the y-axis porameters
plt.show()

#Chart 13 - Post-reccesion GDP indexed

post_recession_GDP = pd.read_excel("//NDATA9/anderj3$/My Documents/Data Science Project/Master file.xlsx", sheet_name="GDP_1.10")
post_recession_GDP = post_recession_GDP[["Time period", "Gross domestic product at market prices: Chained volume measure"]]

recession_dates = ["1973 Q2", "1979 Q4", "1990 Q2", "2008 Q1", "2023 Q2"] 
combined_data = pd.DataFrame()
for date in recession_dates:
     post_recession_GDP_processed = indexed_time_series(post_recession_GDP, date, "Gross domestic product at market prices: Chained volume measure")
     post_recession_GDP_processed[date] = post_recession_GDP_processed["Gross domestic product at market prices: Chained volume measure"]
     post_recession_GDP_processed = post_recession_GDP_processed.iloc[0:16, :].reset_index()
     post_recession_GDP_processed = post_recession_GDP_processed[["Time period", date]]
     combined_data = pd.concat([post_recession_GDP_processed, combined_data], axis=1)
combined_data = combined_data.reset_index()

fig,ax =plt.subplots()
for date in recession_dates:
    rgb_colors = ["32,96,149","39,160,204","0,60,87","17,140,123","168,189,58"]
colors = [tuple(int(x)/255 for x in rgb.split(',')) for rgb in rgb_colors]

for date, color in zip(recession_dates, colors):
    plt.plot(combined_data["index"], combined_data[date], label=date, color=color, linewidth=2)
    plt.legend(loc="upper center", bbox_to_anchor=(0.5,-0.15), ncol=3, frameon=False)
    plt.title("UK volume GDP recession path", fontweight="bold", fontname="Arial", fontsize="12")
    plt.ylabel("Pre-recession Q = 100", rotation=0, loc="top", labelpad=-95)
    plt.axhline(100, color="black", linewidth=0.5) #Grid lines for formatting
    ax.set_ylim(bottom=91, top=105)
    customise_axes(ax)
    plt.xlabel("Quarters after pre-recession peak")
plt.show()
