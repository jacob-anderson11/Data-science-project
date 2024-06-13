import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap 
from matplotlib.dates import DateFormatter, MonthLocator #Importing the packages needed throughout

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

def customise_axes(ax):
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False) 
    ax.grid(b=True, which = "major", axis = "x", color = "white")
    ax.grid(b=True, which = "major", axis = "y", color = "lightblue")
    plt.xlabel("") #This code is defining a function, specifying desired parameters that can be called upon for charts
    
    
#Chart 1 - Real vs nominal household disposable income - Quarterly change


nominal_real_income_link = "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/uksectoraccounts/datasets/quarterlysectoraccounts/quarter4octtodec2023/quarterlysectoraccounts2023q4.xlsx" #This is the link directly to the data from the ONS website
#UPDATE WITH LATEST LINK DIRECTLY TO DATA FILE
file_name = "nominal_real_income" #This is how the data will be stored as in the raw and processed file

ons_data_downloader(nominal_real_income_link, file_name, "HH_2", 452) #This code downloads the data from the ONS website, saves it under a specific name, with the last number being the number of rows skipped so only the necessary data is processed. 'HH_2' is the name of the tab the data is downloaded from
nominal_real_income = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/nominal_real_income.csv") #Saving the data in this specific folder
#UPDATE WITH LINK TO OWN DATA FILE PATH
nominal_real_income_processed = nominal_real_income.iloc[259 : 275 ,[0,8,10,11]].reset_index() #The iloc function isolates the data i want. 259:275 is saying, from the raw data, i want to use rows 259-275 only. The second part, [0,8,10,11] is saying these are the only columns i want to use
#UPDATE THE FIRST (ROW) NUMBERS. CURRENTLY, DATA IS SHOWING FROM Q1 2020 TO Q4 2023. ALTER THE FIRST NUMBER TO CHANGE WHERE TIME SERIES STARTS, SECOND NUMBER NEEDS TO BE +1 EVERY QUARTER TO INCLUDE LATEST DATA (if unsure, look at raw data and see what rows the data sits in)
nominal_real_income_processed = nominal_real_income_processed.rename(columns={
    "Dataset identifier": "date", "CSF2": "real income", "CSE9": "nominal income", "CSEZ": "implied deflator"}) #Here i have just renamed the indexes in the dataframe

nominal_real_income_processed["implied deflator"] = pd.to_numeric(nominal_real_income_processed["implied deflator"], errors="coerce")
nominal_real_income_processed["nominal income"] = pd.to_numeric(nominal_real_income_processed["nominal income"], errors="coerce")
nominal_real_income_processed["real income"] = pd.to_numeric(nominal_real_income_processed["real income"], errors="coerce") #Here, for some reason, the data wasn't being read in as numeric. Converted to numeric so it can be plotted.

