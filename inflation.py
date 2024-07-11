#INFLATION CHARTS


#Below i will be importing the packages needed.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap 
from matplotlib.dates import DateFormatter, MonthLocator
import matplotlib.dates as mdatest
import datetime 


#Below i will be creating functions used throuhgout.

def customise_axes(ax): #This function is specifying desired parameters that can be called upon for charts
    ax.set_axisbelow(True) #This sets the axis lines below the data lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False) #These three remove the top, right and bottom boarders
    ax.grid(b=True, which = "major", axis = "x", color = "white")
    ax.grid(b=True, which = "major", axis = "y", color = "lightblue") #These two display just the horizontal gridlines
    plt.xlabel("") #Makes it so there is no x label (usually unneeded as it is just the date)

def wrap_ylabels(ax, width, break_long_words=False):
 labels = []
 for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=break_long_words))
 ax.set_yticklabels(labels) #This function allows labels (x or y) to be wrapped when they are too long
    
requests.packages.urllib3.disable_warnings() #This function allows us to download the data directly from the ONS website when called upon
def ons_data_downloader(link, output_file_name, tab_name, skip_rows):
    response = requests.get(link, verify=False)
    with open('data/raw/' + output_file_name + '.xlsx', 'wb') as file:
        file.write(response.content)
    data_tab = pd.read_excel('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/raw/' + output_file_name + '.xlsx', sheet_name=tab_name, skiprows=skip_rows) #First, downloading the raw excel file
#UPDATE: CHANGE FILE PATH TO OWN
    data_tab.to_csv('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/'  +  output_file_name + '.csv', index=False) #Then creating a modified CSV file that just has the tab of data we are interested in
#UPDATE: CHANGE FILE PATH TO OWN
    return    


#Chart 1 - CPIH and CPI 12 month percentage change


CPI_CPIH_12month_link = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceinflation/current/consumerpriceinflationdetailedreferencetables.xlsx" #This is the direct link to the data being used (not the URL)
#UPDATE - REPLACE WITH MOST UP-TO-DATE LINK FROM THE ONS WEBSITE
file_name = "CPI_CPIH_12month" #This is how the file will be stored in the processed and raw data
ons_data_downloader(CPI_CPIH_12month_link, file_name, "Table 1", 13) #The first part of the function calls upon the link name, the second part calls the file_name directly, the third is the name of the data tab we will be using from the raw data, the last number is the number of rows being skipped to get to the relevant data (to the first row above the data)
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins. 

CPI_CPIH_12month = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_CPIH_12month.csv") #This is reading in the data from you files and storing it as a dataframe
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_CPIH_12month_processed = CPI_CPIH_12month.iloc[ :37 ,[3, 5]] #The iloc function allows me to pull out the data i want from the 'Table 1' tab. the first number, (:37 in original) means i am using rows 0-36. The [3,5] means i only want to use columns 3 and 5
#This specific dataset shouldn't change the rows and columsn we need. However, if data doesn't output correctly, it could be a case that the data has changed amd this needs editing

date_range = pd.date_range(start='2021-05', end='2024-06', freq='M') #Here i have had to create my own date variable, as the format they are stored in from the raw data is unreadable by python
#UPDATE BOTH START AND END DATE BY ONE MONTH TO SHOW LATEST 3 YEARS. END DATE SHOULD BE A MONTH AHEAD THAN START MONTH.
date_range_str = date_range.strftime('%b %Y')
CPI_CPIH_12month_processed['date'] = date_range_str #Adding the new dates to our dataset. As a check - make sure new dataset dates allign with those in raw data

fig,ax = plt.subplots() #You'll see this throughout. Simply allows us to create plots

