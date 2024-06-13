import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap 
from matplotlib.dates import DateFormatter, MonthLocator
import matplotlib.dates as mdates #Importing the packages needed throughout

def customise_axes(ax): #This code is defining a function, specifying desired parameters that can be called upon for charts
    ax.set_axisbelow(True) #This sets the axis lines below the data lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False) #These three remove the top, right and bottom boarders
    ax.grid(b=True, which = "major", axis = "x", color = "white")
    ax.grid(b=True, which = "major", axis = "y", color = "lightblue") #These two create the horizontal gridlines
    plt.xlabel("") #Makes it so there is no x label (usually unneeded as it is just the date)
    
requests.packages.urllib3.disable_warnings() #Here we are creating a function that allows us to download the data directly from the ONS website.
def ons_data_downloader(link, output_file_name, tab_name, skip_rows):
    response = requests.get(link, verify=False)
    with open('data/raw/' + output_file_name + '.xlsx', 'wb') as file:
        file.write(response.content)
    data_tab = pd.read_excel('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/raw/' + output_file_name + '.xlsx', sheet_name=tab_name, skiprows=skip_rows) #First, downloading the raw excel file
#UPDATE: CHANGE FILE PATH TO OWN COMPUTER. CREATE ONE FOR RAW AND PROCESSED DATA
    data_tab.to_csv('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/'  +  output_file_name + '.csv', index=False) #Then creating a modified CSV file that just has the tab of data we are interested in
#UPDATE: Change file path to own computer.
    return    

def wrap_ylabels(ax, width, break_long_words=False):
 labels = []
 for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=break_long_words))
 ax.set_yticklabels(labels) #A function that allows labels to be wrapped when they are long

#Chart 1 - CPIH and CPI 12 month change

CPI_CPIH_12month_link = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceinflation/current/consumerpriceinflationdetailedreferencetables.xlsx" #This is the direct link to the data being used
#UPDATE - REPLACE WITH MOST UP-TO-DATE LINK FROM THE ONS WEBSITE
file_name = "CPI_CPIH_12month" #This is how the file will be stored in the processed and raw data
ons_data_downloader(CPI_CPIH_12month_link, file_name, "Table 1", 13) #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data

CPI_CPIH_12month = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_CPIH_12month.csv") #This is reading in the data and storing it as a dataframe
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_CPIH_12month = CPI_CPIH_12month.iloc[ :37 ,[3, 5]] #The iloc function allows me to pull out the data i want from the 'Table 1' tab. the ':37' means i am using all the rows to 37. The [3,5] means i only want to use columns 3 and 5

date_range = pd.date_range(start='2021-04', end='2024-05', freq='M') #Here i have had to create my own date variable, as the format they are stored in from the raw data is unreadable by python
#UPDATE BOTH START AND END DATE BY ONE MONTH TO SHOW LATEST 3 YEARS. END DATE SHOULD BE A MONTH AHEAD.
date_range_str = date_range.strftime('%b %Y')# Create a new column 'date' in the dataframe
CPI_CPIH_12month['date'] = date_range_str #Adding the new dates to our dataset. As a check - make sure new dataset dates allign with those in raw data

