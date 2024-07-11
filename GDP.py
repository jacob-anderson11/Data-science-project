#Importing of packages

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap 
from matplotlib.dates import DateFormatter, MonthLocator


#Creation of functions

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

    
    
#Chart 1 - An index of monthly GDP and the four main sectors


gdp_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/monthlygdpandmainsectorstofourdecimalplaces/1997tocurrent/monthlygdpto4dp.xlsx" 
#UPDATE: Make sure link is up-to-date to the latest dataset available 
file_name = "gdp_by_sector" #how the file name will be stored in your files
ons_data_downloader(gdp_link, file_name, "Data_table", 3) #This code downloads the data from the ONS website, saves it under a specific name, with the last number being the number of rows skipped so only the necessary data is processed. 'Data_table' is the name of the tab the data is downloaded from

GDP_data_sectors = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/gdp_by_sector.csv") #Saving the data in this specific folder
#UPDATE WITH LINK TO OWN DATA FILE PATH
GDP_data_sectors = GDP_data_sectors[["Month","Monthly GDP (A-T)", "Agriculture (A)", "Construction (F) [note1],[note 2]", "Production (B-E)", "Services (G-T)"]] #This is a list of the column names used. Ensure they are exactly the same as those being downloaded in the data (check for spaces and capital letters)

GDP_data_sectors = convert_ONS_date_to_date_time(GDP_data_sectors)
GDP_data_sectors = GDP_data_sectors.loc[GDP_data_sectors["Date_time"] > "2022-DEC-01", : ].reset_index() #This is converting the 'month' column in the excel sheet to a format that python can read, as well as specifying from where we want the time series to start
#UPDATE the above date to show the range of data wanted. To then change the x-ticks, change the 'desired labels' part.

fig,ax = plt.subplots() #This is a function used in matplot lib to allow plots to be created
GDP_data_sectors["Date"] = pd.to_datetime(GDP_data_sectors["Month"], format="%Y%b")
GDP_data_sectors["Date"] = GDP_data_sectors["Date"].dt.strftime("%b %Y")
ax.set_xticks(GDP_data_sectors["Date"].index)
ax.set_xticklabels(GDP_data_sectors["Date"])
GDP_data_sectors = GDP_data_sectors.drop("Month", axis=1)#Format the "Date" column as "Feb 2020" from "2020 FEB", and save it under a new variable name "Date"