CPI_CPIH_12month_processed = CPI_CPIH_12month_processed.rename(columns={"L55O":"CPIH", " D7G7":"CPI"}) #Renaming the column names from their data label to actual names
#BEWARE: NOTICE THE SPACE BEFORE THE SECOND DATA LABEL. THIS IS BECAUSE IT IS LIKE THAT IN THE RAW DATA. IF ERROR OCCURS, CHECK FOR SPACES/CAPITAL LETTER CHANGES
plt.plot(CPI_CPIH_12month_processed["date"], CPI_CPIH_12month_processed["CPIH"],  color="#206095", linewidth="2.0")
plt.plot(CPI_CPIH_12month_processed["date"], CPI_CPIH_12month_processed["CPI"],  color="#27a0cc", linewidth="2.0") #These two lines of code are creating the lines for the chart. The colours are ONS house colours.
plt.title("Percentage change over 12 months", fontweight="bold", fontname="Arial", fontsize="12") #Creating a title
#UPDATE TITLE AS YOU NEED
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30) #Adding a y-axis label and formatting it to the top of the y-axis
plt.legend(["CPIH", "CPI"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False) #Adding a legend and formatting it below the x-axis, changing the number of columns and taking the frame off
customise_axes(ax) #Calling upon this function to add the desired parameters
ax.set_ylim(bottom=-0.1, top=12.5) #Setting the y-axis bottom and top limits. Change if needed to fit all data in
desired_labels = ["May 2021", "May 2022", "May 2023", "May 2024"]
#UPDATE THESE LABELS TO SHOW FOR THE LATEST MONTH OF DATA
ax.set_xticks([CPI_CPIH_12month_processed["date"].index[i] for i, label in enumerate(CPI_CPIH_12month_processed["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #Above we have set what desired labels we would like to show on the x-axis

plt.show() #Again this is used throughout, just calls the plot function.


#Chart 2 - CPI & CPIH indexed


CPI_CPIH_index_link = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceinflation/current/consumerpriceinflationdetailedreferencetables.xlsx"
#UPDATE - REPLACE WITH MOST UP-TO-DATE LINK FROM THE ONS WEBSITE
file_name = "CPI_CPIH_index"
ons_data_downloader(CPI_CPIH_index_link, file_name, "Table 1", 13)
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins. 

CPI_CPIH_index = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_CPIH_index.csv") 
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_CPIH_index_processed = CPI_CPIH_index.iloc[ :37, [2, 4]]
#This specific dataset shouldn't change the rows and columsn we need. However, if data doesn't output correctly, it could be a case that the data has changed amd this needs editing

date_range = pd.date_range(start='2021-05', end='2024-06', freq='M') #Here i have created my own date variable, as the format they are stored in from the raw data is unreadable by python
#UPDATE BY ONE MONTH FOR START AND END DATE TO SHOW LATEST 3 YEARS. NOTE: THE END MONTH SHOULD BE ONE MONTH AHEAD OF THE START DATE
date_range_str = date_range.strftime('%b %Y')
CPI_CPIH_index_processed['date'] = date_range_str #Adding the new dates to our dataset. As a check - make sure new dataset dates allign with those in raw data

fig,ax = plt.subplots()

CPI_CPIH_index_processed = CPI_CPIH_index_processed.rename(columns={"L522": "CPIH"," D7BT":"CPI"})
#As above, note the space before " D7BT". It may be a case this space isn't there next time, so ensure to check raw data if unsure
plt.plot(CPI_CPIH_index_processed["date"], CPI_CPIH_index_processed["CPIH"],  color="#206095", linewidth="2.0")
plt.plot(CPI_CPIH_index_processed["date"], CPI_CPIH_index_processed["CPI"],  color="#27a0cc", linewidth="2.0")
plt.title("CPIH and CPI (2015 = 100)", fontweight="bold", fontname="Arial", fontsize="12")
#UPDATE TITLE AS YOU NEED
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)
plt.legend(["CPIH", "CPI"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False)
customise_axes(ax)
ax.set_ylim(bottom=99.9, top=140)
desired_labels = ["May 2021", "May 2022", "May 2023", "May 2024"]
#UPDATE THESE LABELS TO SHOW FOR THE LATEST MONTH OF DATA
ax.set_xticks([CPI_CPIH_index_processed["date"].index[i] for i, label in enumerate(CPI_CPIH_index_processed["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0)

plt.show()


#Chart 3 - CPI, goods, services & CPI excluding energy, food, alcohol & tobacco (ability to choose which lines you want, see UPDATE note)


CPI_goods_services_link = "https://www.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2024/61f205aa&format=xls"
#UPDATE WITH THE DIRECT LINK TO THE CHART IN THE CPI BULLETIN (eg Fig 10 in the April 24 bulletin)
file_name = "CPI_goods_services"
ons_data_downloader(CPI_goods_services_link, file_name, "data", 6)
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins.

CPI_goods_services = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_goods_services.csv")
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH

CPI_goods_services_processed = CPI_goods_services.iloc[71:121, :].reset_index()
#UPDATE - THE FIRST NUMBERS (71:121 IN ORIGINAL) SHOWS WE ONLY WANT TO LOOK AT ROWS 71-120. EDITING THE FIRST NUMBER ALTERS WHERE THE TIME SERIES BEGINS, WITH THE FINAL NUMBER NEEDING +1 EACH MONTH TO SHOW FOR LATEST DATA. (AS REFERENCE, STARTING AT 71-121 SHOWED LATEST 4 YEARS)

fig,ax = plt.subplots()

CPI_goods_services_processed = CPI_goods_services_processed.rename(columns={"Unnamed: 0": "date"})
plt.plot(CPI_goods_services_processed["date"], CPI_goods_services_processed["CPI"], color="#206095", linewidth="2.0", linestyle="dotted")
plt.plot(CPI_goods_services_processed["date"], CPI_goods_services_processed["Goods"], color="#27a0cc", linewidth="2.0")
plt.plot(CPI_goods_services_processed["date"], CPI_goods_services_processed["Services"], color="#003c57", linewidth="2.0")
plt.plot(CPI_goods_services_processed["date"], CPI_goods_services_processed["CPI excl energy, food, alcohol & tobacco"], color="#118c7b", linewidth="2.0")
#UIf you only want certain lines showing, e.g. you don't want goods in the chart, comment that line of code relating to it (using a #) out and remove it from the legend
plt.title("CPI goods, services and core inflation", fontweight="bold", fontname="Arial", fontsize="12")
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)
plt.legend(["CPI","Goods","Services","CPI excl energy, food, alcohol & tobacco"], loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False)
customise_axes(ax)
plt.axhline(0, color="black", linewidth=0.5) #Black line at x=0 for formatting
ax.set_ylim(bottom=-2.6, top=18)
desired_labels = ["May 2020", "May 2021", "May 2022", "May 2023", "May 2024"]
#UPDATE THESE LABELS TO SHOW FOR THE LATEST MONTH
ax.set_xticks([CPI_goods_services_processed["date"].index[i] for i, label in enumerate(CPI_goods_services_processed["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0)

plt.show()

#Chart 4 - CPI headline, 15% trimmed mean, median, core & services


CPI_QEC_link = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/uksectoraccounts/articles/quarterlyeconomiccommentary/januarytomarch2024/31b2b88a&format=xls"
#UPDATE - REPLACE WITH MOST UP-TO-DATE DIRECT LINK TO THE DATA FROM THE ONS WEBSITE (Fig 5 in June release)
file_name = "CPI_QEC"
ons_data_downloader(CPI_QEC_link, file_name, "data", 6)
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins.

CPI_QEC = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPI_QEC.csv")
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPI_QEC_processed = CPI_QEC.iloc[208:273, :].reset_index()
#UPDATE ROW NUMBERS ACCORDINGLY TO ADD MOST RECENT DATA AND ALTER TIME SERIES

CPI_QEC_processed["date"] = pd.to_datetime(CPI_QEC_processed["Unnamed: 0"], format="%b-%Y")#Format the "date" column as "Feb 2020"
CPI_QEC_processed["date"] = CPI_QEC_processed["date"].dt.strftime("%b %Y")#Set "date" as the new x-axis
ax.set_xticks(CPI_QEC_processed["date"].index)
ax.set_xticklabels(CPI_QEC_processed["date"])
CPI_QEC_processed = CPI_QEC_processed.drop("Unnamed: 0", axis=1) #The raw data is stored as Y M, e.g. 2020 Feb. For formatting, this function creates a new variable called 'date', and switches it to Feb 2020

fig,ax = plt.subplots()

plt.plot(CPI_QEC_processed["date"], CPI_QEC_processed["Headline"], color="#206095", linewidth="2.0", linestyle="dotted")
plt.plot(CPI_QEC_processed["date"], CPI_QEC_processed["15% trimmed mean"], color="#27a0cc", linewidth="2.0")
plt.plot(CPI_QEC_processed["date"], CPI_QEC_processed["Median"], color="#003c57", linewidth="2.0")
plt.plot(CPI_QEC_processed["date"], CPI_QEC_processed["Core"], color="#118c7b", linewidth="2.0")
plt.plot(CPI_QEC_processed["date"], CPI_QEC_processed["Services"], color="#a8bd3a", linewidth="2.0")
#if you only want to show certain lines, e.g. you don't want to show services, comment the plt.plot function out using #, take it out the legend and run the code as normal
plt.title("CPI core inflation", fontweight="bold", fontname="Arial", fontsize="12")
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)
plt.legend(["Headline", "15% trimmed mean", "Median", "Core", "Services"],loc="upper center", bbox_to_anchor=(0.5,-0.07), ncol=2, frameon=False)
customise_axes(ax)
ax.set_ylim(bottom=-0.1, top=12.5) 
desired_labels = ["May 2020", "May 2021", "May 2022", "May 2023", "May 2024"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST MONTH
ax.set_xticks([CPI_QEC_processed["date"].index[i] for i, label in enumerate(CPI_QEC_processed["date"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0)

plt.show()


#Chart 5 - Output and input PPI
#This chart is using data from two different data sources. Essentially, you will need to update the usual stuff twice

PPI_link = "https://www.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/bulletins/producerpriceinflation/may2024/9bd9f5b8&format=xls"
#UPDATE WITH THE LATEST DATA LINK 
file_name = "PPI"
ons_data_downloader(PPI_link, file_name, "data", 6) 
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins.
PPI_data = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/PPI.csv") 
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH

CPIH_link = "https://www.ons.gov.uk/generator?format=xls&uri=/economy/inflationandpriceindices/timeseries/l55o/mm23"
#UPDATE WITH THE LATEST DATA
file_name ="CPIH" 
ons_data_downloader(CPIH_link, file_name, "data", 486) 
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins.
CPIH_data = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPIH.csv")
#UPDATE WITH LINK TO OWN PROCESSED DATA FILE PATH
CPIH_data.columns = ["CPIH_MAR", "CPIH"] # Rename the columns of CPIH data to avoid duplicate column names


PPI_CPIH_data = pd.concat([PPI_data, CPIH_data], axis=1) # Concatenate the two datasets horizontally (joining the two datasets and meerging them into one under a new dataframe)
PPI_CPIH_data = PPI_CPIH_data[["Unnamed: 0", "Input PPI", "Output PPI", "CPIH"]] #List of variables names in joined dataset
PPI_CPIH_processed = PPI_CPIH_data.iloc[60: 121, :].reset_index()
#UPDATE AS DESIRED. CHANGING '60' WILL ALTER THE LENGTH OF THE TIME SERIES, HAVING IT AT 0 WOULD SHOW ALL THE DATA FROM 2014. THE LAST NUMBER (121 IN ORIGINAL) WILL NEED +1 EACH PERIOD TO SHOW LATEST DATA
PPI_CPIH_processed = PPI_CPIH_processed.rename(columns={"Unnamed: 0":"date"})

fig,ax1 = plt.subplots() #notice the ax1 instead of the usual ax. Shows we are going to be operating on two different axis.

ax1.set_ylabel('PPI %', fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)
ax1.plot(PPI_CPIH_processed["date"], PPI_CPIH_processed["Input PPI"], color="#206095", linewidth="2.0", label='Input PPI')
ax1.plot(PPI_CPIH_processed["date"], PPI_CPIH_processed["Output PPI"], color="#27a0cc", linewidth="2.0", label='Output PPI')
ax1.tick_params(axis='y')
ax1.grid(b=True, which = "major", axis = "x", color = "white")
ax1.grid(b=True, which = "major", axis = "y", color = "lightblue")
ax1.set_axisbelow(True)
ax1.spines['bottom'].set_visible(False) 
ax1.spines['top'].set_visible(False)
plt.legend(["Input PPI", "Output PPI", "CPIH"], loc="upper center", bbox_to_anchor=(0.35,-0.07), ncol=2, frameon=False) 

desired_labels = ["May-19", "May-20", "May-21", "May-22", "May-23", "May-24"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST DATA
ax1.set_xticks([PPI_CPIH_processed["date"].index[i] for i, label in enumerate(PPI_CPIH_processed["date"]) if label in desired_labels])
ax1.set_xticklabels(desired_labels, rotation=0)

#The above is setting the parameters for ax1, our primary axis, where the PPI data will be measured. Next, ax2, will be our secondary axis, measuring the CPIH

ax2 = ax1.twinx()  #instantiate a second axes that shares the same x-axis

ax2.set_ylabel('CPIH %', fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=30)
ax2.yaxis.set_label_coords(1.05, 1.06)
ax2.plot(PPI_CPIH_processed["date"], PPI_CPIH_processed["CPIH"], color="#003c57", linewidth="2.0", linestyle="dotted", label='CPIH')
ax2.tick_params(axis='y')
fig.tight_layout() 
plt.title("Output & Input PPI", fontweight="bold", fontname="Arial", fontsize="12")
#Update title as required
ax2.set_axisbelow(True)
ax2.spines['bottom'].set_visible(False) 
ax2.spines['top'].set_visible(False)
plt.legend(["CPIH"], loc="upper center", bbox_to_anchor=(0.72,-0.07), ncol=2, frameon=False)
ax2.set_ylim(bottom =-0.01, top=10)
desired_labels = ["May-19", "May-20", "May-21", "May-22", "May-23", "May-24"]
#UPDATE THESE LABELS EACH MONTH TO SHOW FOR THE LATEST MONTH
ax2.set_xticks([PPI_CPIH_processed["date"].index[i] for i, label in enumerate(PPI_CPIH_processed["date"]) if label in desired_labels])
ax2.set_xticklabels(desired_labels, rotation=0) 

plt.show()


#Chart 6 - CPIH annual contributions (% change on a year earlier)


CPIH_annual_link = "https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceinflation/current/consumerpriceinflationdetailedreferencetables.xlsx"
#UPDATE WITH LATEST DATA LINK 
file_name  = "CPIH_annual"
ons_data_downloader(CPIH_annual_link, file_name, "Table 2", 44) 
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins.

CPIH_annual = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPIH_annual.csv")
#UPDATE WITH LINK TO OWN DATA FILE PATH
CPIH_annual_processed = CPIH_annual.iloc[24:25, 1:14] 
#using an iloc function to say we only want the data between rows 24 and 25, and between columns 1 to 14. This won't need updating unless the formatting of the raw data changes


CPIH_annual_processed = CPIH_annual_processed.T
CPIH_annual_processed.reset_index(inplace=True)
CPIH_annual_processed.columns = CPIH_annual_processed.iloc[0]
CPIH_annual_processed.drop(index=0, inplace=True) #Transposing the data and replacing the index

new_names = ["Food and non-alcoholic beverages", "Alcoholic beverages and tobacco", "Clothing and footwear", "Housing, water, electricity, gas & other fuels",
             "Furtniture, household equipment & routine maintenance", "Health", "Transport", "Communication", "Recreation and culture ", "Education",
             "Restaurants and hotels", "Miscellaneous goods and services"] #Adding all the variable names in
CPIH_annual_processed.index = new_names
CPIH_annual_processed.reset_index(inplace=True)
CPIH_annual_processed.columns = ['Category', 'Index', 'Latest month'] #Replacing all the old variable names with the appropriate ones

fig, ax = plt.subplots()

CPIH_annual_processed.plot("Category", kind="barh", stacked=False, ax=ax, color="#206095")
plt.xlabel("Percentage points")
ax.set_frame_on(False)
plt.ylabel("") 
plt.title("Percentage change from the same month a year ago: May 2024", fontweight="bold", fontname="Arial", fontsize="12")
#Update title as required
ax.set_xlim(left=-4, right=9);
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.5, color="black")
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue")
ax.set_axisbelow(True)
wrap_ylabels(ax, 43) #Calling upon the wrapping function, after 43 characters the labels will go to the next line
ax.tick_params(axis='y', labelsize=8) #Label size
ax.legend().set_visible(False) #Turning off the legend

plt.show()


# Chart 7 - CPIH monthly changes


CPIH_monthly_link = "https://www.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2024/c8b7e3c9&format=xls" 
#UPDATE WITH LATEST DATA
file_name = "CPIH_monthly" #How the data is going to be stored in the raw and processes data file
ons_data_downloader(CPIH_monthly_link, file_name, "data", 6)  
#Usually this won't need updating. If you run into an error, check the tab name hasn't been changed, or where the data begins.
                    
CPIH_monthly = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/CPIH_monthly.csv")
#UPDATE WITH LINK TO OWN DATA FILE PATH      
CPIH_monthly_processed = CPIH_monthly.rename(columns={"Unnamed: 0":"Category"})       
                
fig, ax = plt.subplots()    

CPIH_monthly_processed.plot("Category", kind="barh", ax=ax, stacked=False, color="#206095")
plt.xlabel("Percentage points")
ax.set_frame_on(False)
plt.ylabel("")
plt.title("Monthly change in contributions: May 2024", fontweight="bold", fontname="Arial", fontsize="12")
#Update title as required
ax.set_xlim(left=-0.5, right=0.21);
plt.axvline(0, color="black", linewidth=0.5)
plt.axhline(-0.5, color="black")
ax.grid(b=True, which = "major", axis = "y", color = "white")
ax.grid(b=True, which = "major", axis = "x", color = "lightblue")
ax.set_axisbelow(True)
wrap_ylabels(ax, 43) #Labels will begin wrapping after 43 characters
ax.tick_params(axis='y', labelsize=8) #Chainging the label size
ax.legend().set_visible(False)

plt.show()