fig,ax = plt.subplots()
plt.plot(CPI_CPIH_12month["date"], CPI_CPIH_12month["L55O"],  color="#206095", linewidth="2.0")
plt.plot(CPI_CPIH_12month["date"], CPI_CPIH_12month[" D7G7"],  color="#27a0cc", linewidth="2.0") #These two lines of code are creating the line graphs for CPIH, then CPI. The dataframe is stored as the datacode names
plt.title("Percentage change over 12 months", fontweight="bold", fontname="Arial", fontsize="12") #Creating a title and changing the formatting
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30) #Adding a y-axis label and changing the formatting
plt.legend(["CPIH", "CPI"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Adding a legend and changing the formatting
customise_axes(ax) #Calling upon this function to add the desired parameters
ax.set_ylim(bottom=-0.1, top=12.5) #Setting the y-axis porameters
desired_labels = ["Apr 2021", "Apr 2022", "Apr 2023", "Apr 2024"]
#UPDATE these labels each month to show for the latest month
ax.set_xticks([CPI_CPIH_12month["date"].index[i] for i, label in enumerate(CPI_CPIH_12month["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.show()


#Chart 2 - CPI & CPIH indexed


CPI_CPIH_index_link = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceinflation/current/consumerpriceinflationdetailedreferencetables.xlsx" #This is the direct link to the data being used
#UPDATE - REPLACE WITH MOST UP-TO-DATE LINK FROM THE ONS WEBSITE
file_name = "CPI_CPIH_index" #This is how the file will be stored in the processed and raw data
ons_data_downloader(CPI_CPIH_index_link, file_name, "Table 1", 13) #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data

CPI_CPIH_index = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_CPIH_index.csv")  #This is reading in the data and storing it as a dataframe
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_CPIH_index = CPI_CPIH_index.iloc[ :37, [2, 4]]  #The iloc function allows me to pull out the data i want from the 'Table 1' tab. the ':37' means i am using all the rows to 37. The [2,4] means i only want to use columns 3 and 5

date_range = pd.date_range(start='2021-04', end='2024-05', freq='M') #Here i have had to create my own date variable, as the format they are stored in from the raw data is unreadable by python
#UPDATE by one month on each end to show latest 3 years. The end date should always be one month ahead of the start date.
date_range_str = date_range.strftime('%b %Y')# Create a new column 'date' in the dataframe
CPI_CPIH_index['date'] = date_range_str #Adding the new dates to our dataset. As a check - make sure new dataset dates allign with those in raw data

fig,ax = plt.subplots()
plt.plot(CPI_CPIH_index["date"], CPI_CPIH_index["L522"],  color="#206095", linewidth="2.0")
plt.plot(CPI_CPIH_index["date"], CPI_CPIH_index[" D7BT"],  color="#27a0cc", linewidth="2.0") #These two lines of code are creating the line graphs for CPIH, then CPI. The dataframe is stored as the datacode names
plt.title("CPIH and CPI (2015 = 100)", fontweight="bold", fontname="Arial", fontsize="12") #Creating a title and changing the formatting
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30) #Adding a y-axis label and changing the formatting
plt.legend(["CPIH", "CPI"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Adding a legend and changing the formatting
customise_axes(ax) #Calling upon this function to add the desired parameters
ax.set_ylim(bottom=99.9, top=140) #Setting the y-axis porameters
desired_labels = ["Apr 2021", "Apr 2022", "Apr 2023", "Apr 2024"]
#UPDATE these labels each month to show for the latest month
ax.set_xticks([CPI_CPIH_12month["date"].index[i] for i, label in enumerate(CPI_CPIH_12month["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.show()


#Chart 3 - CPI, goods, services & CPI excluding energy, food, alcohol & tobacco (ability to choose which lines you want, see UPDATE note)


CPI_link = "https://www.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/bulletins/consumerpriceinflation/april2024/78e93de2&format=xls" #This is the direct link to the data being used
#UPDATE with the link to the CPI chart in the bulletin (eg Fig 10 in the April 24 bulletin)
file_name = "CPI_goods_services" #This is how the file will be stored in the processed and raw data
ons_data_downloader(CPI_link, file_name, "data", 6) #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data

CPI_goods_services = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_goods_services.csv") #Reading in the processed data
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_goods_services = CPI_goods_services[["Unnamed: 0", "CPI", "Goods", "Services", "CPI excl energy, food, alcohol & tobacco"]] #Naming all the variables in the processed data

CPI_goods_services_processed = CPI_goods_services.iloc[71:121, :].reset_index() #Using and iloc function to isolate the time frame we want to look at
#UPDATE - the numbers 71-121 show we only want to look at the data in this time frame. Need to update +1 on both numbers to look at most recent 4 years of data as and when updated

fig,ax = plt.subplots()
plt.plot(CPI_goods_services_processed["Unnamed: 0"], CPI_goods_services_processed["CPI"], color="#206095", linewidth="2.0", linestyle="dotted")
plt.plot(CPI_goods_services_processed["Unnamed: 0"], CPI_goods_services_processed["Goods"], color="#27a0cc", linewidth="2.0")
plt.plot(CPI_goods_services_processed["Unnamed: 0"], CPI_goods_services_processed["Services"], color="#003c57", linewidth="2.0")
plt.plot(CPI_goods_services_processed["Unnamed: 0"], CPI_goods_services_processed["CPI excl energy, food, alcohol & tobacco"], color="#118c7b", linewidth="2.0") #These lines of code create all the lines for the line graph.
#UPDATE - If you only want certain lines showing, e.g. you don't want goods in the chart, comment that line of code relating to it out and remove it from the legend
plt.title("CPI goods, services and core inflation", fontweight="bold", fontname="Arial", fontsize="12") #Creating a title and changing the formatting
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30) #y-axis label and the parameters to position it
plt.legend(["CPI","Goods","Services","CPI excl energy, food, alcohol & tobacco"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Adding a legend and changing the formatting
customise_axes(ax) #Calling upon this function to add the desired parameters
plt.axhline(0, color="black", linewidth=0.5) #Black line at x=0 for formatting
ax.set_ylim(bottom=-2.6, top=18) #Setting the y-axis porameters
desired_labels = ["Apr 2020", "Apr 2021", "Apr 2022", "Apr 2023", "Apr 2024"]
#UPDATE these labels each month to show for the latest month
ax.set_xticks([CPI_goods_services_processed["Unnamed: 0"].index[i] for i, label in enumerate(CPI_goods_services_processed["Unnamed: 0"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.show()

#Chart 4 - CPI headline, 15% trimmed mean, median, core & services


CPI_link2 = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/uksectoraccounts/articles/quarterlyeconomiccommentary/octobertodecember2023/62482606&format=xls" #This is the direct link to the data being used
#UPDATE - REPLACE WITH MOST UP-TO-DATE LINK FROM THE ONS WEBSITE
file_name = "CPI_QEC" #This is how the file will be stored in the processed and raw data
ons_data_downloader(CPI_link2, file_name, "data", 6) #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data

CPI_QEC = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_QEC.csv") #Reading in the processed data
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_QEC = CPI_QEC[["Unnamed: 0","Headline", "15% trimmed mean","Median", "Core", "Services"]] #Name of the variables being stored in the dataframe
CPI_QEC_processed = CPI_QEC.iloc[217:273, :].reset_index() #Here i am telling python, i only want to download the data between rows 217-273.
#UPDATE - at a minimum, the second number must increase by 3 to include latest data (as updated quarterly). Change the first number as desired to show a shorter or longer time period

import datetime #Convert "Unnamed: 0" column to datetime format
CPI_QEC_processed["Date"] = pd.to_datetime(CPI_QEC_processed["Unnamed: 0"], format="%Y %b")#Format the "Date" column as "Feb 2020"
CPI_QEC_processed["Date"] = CPI_QEC_processed["Date"].dt.strftime("%b %Y")#Set "Date" as the new x-axis
ax.set_xticks(CPI_QEC_processed["Date"].index)
ax.set_xticklabels(CPI_QEC_processed["Date"])#Remove "Unnamed: 0" column
CPI_QEC_processed = CPI_QEC_processed.drop("Unnamed: 0", axis=1) #The raw data is stored as Y M, e.g. 2020 Feb. For formatting, this function creates a new variable called 'date', and switches it to Feb 2020

fig,ax = plt.subplots()
plt.plot(CPI_QEC_processed["Date"], CPI_QEC_processed["Headline"], color="#206095", linewidth="2.0", linestyle="dotted")
plt.plot(CPI_QEC_processed["Date"], CPI_QEC_processed["15% trimmed mean"], color="#27a0cc", linewidth="2.0")
plt.plot(CPI_QEC_processed["Date"], CPI_QEC_processed["Median"], color="#003c57", linewidth="2.0")
plt.plot(CPI_QEC_processed["Date"], CPI_QEC_processed["Core"], color="#118c7b", linewidth="2.0")
plt.plot(CPI_QEC_processed["Date"], CPI_QEC_processed["Services"], color="#a8bd3a", linewidth="2.0") #These are creating all the lines needed for the chart
#UPDATE : if you only want to show certain lines, e.g. you don't want to show services, comment the plt.plot function out using #, take it out the legend and run the code as normal
plt.title("CPI core inflation", fontweight="bold", fontname="Arial", fontsize="12")#Creating title and changing formatting
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30) #y-axis label and the parameters to position it
plt.legend(["Headline", "15% trimmed mean", "Median", "Core", "Services"],loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Legend placement, number of columns and taking the frame off
customise_axes(ax) #Calling upon our custom function
ax.set_ylim(bottom=-0.1, top=12.5) #Setting the y-axis porameters
desired_labels = ["Feb 2020", "Feb 2021", "Feb 2022", "Feb 2023", "Feb 2024"]
#UPDATE these labels each month to show for the latest month
ax.set_xticks([CPI_QEC_processed["Date"].index[i] for i, label in enumerate(CPI_QEC_processed["Date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis
plt.show()


#Chart 5 - Output and input PPI


PPI_link = "https://www.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/bulletins/producerpriceinflation/april2024/b6ad7e4b&format=xls" #This is the direct link to the data being used
#UPDATE WITH THE LATEST DATA
file_name = "PPI" #How the data is going to be saved in your files
ons_data_downloader(PPI_link, file_name, "data", 6)  #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data
PPI_data = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/PPI.csv") 
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
PPI_data = PPI_data[["Unnamed: 0", "Input PPI", "Output PPI"]] #List of the variable names

CPIH_link = "https://www.ons.gov.uk/generator?format=xls&uri=/economy/inflationandpriceindices/timeseries/l55o/mm23" #link to the latest CPIH data
#UPDATE WITH THE LATEST DATA
file_name ="CPIH" #How the data will be stored in your files
ons_data_downloader(CPIH_link, file_name, "data", 486)  #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data
CPIH_data = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPIH.csv")
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPIH_data = CPIH_data[["2014 MAR","1.5"]] #Name of variables being stored in the dataframe
CPIH_data.columns = ["CPIH_MAR", "CPIH"] # Rename the columns of CPIH data to avoid duplicate column names

PPI_CPIH_data = pd.concat([PPI_data, CPIH_data], axis=1) # Concatenate the two datasets horizontally (axis=1)
PPI_CPIH_data = PPI_CPIH_data[["Unnamed: 0", "Input PPI", "Output PPI", "CPIH"]] #List of variables names in joined dataset
PPI_CPIH_processed = PPI_CPIH_data.iloc[60: , :].reset_index() #Only using the data from row 60 onwards
#UPDATE AS DESIRED. CHANGING '60' WILL ALTER THE LENGTH OF THE TIME SERIES, HAVING IT AT 0 WOULD SHOW ALL THE DATA FROM 2014

fig,ax1 = plt.subplots()
ax1.set_ylabel('PPI %', fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30) #Creating our primary axis label
ax1.plot(PPI_CPIH_processed["Unnamed: 0"], PPI_CPIH_processed["Input PPI"], color="#206095", linewidth="2.0", label='Input PPI')
ax1.plot(PPI_CPIH_processed["Unnamed: 0"], PPI_CPIH_processed["Output PPI"], color="#27a0cc", linewidth="2.0", label='Output PPI')# Creating the lines for the PPI data
ax1.tick_params(axis='y')
ax1.grid(b=True, which = "major", axis = "x", color = "white")
ax1.grid(b=True, which = "major", axis = "y", color = "lightblue") #Creates our gridlines
ax1.set_axisbelow(True) #Sets axis below the data
ax1.spines['bottom'].set_visible(False) 
ax1.spines['top'].set_visible(False)#Removing top and bottom border for formatting
plt.legend(["Input PPI", "Output PPI", "CPIH"], loc="upper center", bbox_to_anchor=(0.35,-0.07), ncol=2, frameon=False) #Setting our legend

desired_labels = ["Apr 2019", "Apr 2020", "Apr 2021", "Apr 2022", "Apr 2023", "Apr 2024"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST DATA
ax1.set_xticks([PPI_CPIH_processed["Unnamed: 0"].index[i] for i, label in enumerate(PPI_CPIH_processed["Unnamed: 0"]) if label in desired_labels])
ax1.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.set_ylabel('CPIH %', fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=30)  # we already handled the x-label with ax1
ax2.yaxis.set_label_coords(1.05, 1.06) #Moving secondary axis label above the axis
ax2.plot(PPI_CPIH_processed["Unnamed: 0"], PPI_CPIH_processed["CPIH"], color="#003c57", linewidth="2.0", linestyle="dotted", label='CPIH') #Creating our line for the CPIH data
ax2.tick_params(axis='y')
fig.tight_layout() 
plt.title("Output & Input PPI", fontweight="bold", fontname="Arial", fontsize="12")#Creating a title and changing the formatting
ax2.set_axisbelow(True) #Setting axis lines below data lines
ax2.spines['bottom'].set_visible(False) 
ax2.spines['top'].set_visible(False) #Repeating the formatting as we have two seperate axis we want to apply it to (primary and secondary)
plt.legend(["CPIH"], loc="upper center", bbox_to_anchor=(0.72,-0.07), ncol=2, frameon=False) #Adding the CPIH to the legend, and moving it so it alligns with the other legend
ax2.set_ylim(bottom =-0.01, top=10) #Setting the secondary axis limits
desired_labels = ["Apr 2019", "Apr 2020", "Apr 2021", "Apr 2022", "Apr 2023", "Apr 2024"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST MONTH
ax2.set_xticks([PPI_CPIH_processed["Unnamed: 0"].index[i] for i, label in enumerate(PPI_CPIH_processed["Unnamed: 0"]) if label in desired_labels])
ax2.set_xticklabels(desired_labels, rotation=0) #Doing the labels again as we have to do it for both axis
plt.show()


#Chart 6 - CPIH annual contributions (% change on a year earlier)


CPIH_annual_link = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceinflation/current/consumerpriceinflationdetailedreferencetables.xlsx" #This is the direct link to the data being used
#UPDATE WITH LATEST DATA
file_name  = "CPIH_annual" #How the file is going to be stored in the raw and processed files
ons_data_downloader(CPIH_annual_link, file_name, "Table 2", 44) #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data

CPIH_annual = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPIH_annual.csv") #where we are reading the data in from
#UPDATE WITH LINK TO OWN DATA FILE PATH
CPIH_annual_processed = CPIH_annual.iloc[24:25, 1:14] #using an iloc function to say we only want the data between rows 24 and 25, and between columns 1 to 14


CPIH_annual_processed = CPIH_annual_processed.T
CPIH_annual_processed.reset_index(inplace=True)
CPIH_annual_processed.columns = CPIH_annual_processed.iloc[0]
CPIH_annual_processed.drop(index=0, inplace=True) #Transposing the data and replacing the index

new_names = ["Food and non-alcoholic beverages", "Alcoholic beverages and tobacco", "Clothing and footwear", "Housing, water, electricity, gas & other fuels",
             "Furtniture, household equipment & routine maintenance", "Health", "Transport", "Communication", "Recreation and culture ", "Education",
             "Restaurants and hotels", "Miscellaneous goods and services"] #Adding all the variable names in
CPIH_annual_processed.index = new_names
CPIH_annual_processed.reset_index(inplace=True)
CPIH_annual_processed.columns = ['Category', 'Index', 'April 2024']
#UPDATE THE MONTH TO LATEST MONTH

fig, ax = plt.subplots()
CPIH_annual_processed.plot("Category", kind="barh", stacked=False, ax=ax, color="#206095") #Creating the barplot
plt.xlabel("Percentage points") #x-axis label
ax.set_frame_on(False) #Removing chart frame
plt.ylabel("") #No y-label needed hence left blank
plt.title("Percentage change from the same month a year ago: April 2024", fontweight="bold", fontname="Arial", fontsize="12") #Title and formatting
ax.set_xlim(left=-4, right=9); #y-axis scale
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.5, color="black") #Grid lines for formatting
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue") #Gridlines for formatting
ax.set_axisbelow(True) #Setting axis below frame
wrap_ylabels(ax, 43) #Calling upon the wrapping function, after 43 characters the labels will go to the next line
ax.tick_params(axis='y', labelsize=8) #Label size
ax.legend().set_visible(False) #Turning off the legend
plt.show()


# Chart 7 - CPIH monthly changes


CPIH_monthly_link = "https://www.beta.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/bulletins/consumerpriceinflation/april2024/569af73c&format=xls" #This is the direct link to the data being used
#UPDATE WITH LATEST DATA
file_name = "CPIH_monthly" #How the data is going to be stored in the raw and processes data file
ons_data_downloader(CPIH_monthly_link, file_name, "data", 6)  #The first part of the function calls upon the link name, the second part calls upon the file name, the third is the name of the data tab we will be using, the last number is the number of rows being skipped to get to the relevant data
                    
CPIH_monthly = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPIH_monthly.csv") #Reading in the data from our files
#UPDATE WITH LINK TO OWN DATA FILE PATH
CPIH_monthly = CPIH_monthly[["Unnamed: 0", "Percentage points"]] #Creating our dataframe              
                
fig, ax = plt.subplots()    
CPIH_monthly.plot("Unnamed: 0", kind="barh", ax=ax, stacked=False, color="#206095") #Creating the bar plot
plt.xlabel("Percentage points") #x-axis label
ax.set_frame_on(False) #Removing chart frame
plt.ylabel("") #No y-label needed hence left blank
plt.title("Monthly change in contributions: April 2024", fontweight="bold", fontname="Arial", fontsize="12") #Title and formatting
ax.set_xlim(left=-0.5, right=0.21); #y-axis scale
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.5, color="black") #Grid lines for formatting
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue") #Gridlines for formatting
ax.set_axisbelow(True) #Setting axis below frame
wrap_ylabels(ax, 43) #Labels will begin wrapping after 43 characters
ax.tick_params(axis='y', labelsize=8) #Chainging the label size
ax.legend().set_visible(False) #Turning off the legend
plt.show()