plt.plot(GDP_data_sectors["Date"],GDP_data_sectors["Monthly GDP (A-T)"], color="#206095", linewidth="2.0")
plt.plot(GDP_data_sectors["Date"],GDP_data_sectors["Agriculture (A)"], color="#27a0cc", linewidth="2.0")
plt.plot(GDP_data_sectors["Date"],GDP_data_sectors["Construction (F) [note1],[note 2]"], color="#003c57", linewidth="2.0")
plt.plot(GDP_data_sectors["Date"],GDP_data_sectors["Production (B-E)"] ,color="#118c7b", linewidth="2.0")
plt.plot(GDP_data_sectors["Date"],GDP_data_sectors["Services (G-T)"], color="#a8bd3a", linewidth="2.0") #This is all plotting the different variables (Y axis) against the month (x axis). Ensure the names exactly match those in the excel document.
desired_labels = ["Jan 2023", "Sep 2023", "Apr 2024"]
ax.set_xticks([GDP_data_sectors["Date"].index[i] for i, label in enumerate(GDP_data_sectors["Date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.title('Main GDP contributors (2019=100)', fontweight="bold", fontname="Arial", fontsize="12") #Title label
plt.legend(["Monthly GDP","Agriculture","Construction","Production","Services"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=3, frameon=False) #Setting the legend as well as the location of it, the number of columns and whether there is a frame on the legend
customise_axes(ax) #calling upon the second function specified, which just has a common set of parameters used throughout to save time
ax.set_ylim(bottom=79.5, top=110); #The y-axis scale


#Chart 2 - Just the index of monthly GDP


fig,ax = plt.subplots()
plt.plot(GDP_data_sectors["Date"],GDP_data_sectors["Monthly GDP (A-T)"], color="#206095", linewidth="2.0") #Plotting just the monthly GDP against the month

plt.title('Monthly GDP (2019=100)', fontweight="bold", fontname="Arial", fontsize="12") #Title for the chart
customise_axes(ax) #Calling in the function defined for chart paramaters
ax.set_ylim(bottom=99.5, top=105); #y axis scale
desired_labels = ["Jan 2023", "Sep 2023", "Apr 2024"]
ax.set_xticks([GDP_data_sectors["Date"].index[i] for i, label in enumerate(GDP_data_sectors["Date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.show() #Nothing needs updating in chart 2, unless parameters are being changed


#Chart 3 - The change in monthly GDP, month-month and 3month-3month growth


GDP_data_m_3m_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/monthlygrossdomesticproductbygrossvalueadded/current/monthlygdptablesapril24.xlsx"
file_name = "GDP_data_m_3m"
ons_data_downloader(GDP_data_m_3m_link, file_name, "GVA", 44)

monthly_data_only = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/GDP_data_m_3m.csv")
monthly_data_only = monthly_data_only.iloc[52:77, [0,2]].reset_index()
monthly_data_only = monthly_data_only.rename(columns={"[Not applicable]": 'Time period', "ED3H": 'Monthly growth'})

three_month_data_only = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/GDP_data_m_3m.csv")
three_month_data_only = three_month_data_only.iloc[0:25,[0,2]].reset_index()
three_month_data_only = three_month_data_only.rename(columns={"[Not applicable]":"Time period", "ED3H":"3 month growth"})

GDP_data_m_3m_processed = pd.merge(monthly_data_only, three_month_data_only, on='Time period')
GDP_data_m_3m_processed = GDP_data_m_3m_processed[['Time period', 'Monthly growth', '3 month growth']]

GDP_data_m_3m_processed["Monthly growth"] = pd.to_numeric(GDP_data_m_3m_processed["Monthly growth"], errors="coerce")
#GDP_data_m_3m_processed["Monthly growth"] = pd.to_numeric(GDP_data_m_3m_processed["Monthly growth"], errors="coerce")
GDP_data_m_3m_processed["3 month growth"] = pd.to_numeric(GDP_data_m_3m_processed["3 month growth"], errors="coerce")

GDP_data_m_3m_processed["Date"] = pd.to_datetime(GDP_data_m_3m_processed["Time period"], format="%Y %b")
GDP_data_m_3m_processed["Date"] = GDP_data_m_3m_processed["Date"].dt.strftime("%b %Y")
ax.set_xticks(GDP_data_m_3m_processed["Date"].index)
ax.set_xticklabels(GDP_data_m_3m_processed["Date"])
GDP_data_m_3m_processed = GDP_data_m_3m_processed.drop("Time period", axis=1)#Format the "Date" column as "Feb 2020" from "2020 FEB", and save it under a new variable name "Date"

fig,ax =plt.subplots()
plt.plot(GDP_data_m_3m_processed["Date"],GDP_data_m_3m_processed["Monthly growth"], color="#206095", linewidth="2.0") #Line plot of the month/month change against the time period
plt.bar(GDP_data_m_3m_processed["Date"],GDP_data_m_3m_processed["3 month growth"], color='#27a0cc', width=0.8) #Adding a bar plot of 3month/3month change
plt.legend(["Month/Month","3month/3month"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Adding a legend and setting the location
customise_axes(ax) #Calling upon this function again
plt.axhline(0, color="black", linewidth=0.5) #For formatting - put a line through the x axis
ax.set_ylim(bottom=-1.05, top=1); #Setting the y-axis parameters
ax.xaxis.set_major_locator(plt.MaxNLocator(5)) #Setting the number of ticks on the x-axis
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-45) #y-axis label
plt.title("Changes in GDP", fontweight="bold", fontname="Arial", fontsize="12") #Title for the chart
plt.ylim(bottom=-1.15, top=1.05)
plt.show()


#Chart 4 and 5 started in notes - Uses calculations so will wait till we get to this

GDP_by_expenditure_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables/quarter1jantomar2024quarterlynationalaccounts/quarterlynationalaccountsdatatables.xlsx"
file_name = "GDP_by_expenditure"
ons_data_downloader(GDP_by_expenditure_link, file_name, "C2 EXPENDITURE", 87)

GDP_by_expenditure =  pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/GDP_by_expenditure.csv")
GDP_by_expenditure_processed = GDP_by_expenditure.iloc[1: ,[0,1,2,3,4,6,8,13,15]].reset_index().copy()
cols = GDP_by_expenditure_processed.columns.drop('Time period and dataset code row')
GDP_by_expenditure_processed[cols] = GDP_by_expenditure_processed[cols].apply(pd.to_numeric, downcast = "float", errors='coerce')

GDP_by_expenditure_processed["consumption"] =  GDP_by_expenditure_processed["Households: Final consumption expenditure"] + GDP_by_expenditure_processed["Non-profit institutions: Final consumption expenditure  [note 2, 7]"]
GDP_by_expenditure_processed["investment"] = GDP_by_expenditure_processed["Gross fixed capital formation: Gross capital formation"] + GDP_by_expenditure_processed["Changes in inventories: Gross capital formation  [note 4]"] + GDP_by_expenditure_processed["Acquisitions less disposals of valuables: Gross capital formation  [note 5]"]
GDP_by_expenditure_processed["GDP"] = GDP_by_expenditure_processed["Gross domestic product at market prices"]

GDP_by_expenditure_processed.rename(columns={"General Government: Final consumption expenditure":"government", "Trade balance [note 6]":"net trade"}, inplace=True)
GDP_by_expenditure_processed["GDP (LESS STATS DISCREPANCY)"] = GDP_by_expenditure_processed["consumption"] + GDP_by_expenditure_processed["government"] + GDP_by_expenditure_processed["investment"] + GDP_by_expenditure_processed["net trade"]
GDP_by_expenditure_processed = GDP_by_expenditure_processed.iloc[ 272:277, [0,1,4,8,10,11,12,13]]


def GDP_expend_calc(df1, col1):
    df1 = df1.reset_index()
    df1 = df1.drop(["index", "Time period and dataset code row"], axis=1)
    cols = df1.columns
    df1[cols] = df1[cols].apply(pd.to_numeric, downcast = "float", errors='coerce')
    output_df1 = df1.copy()
    if col1 == "GDP":
#Explain why...
        denominator = "GDP"
    else:
#Explain why...
        denominator = "GDP (LESS STATS DISCREPANCY)"
    output_df1[col1][0] = 100*((df1[col1][1] - df1[col1][0])/df1[denominator][0])
    output_df1[col1][1] = 100*((df1[col1][2] - df1[col1][1])/df1[denominator][1])
    output_df1[col1][2] = 100*((df1[col1][3] - df1[col1][2])/df1[denominator][2])
    output_df1[col1][3] = 100*((df1[col1][4] - df1[col1][3])/df1[denominator][3])
    return output_df1[col1]
    
combined_df1 = pd.DataFrame()
col1_list = GDP_by_expenditure_processed.columns[2:-1]
for col1 in col1_list:
    Output_df1 = GDP_expend_calc(GDP_by_expenditure_processed, col1)
    combined_df1 = pd.concat([combined_df1, Output_df1], axis=1)
combined_df1 = combined_df1.iloc[0 : 4, : ]

combined_df1.insert(loc=0, column='Time period and dataset code row', value=GDP_by_expenditure_processed['Time period and dataset code row'].values[-4:])

fig, ax = plt.subplots()

plt.plot(combined_df1["Time period and dataset code row"],combined_df1['GDP'], marker='D', linestyle='None', color="#871a5b")
combined_df1[["Time period and dataset code row", "net trade","government","investment","consumption"]].plot(kind="bar", stacked=True, ax=ax, x="Time period and dataset code row", color=["#206095", "#27a0cc","#118c7b","#003c57"])

customise_axes(ax)
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-45)
plt.title("Contributions to changes in real GDP by expenditure component", fontweight="bold", fontname="Arial", fontsize="10")
plt.legend(["GDP", "Net trade","Government","Investment","Consumption"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=3, frameon=False)
plt.ylim(bottom =-1, top =1)
plt.axhline(0, color="black", linewidth=0.5)
plt.xticks(rotation=0)
plt.show()


    
#Chart 6 - Contributions to changes in monthly GDP by sector 


gdp_link_sector_changes  = "https://www.ons.gov.uk/generator?uri=/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/april2024/4b66e990&format=xls"
#UPDATE with latest link, from figure 2 in the GDP bulletin (linked below chart)
file_name = "gdp_by_sector_monthly" #How the file name will be stored in your files
ons_data_downloader(gdp_link_sector_changes, file_name, "data", 6) #downloading the data from the ONS website. Again, 'data' is the name of the tab being used, with 6 being the number of rows being skipped

GDP_sectors_month = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/gdp_by_sector_monthly.csv")
#UPDATE with file path to your own computer, again ensuring the necessary folders are set up to store the raw and processed data 
GDP_sectors_month = GDP_sectors_month[["Date", "GDP", "Services", "Production", "Construction"]] #Ensure these variable names match those in the dataset (be careful of capital letters and spaces)

fig, ax =plt.subplots()
plt.plot(GDP_sectors_month["Date"], GDP_sectors_month["GDP"], color="#206095", linewidth="2.0") #Plotting the line graph of GDP first

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


Contributions_to_monthly_changes_link  = "https://www.ons.gov.uk/generator?uri=/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/april2024/2ca773c2&format=xls"
#UPDATE with latest link, figure 3 in GDP bulletin (link below chart)
file_name = "contributions_to_monthly_changes"
ons_data_downloader(Contributions_to_monthly_changes_link, file_name, "data", 6) #This is doing the same things as previously mentioned. Only need to check the tab is still called 'data', and that we want to skip 6 rows

GDP_contributions = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/contributions_to_monthly_changes.csv")
#UPDATE with your own file path, again, make sure necessary file paths are created
GDP_contributions = GDP_contributions[["Unnamed: 0","Monthly","Three-month"]]

fig, ax=plt.subplots()
GDP_contributions[["Unnamed: 0", "Monthly"]].plot("Unnamed: 0",kind="barh", stacked=False, ax=ax, color=["#206095","#27a0cc"])  #Creating a barplot of the monthly data. Unnamed: 0 is the default for the processed data when it is orignally blank in the excel raw data.

plt.xlabel("Percentage points") #x-axis label
ax.set_frame_on(False) #Removes frame off the chart
plt.title("Contributions to changes in Apr GDP: services", fontweight="bold", fontname="Arial", fontsize="12") #Title
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.4, color="black", linewidth=0.5) #Both lines for formatting
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
plt.title("Contributions to changes in Apr GDP: services", fontweight="bold", fontname="Arial", fontsize="12") #Title
ax.set_xlim(left=-0.102, right=0.102); #x-axis scale
plt.legend(["Monthly", "Three month"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False)#Altering the legend
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.5, color="black") #Grid lines for formatting
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue") #Gridlines for formatting
ax.set_axisbelow(True) #Setting axis below frame
wrap_ylabels(ax, 50)
ax.tick_params(axis='y', labelsize=8)
plt.show()


#Chart 9 - Contributions to UK real GVA 


Real_GVA_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables/quarter1jantomar2024quarterlynationalaccounts/quarterlynationalaccountsdatatables.xlsx"
file_name = "Real_GVA"
ons_data_downloader(Real_GVA_link, file_name, "B1 CVM OUTPUT", 47)

Real_GVA = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/Real_GVA.csv")
Real_GVA = Real_GVA.iloc[134:137, [0, 1, 6, 7, 12, 13]].reset_index()

Real_GVA["Agriculture"] = pd.to_numeric(Real_GVA["L2KL"], errors="coerce")
Real_GVA["Production"] = pd.to_numeric(Real_GVA["L2KQ"], errors="coerce")
Real_GVA["Construction"] = pd.to_numeric(Real_GVA["L2N8"], errors="coerce")
Real_GVA["Services"] = pd.to_numeric(Real_GVA["L2NC"], errors="coerce")
Real_GVA["Total GVA"] = pd.to_numeric(Real_GVA["CGCE"], errors="coerce")
Real_GVA = Real_GVA.iloc[:, [1,7,8,9,10,11]]

def Real_GVA_calc(df, col):
    output_df = df.copy()
    output_df.loc[0, col] = 100*((df[col][1] / df[col][0]) - 1)
    output_df.loc[1, col] = 100*((df[col][2] / df[col][1]) - 1)
    output_df.loc[2, col] = 100*((df[col][2] / df[col][0]) - 1)
    return output_df[col]

Real_GVA_processed = pd.DataFrame()
col_list = Real_GVA.columns[1:]
for col in col_list:
    Output_df = Real_GVA_calc(Real_GVA, col)
    Real_GVA_processed = pd.concat([Real_GVA_processed, Output_df], axis=1)

Real_GVA_processed = Real_GVA_processed.T
Real_GVA_processed.columns = ["Q4 2023", "Q1 2024", "Q3 2023 - Q1 2024"] 
Real_GVA_processed = Real_GVA_processed.reset_index()

fig, ax = plt.subplots()
plt.plot(Real_GVA_processed["index"], Real_GVA_processed["Q3 2023 - Q1 2024"], marker="*", linestyle="None", color="#871a5b")
Real_GVA_processed[["index", "Q4 2023","Q1 2024"]].plot(kind="bar", stacked=True, ax=ax, x="index", color=["#206095", "#27a0cc"])
customise_axes(ax)
plt.title("Real GVA contributions", fontweight="bold", fontname="Arial", fontsize="12")
plt.legend(["Q3 2023 - Q1 2024", "Q4 2023", "Q1 2024"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False)
plt.ylabel("%", rotation=0, loc="top", labelpad=-35)
plt.axhline(0, color="black", linewidth="0.5") #Grid lines for formatting
plt.ylim(bottom=-2.1, top=1)
plt.setp(ax.get_xticklabels(), rotation=0)
plt.show()


#Chart 10 - Quarterly change in GDP per capita


PC_quarterly_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/uksecondestimateofgdpdatatables/quarter1jantomar2024quarterlynationalaccounts/quarterlynationalaccountsdatatables.xlsx"
file_name = "GDP_per_capita_quarterly_change"
ons_data_downloader(PC_quarterly_link, file_name, "P GDP per head", 432)

PC_quarterly = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/GDP_per_capita_quarterly_change.csv")
PC_quarterly = PC_quarterly[["Dataset identifier", "N3Y7"]]
PC_quarterly = PC_quarterly.iloc[267:276, :].reset_index()
PC_quarterly["N3Y7"] = pd.to_numeric(PC_quarterly["N3Y7"], errors="coerce")

fig,ax=plt.subplots()
plt.bar(PC_quarterly["Dataset identifier"], PC_quarterly["N3Y7"], color="#206095") #Plotting a barplot

plt.ylabel("%", rotation=0, loc="top", labelpad=-35) #y-axis label: rotating it so it reads horizontal, at the top of the axis, and above the axis
plt.title("Quarterly change in GDP per capita", fontweight="bold", fontname="Arial", fontsize="12") #Title
plt.axhline(0, color="black", linewidth=0.5) #Line for formatting
customise_axes(ax) #Calling upon this common function
desired_labels = ["2022 Q1", "2023 Q1", "2024 Q1"]
ax.set_xticks([PC_quarterly["Dataset identifier"].index[i] for i, label in enumerate(PC_quarterly["Dataset identifier"]) if label in desired_labels])
ax.set_xticklabels([label.split(" ")[1] + " " + label.split(" ")[0] for label in desired_labels], rotation=0)
plt.show()


#Chart 11 - GDP per capita indexed


ons_data_downloader(PC_quarterly_link, file_name, "P GDP per head", 78)
PC_quarterly_index = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/GDP_per_capita_quarterly_change.csv")

PC_quarterly_index = PC_quarterly_index.drop(index=0)
PC_quarterly_index = PC_quarterly_index.drop(columns= ["UK resident population mid-year estimates (persons, thousands) [note 2]", "Gross domestic product at market prices: Current Prices [note 3]"
                                                       , "Gross domestic product per head: Current Prices", "Gross domestic product at market prices: Chained volume measures [note 3]"])
PC_quarterly_index = PC_quarterly_index.iloc[228 :277, :].reset_index()
GDP_per_capita_processed = indexed_time_series(PC_quarterly_index, "2012 Q1", "Gross domestic product per head: Chained volume measures") #Using the function created at the top to index the GDP per capita raw data
GDP_per_capita_processed = GDP_per_capita_processed.drop(columns="index")
GDP_per_capita_processed = GDP_per_capita_processed[["Time period and dataset code row", "Gross domestic product per head: Chained volume measures", "date time"]]

fig,ax = plt.subplots()
plt.plot(GDP_per_capita_processed["Time period and dataset code row"], GDP_per_capita_processed["Gross domestic product per head: Chained volume measures"], color="#206095") #Creating a time series of the indexed GDP per capita data
plt.title("GDP per capita (Q1 2012 = 100)", fontweight="bold", fontname="Arial", fontsize="12") #Creating a title and changing the parameters
desired_labels = ["2012 Q1", "2014 Q4", "2017 Q4", "2020 Q4", "2024 Q1"]
ax.set_xticks([GDP_per_capita_processed["Time period and dataset code row"].index[i] for i, label in enumerate(GDP_per_capita_processed["Time period and dataset code row"]) if label in desired_labels])
ax.set_xticklabels([label.split(" ")[1] + " " + label.split(" ")[0] for label in desired_labels], rotation=0)
plt.axhline(100, color="black", linewidth=0.5) #Line for formatting
ax.set_ylim(bottom=83, top=115); #Setting the y-axis parameters
customise_axes(ax) #Calling upon this function
plt.show()


#Chart 12 - Public sector net debt as a percentage of GDP


Debt_GDP_link  = "https://www.ons.gov.uk/generator?format=xls&uri=/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ruto/pusf"
file_name = "Public_debt_%_GDP"
ons_data_downloader(Debt_GDP_link, file_name, "data", 253)

Debt_GDP = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/Public_debt_%_GDP.csv")
Debt_GDP = Debt_GDP[["2024 Q1", "112"]]

fig,ax=plt.subplots()
Debt_GDP["Date"] = pd.to_datetime(Debt_GDP["2024 Q1"], format="%Y %b")
Debt_GDP["Date"] = Debt_GDP["Date"].dt.strftime("%b %Y")
ax.set_xticks(Debt_GDP["Date"].index)
ax.set_xticklabels(Debt_GDP["Date"])
Debt_GDP = Debt_GDP.drop("2024 Q1", axis=1)#Format the "Date" column as "Feb 2020" from "2020 FEB", and save it under a new variable name "Date"

plt.plot(Debt_GDP["Date"], Debt_GDP["112"], color="#206095") #Creating a plot of net debt as a % of GDP across time (when downloading data from the ONS website, after we skip rows to get to the )
plt.ylabel("%", rotation=0, loc="top", labelpad=-35) #y-axis label
plt.title("Net debt as a percentage of GDP", fontweight="bold", fontname="Arial", fontsize="12") #Title
customise_axes(ax) #Calling upon the function again to set chart parameters
desired_labels = ["May 1993", "May 2001", "May 2009", "May 2017", "May 2024"]
ax.set_xticks([Debt_GDP["Date"].index[i] for i, label in enumerate(Debt_GDP["Date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
ax.set_ylim(bottom=20, top=163) #Setting the y-axis porameters
plt.show()


#Chart 13 - Post-reccesion GDP indexed


post_recession_GDP_link = "https://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/realtimedatabaseforukgdpabmi/quarter1jantomar2024quarterlynationalaccounts/gdpinchainedvolumemeasuresrealtimedatabaseabmi.xlsx"
file_name = "post_recession_GDP"
ons_data_downloader(post_recession_GDP_link, file_name, "2018 - ", 2)

post_recession_GDP = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/post_recession_GDP.csv")
post_recession_GDP1 = post_recession_GDP.iloc[1:, [0, -1]]
post_recession_GDP1.columns = ["Time period and dataset code row", "Gross domestic product at market prices: Chained volume measure"]

post_recession_GDP1["Time period and dataset code row"] = post_recession_GDP1["Time period and dataset code row"].str.split(" ").str[1] + " " + post_recession_GDP1["Time period and dataset code row"].str.split(" ").str[0] 


recession_dates = ["1973 Q2", "1979 Q4", "1990 Q2", "2008 Q1", "2023 Q2"] 
combined_data = pd.DataFrame()
for date in recession_dates:
      post_recession_GDP_processed = indexed_time_series(post_recession_GDP1, date, "Gross domestic product at market prices: Chained volume measure")
      post_recession_GDP_processed[date] = post_recession_GDP_processed["Gross domestic product at market prices: Chained volume measure"]
      post_recession_GDP_processed = post_recession_GDP_processed.iloc[0:16, :].reset_index()
      post_recession_GDP_processed = post_recession_GDP_processed[["Time period and dataset code row", date]]
      combined_data = pd.concat([post_recession_GDP_processed, combined_data], axis=1)
combined_data = combined_data.reset_index()

fig,ax =plt.subplots()
colors = [(32/255, 96/255, 149/255), (39/255, 160/255, 204/255), (0/255, 60/255, 87/255), (17/255, 140/255, 123/255), (168/255, 189/255, 58/255)]
for i, date in enumerate(recession_dates):
    plt.plot(combined_data["index"], combined_data[date], label=date, color=colors[i], linewidth=2)
 
plt.legend(["Q2 1973", "Q4 1979", "Q2 1990", "Q1 2008", "Q2 2023"], loc="upper center", bbox_to_anchor=(0.5,-0.15), ncol=3, frameon=False)
plt.title("UK volume GDP recession path", fontweight="bold", fontname="Arial", fontsize="12")
plt.ylabel("Pre-recession Q = 100", rotation=0, loc="top", labelpad=-95)
plt.axhline(100, color="black", linewidth=0.5) #Grid lines for formatting
ax.set_ylim(bottom=91, top=105)
customise_axes(ax)
plt.xlabel("Quarters after pre-recession peak")
plt.show()