fig, ax = plt.subplots()
plt.plot(nominal_real_income_processed["date"], nominal_real_income_processed["real income"], color="#206095", linewidth="2.0") #Creating the line plot for the real income
nominal_real_income_processed.set_index("date")[["implied deflator", "nominal income"]].plot(kind="bar", ax=ax, stacked=True, color=["#27a0cc","#003c57"]) #Creating the bar plots for nominal income and the implied deflator
customise_axes(ax) #Calling upon the custom axise function
plt.title("Real vs nominal household disposable income", fontweight="bold", fontname="Arial", fontsize="12")#Creating a title and changing the parameters
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)#Adding a y-label and changing the parameters
plt.legend(["Real income", "Implied deflator", "Nominal income"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False)#Adding a legend and changing the paramerters
plt.ylim(bottom=-4.1, top=8) #Altering the y-axis limit
desired_labels = ["2020 Q4", "2021 Q4", "2022 Q4", "2023 Q4"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([nominal_real_income_processed["date"].index[i] for i, label in enumerate(nominal_real_income_processed["date"]) if label in desired_labels])
ax.set_xticklabels([label.split(" ")[1] + " " + label.split(" ")[0] for label in desired_labels], rotation=0) #This allows me to add the desired labels on the x-axis
plt.show()


#Chart 2 - Real household disposable income - Quarterly change

real_income = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/nominal_real_income.csv") #Reading in the data, and saving it as a dataframe
#UPDATE WITH LINK TO OWN DATA FILE PATH
real_income_processed = real_income.iloc[259 : 275 ,[0,11]].reset_index() #The iloc function does the same as above. However, notice now we are only using columns 0 and 11.
#UPDATE THE FIRST SET OF NUMBERS (259 : 275) as wanted. 259 STARTS THE TIME SERIES AT Q1 2020, ADJUST AS NEEDED, AND 275 ENDS THE TIME SERIES WITH THE LATEST DATA. WILL NEED +1 FOR EACH NEW QUARTER FROM Q4 2023

real_income_processed = real_income_processed.rename(columns={"Dataset identifier" : "date", "CSF2" : "real income"}) #Renaming our variables within the data frame
real_income_processed["real income"] = pd.to_numeric(real_income_processed["real income"], errors="coerce") #As above, converting the data to numeric so python can read it

fig,ax = plt.subplots()
real_income_processed.set_index("date")[["real income"]].plot(kind="bar", ax=ax, stacked=True, color=["#27a0cc"]) #Creating the barplot
customise_axes(ax) #Calling upon the custom axise function
plt.title("Real household disposable income", fontweight="bold", fontname="Arial", fontsize="12")#Creating a title and changing the parameters
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)#Adding a y-label and changing the parameters
ax.legend().set_visible(False) #Turning off the legend
plt.ylim(bottom=-2.1, top=4.1) #Altering the y-axis limit
desired_labels = ["2020 Q4", "2021 Q4", "2022 Q4", "2023 Q4"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([real_income_processed["date"].index[i] for i, label in enumerate(real_income_processed["date"]) if label in desired_labels])
ax.set_xticklabels([label.split(" ")[1] + " " + label.split(" ")[0] for label in desired_labels], rotation=0) #This allows me to add the desired labels on the x-axis
plt.show()


#Chart 3 - Real household disposable income per capita - Quarterly change

real_income_per_capita_link = "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/uksectoraccounts/datasets/quarterlysectoraccounts/quarter4octtodec2023/quarterlysectoraccounts2023q4.xlsx" #The latest link for the data
#UPDATE WITH LATEST DIRECT LINK TO THE DATA
file_name = "real_income_per_capita" #How the data will be saved in the raw and processed file

ons_data_downloader(real_income_per_capita_link, file_name, "KEI", 430) #This code downloads the data from the ONS website, saves it under a specific name, with the last number being the number of rows skipped so only the necessary data is processed. 'KEI' is the name of the tab the data is downloaded from
real_income_per_capita =  pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/real_income_per_capita.csv") #Reading in the data, and saving it as a dataframe
#UPDATE WITH LINK TO OWN DATA FILE PATH
real_income_per_capita_processed = real_income_per_capita.iloc[259 : 275, [0,2]].reset_index() #Similar iloc function as before. As before
#UPDATE FIRST NUMBERS 259:285 AS NEEDED. FIRST NUMBER STARTS TIME SERIES AT Q1 2020, ADJUST AS WANTED. SECOND NUMBER WILL NEED TO BE PUSHED BACK ONE FOR EACH NEW QUARTER. 275 IS Q4 2023

real_income_per_capita_processed = real_income_per_capita_processed.rename(columns={"Dataset identifier" : "date", "CRXZ" : "real income PC"}) #Renaming our variables within the data frame
real_income_per_capita_processed["real income PC"] = pd.to_numeric(real_income_per_capita_processed["real income PC"], errors="coerce") #As above, converting the data to numeric so python can read it

fig,ax = plt.subplots()
real_income_per_capita_processed.set_index("date")[["real income PC"]].plot(kind="bar", ax=ax, stacked=True, color=["#27a0cc"]) #Creating the barplot
customise_axes(ax) #Calling upon the custom axise function
plt.title("Real household disposable income per capita", fontweight="bold", fontname="Arial", fontsize="12")#Creating a title and changing the parameters
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)#Adding a y-label and changing the parameters
ax.legend().set_visible(False) #Turning off the legend
plt.ylim(bottom=-4.1, top=4.1) #Altering the y-axis limit
desired_labels = ["2020 Q4", "2021 Q4", "2022 Q4", "2023 Q4"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([real_income_per_capita_processed["date"].index[i] for i, label in enumerate(real_income_per_capita_processed["date"]) if label in desired_labels])
ax.set_xticklabels([label.split(" ")[1] + " " + label.split(" ")[0] for label in desired_labels], rotation=0) #This allows me to add the desired labels on the x-axis
plt.show()


#Chart 4 - Household savings ratio

savings_ratio_link = "https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/uksectoraccounts/datasets/quarterlysectoraccounts/quarter4octtodec2023/quarterlysectoraccounts2023q4.xlsx" #The latest link for the data
file_name = "savings_ratio"

ons_data_downloader(savings_ratio_link, file_name, "HH_3", 89) #This code downloads the data from the ONS website, saves it under a specific name, with the last number being the number of rows skipped so only the necessary data is processed. 'HH_3' is the name of the tab the data is downloaded from
savings_ratio =  pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/savings_ratio.csv") #Reading in the data, and saving it as a dataframe
#UPDATE WITH LINK TO OWN DATA FILE PATH
savings_ratio_processed = savings_ratio.iloc[260 : 276, [0,7]].reset_index() #Similar iloc function as before. As before
#UPDATE FIRST NUMBERS 259:285 AS NEEDED. FIRST NUMBER STARTS TIME SERIES AT Q1 2020, ADJUST AS WANTED. SECOND NUMBER WILL NEED TO BE PUSHED BACK ONE FOR EACH NEW QUARTER. 275 IS Q4 2023


savings_ratio_processed = savings_ratio_processed.rename(columns={"Dataset identifier" : "date", "DGD8" : "Savings ratio"}) #Renaming our variables within the data frame

fig, ax = plt.subplots()
plt.plot(savings_ratio_processed["date"], savings_ratio_processed["Savings ratio"], color="#206095", linewidth="2.0") #Creating the line plot
customise_axes(ax) #Calling upon the custom axise function
plt.title("Households' savings ratio", fontweight="bold", fontname="Arial", fontsize="12")#Creating a title and changing the parameters
plt.ylabel("%", fontname="Arial", fontsize="12", rotation=0, loc="top", labelpad=-30)#Adding a y-label and changing the parameters
ax.legend().set_visible(False) #Turning off the legend
plt.ylim(bottom=-0.1, top=30) #Altering the y-axis limit
desired_labels = ["2020 Q4", "2021 Q4", "2022 Q4", "2023 Q4"]
#UPDATE TO SHOW FOR THE LATEST QUARTER AS WANTED
ax.set_xticks([savings_ratio_processed["date"].index[i] for i, label in enumerate(savings_ratio_processed["date"]) if label in desired_labels])
ax.set_xticklabels([label.split(" ")[1] + " " + label.split(" ")[0] for label in desired_labels], rotation=0) #This allows me to add the desired labels on the x-axis
plt.show()

