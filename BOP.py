import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import textwrap #Importing packages used throughout

def customise_axes(ax):
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False) 
    ax.grid(b=True, which = "major", axis = "x", color = "white")
    ax.grid(b=True, which = "major", axis = "y", color = "lightblue")
    plt.axhline(0, color="black", linewidth=0.5)
    ax.set_axisbelow(True)
    plt.xlabel("")#Defining a function allowing me to call upon it for each chart to set the common parameters each chart uses

requests.packages.urllib3.disable_warnings()
def ons_data_downloader(link, output_file_name, tab_name, skip_rows):
    response = requests.get(link, verify=False)
    with open('data/raw/' + output_file_name + '.xlsx', 'wb') as file:
        file.write(response.content) #
    data_tab = pd.read_excel('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/raw/' + output_file_name + '.xlsx', sheet_name=tab_name, skiprows=skip_rows)
    #UPDATE: change file path to own computer. Create folders as such for ease
    data_tab.to_csv('//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/'  +  output_file_name + '.csv', index=False)
    return
    #UPDATE: change file path to own computer. Create folders as such for ease
    #This function allows us to download the data directly from the ONS website. It stores the original in the 'raw' and the data we will then use in 'processed'.
    
#BOP SECTION

#Chart 1 - Current account balances

CA_link = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/balanceofpayments/bulletins/balanceofpayments/octobertodecember2023/c7ed4d23&format=xls"
#UPDATE with latest link from the BOP bulletin, copy link from chart link
file_name = "current_account_balances" #This is what we are saving the data as in our files
ons_data_downloader(CA_link, file_name, "data", 6) #CA link is the name of the link created when downnloading the data, file name is the name we give the file, 'data' is the name of the tab the data is being downloaded from, 6 is the number of rows skipped to acquire the necessary info

current_account = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/current_account_balances.csv")
#UPDATE with link to own folders and directory
current_account = current_account[["Unnamed: 0","Total secondary income ", "Total primary income", "Trade in services", "Trade in goods", "Current account","Current Account balance including precious metals"]]#List of the variable names, be careful of capital letters and spaces as easy to miss

fig, ax= plt.subplots()
plt.plot(current_account["Unnamed: 0"], current_account["Current account"], label="Current account", color=(32/255, 96/255, 149/255), linewidth=2.0)
plt.plot(current_account["Unnamed: 0"], current_account["Current Account balance including precious metals"], label="Current account balance including precious metals", color=(39/255, 160/255, 204/255), linewidth=2.0) #These two are producing the lines on the charts, the colours are in RGBA format matching ONS house style
ax.set_axisbelow(True) #Setting the chart axis below the data

current_account[["Unnamed: 0", "Total secondary income ", "Total primary income", "Trade in services", "Trade in goods"]].plot("Unnamed: 0", kind="bar", stacked=True, ax=ax, color = [(0/255, 60/255, 87/255), (17/255, 140/255, 123/255), (168/255, 189/255, 58/255), (135/255, 26/255, 91/255)]) #Creating a stacked barplot for the rest of the data, colours matching ONS house style
plt.legend(loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False) #Setting the legend and its parameters (bbox moves the position, ncol is number of columns and the frame is removed)
plt.ylabel("% of GDP", rotation=0, loc="top", labelpad=-70) #y-axis label - rotation ensures it is read horizontal, location places it at the top of the axis and label pad positions it to the right
plt.title("Current account balances", fontweight="bold", fontname="Arial", fontsize="12") #Title
customise_axes(ax) #Calling upon the function used to set chart parameters
ax.set_ylim(bottom=-16, top=10) #y-axis scale
desired_labels = ["Q1 2021", "Q1 2022", "Q1 2023","Q4 2023"]
#UPDATE the desired labels to what is wanted
ax.set_xticks([current_account["Unnamed: 0"].index[i] for i, label in enumerate(current_account["Unnamed: 0"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #These 3 lines of code are allowing us the ability to decide what x labels we want on show
plt.show()

#Chart 2 - Trade balance

TB_link = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/balanceofpayments/bulletins/balanceofpayments/octobertodecember2023/8156470c&format=xls"
file_name = "trade_balance"
ons_data_downloader(TB_link, file_name, "data", 6)#TB link is the name of the link created when downnloading the data, file name is the name we give the file, 'data' is the name of the tab the data is being downloaded from, 6 is the number of rows skipped to acquire the necessary info

trade_balance = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/trade_balance.csv")
#UPDATE with link to own file path
trade_balance = trade_balance[["Unnamed: 0", "Trade in goods", "Trade in services", "Total Trade in goods and services ", "Total trade in goods and services including precious metals"]] #Ensure names match those in the excel file, being careful of spaces and capital letters

fig, ax =plt.subplots()
plt.plot(trade_balance["Unnamed: 0"], trade_balance["Total Trade in goods and services "], color=(32/255, 96/255, 149/255), linewidth=2.0)
plt.plot(trade_balance["Total trade in goods and services including precious metals"], color=(39/255, 160/255, 204/255), linewidth=2.0) #First plotting the total trades as lines

trade_balance[["Unnamed: 0", "Trade in goods", "Trade in services"]].plot("Unnamed: 0", kind="bar", stacked=True, ax=ax, color=[(0/255, 60/255, 87/255), (17/255, 140/255, 123/255)]) #Then plotting the rest of the data as a bars, ensuring they're stacked
plt.legend(["Total trade in goods and services", "Total trade in goods and services including precious metals", "Trade in goods", "Trade in services"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False) #Setting the legend and its parameters (bbox moves the position, ncol is number of columns and the frame is removed)
plt.ylabel(" £ billion", rotation=0, loc="top", labelpad=-70) #y-axis label - rotation ensures it is read horizontal, location places it at the top of the axis and label pad positions it to the right
plt.title("Trade balance", fontweight="bold", fontname="Arial", fontsize="12") #Title
customise_axes(ax) #Adding the common set of parameters defined at the beginning
ax.set_ylim(bottom=-81, top=60) #y-axis paramaters
desired_labels = ["Q1 2021", "Q1 2022", "Q1 2023","Q4 2023"]
#UPDATE the desired labels to what is wanted
ax.set_xticks([trade_balance["Unnamed: 0"].index[i] for i, label in enumerate(trade_balance["Unnamed: 0"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #These 3 lines of code are allowing us the ability to decide what x labels we want on show
plt.show()

#Chart 3 - Primary income account

PI_link = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/balanceofpayments/bulletins/balanceofpayments/octobertodecember2023/deba072c&format=xls"
file_name = "primary_income_account"
ons_data_downloader(PI_link, file_name, "data", 6)#PI link is the name of the link created when downnloading the data, file name is the name we give the file, 'data' is the name of the tab the data is being downloaded from, 6 is the number of rows skipped to acquire the necessary info

primary_income = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/primary_income_account.csv")
#UPDATE with link to own file path
primary_income = primary_income[["Unnamed: 0", "Direct investment", "Portfolio investment", "Other investment", "Total"]] #Ensure they match those in the excel file, careful of spaces and capital letters

fig, ax= plt.subplots()
plt.plot(primary_income["Unnamed: 0"], primary_income["Total"], color=[32/255,96/255,149/255], linewidth=2.0) #First plotting the total as a line

primary_income[["Unnamed: 0", "Direct investment", "Portfolio investment", "Other investment"]].plot("Unnamed: 0", kind="bar", stacked=True, ax=ax, color=[(39/255, 160/255, 204/255),(0/255, 60/255, 87/255), (17/255, 140/255, 123/255)]) #Then plotting the rest as bars, ensuring they're stacked
plt.legend(["Total", "Direct investment", "Portfolio investment", "Other investment"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False) #Setting the legend and its parameters (bbox moves the position, ncol is number of columns and the frame is removed)
plt.ylabel("£ billion", rotation=0, loc="top", labelpad=-70) #y-axis label - rotation ensures it is read horizontal, location places it at the top of the axis and label pad positions it to the right
plt.title("Primary income account", fontweight="bold", fontname="Arial", fontsize="12") #Title
customise_axes(ax) #calling upon the function with the various input parameters for charts
ax.set_ylim(bottom=-40, top=40) #Setting the y-axis parameters
desired_labels = ["Q1 2021", "Q1 2022", "Q1 2023","Q4 2023"]
#UPDATE the desired labels to what is wanted
ax.set_xticks([primary_income["Unnamed: 0"].index[i] for i, label in enumerate(primary_income["Unnamed: 0"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #These 3 lines of code are allowing us the ability to decide what x labels we want on show
plt.show()

# Chart 4 - Financial account

FA_link = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/balanceofpayments/bulletins/balanceofpayments/octobertodecember2023/aa911697&format=xls"
file_name = "financial_account"
ons_data_downloader(FA_link, file_name, "data", 6)#FA link is the name of the link created when downnloading the data, file name is the name we give the file, 'data' is the name of the tab the data is being downloaded from, 6 is the number of rows skipped to acquire the necessary info

financial_account = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/financial_account.csv")
#UPDATE with link to own file path
financial_account = financial_account[["Unnamed: 0", "Direct investment", "Portfolio investment", "Other investment", "Financial derivatives & employee stock options", "Total"]] #Ensure they match those in the excel file, being careful of capital letters and spaces

fig,ax= plt.subplots()
plt.plot(financial_account["Unnamed: 0"], financial_account["Total"], color=[32/255,96/255,149/255], linewidth=2.0) #First plotting the total as a line

financial_account[["Unnamed: 0", "Direct investment", "Portfolio investment", "Other investment", "Financial derivatives & employee stock options"]]. plot("Unnamed: 0", kind="bar", stacked=True, ax=ax, color=[(39/255, 160/255, 204/255),(0/255, 60/255, 87/255), (17/255, 140/255, 123/255),(168/255, 189/255, 58/255)]) #Then plotting the rest as a stacked bar plot
plt.legend(["Total", "Direct investment", "Portfolio investment", "Other investment", "Financial derivatives & employee stock options"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False) #Setting the legend and its parameters (bbox moves the position, ncol is number of columns and the frame is removed)
plt.ylabel("£ billion", rotation=0, loc="top", labelpad=-70) #y-axis label - rotation ensures it is read horizontal, location places it at the top of the axis and label pad positions it to the right
plt.title("Financial account", fontweight="bold", fontname="Arial", fontsize="12") #Title
desired_labels = ["Q1 2021", "Q1 2022", "Q1 2023","Q4 2023"]
#UPDATE the desired labels to what is wanted
ax.set_xticks([financial_account["Unnamed: 0"].index[i] for i, label in enumerate(financial_account["Unnamed: 0"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #These 3 lines of code are allowing us the ability to decide what x labels we want on show
customise_axes(ax) #Calling upon the input parameter function again
plt.show()

#Chart 5 - International investment position

IIP_link = "https://www.ons.gov.uk/generator?uri=/economy/nationalaccounts/balanceofpayments/bulletins/balanceofpayments/octobertodecember2023/d33dda77&format=xls"
file_name = "international_IP"
ons_data_downloader(IIP_link, file_name, "data", 6)#IIP link is the name of the link created when downnloading the data, file name is the name we give the file, 'data' is the name of the tab the data is being downloaded from, 6 is the number of rows skipped to acquire the necessary info

international_ip = pd.read_csv("//NDATA9/anderj3$/My Documents/Data Science Project/Code/data/processed/international_IP.csv")
#UPDATE with link to own file path
international_ip = international_ip[["Unnamed: 0", "Direct investment", "Portfolio investment", "Other investment", "Financial derivatives & employee stock options", "Reserve assets", "Total"]] #Ensure the names match to those in excel file, being careful of spaces ans capital letters

fig, ax= plt.subplots()
plt.plot(international_ip["Unnamed: 0"], international_ip["Total"], color=[32/255,96/255,149/255], linewidth=2.0) #First plotting the total as a line

international_ip[["Unnamed: 0", "Direct investment", "Portfolio investment", "Other investment", "Financial derivatives & employee stock options", "Reserve assets"]].plot("Unnamed: 0", kind="bar", stacked=True, ax=ax, color= [(39/255, 160/255, 204/255),(0/255, 60/255, 87/255), (17/255, 140/255, 123/255),(168/255, 189/255, 58/255), (135/255, 26/255, 91/255)]) #Then the rest as a stacked bar plot
plt.legend(["Total", "Direct investment", "Portfolio investment", "Other investment", "Financial derivatives & employee stock options", "Reserve assets"], loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=2, frameon=False) #Setting the legend and its parameters (bbox moves the position, ncol is number of columns and the frame is removed)
plt.ylabel("£ billion", rotation=0, loc="top", labelpad=-77) #y-axis label - rotation ensures it is read horizontal, location places it at the top of the axis and label pad positions it to the right
plt.title("International investment position", fontweight="bold", fontname="Arial", fontsize="12") #Title
customise_axes(ax) #Calling upon this function again
ax.set_ylim(bottom=-1500, top=1000) #Setting y-axis paramaters
desired_labels = ["Q1 2021", "Q1 2022", "Q1 2023","Q4 2023"]
#UPDATE the desired labels to what is wanted
ax.set_xticks([international_ip["Unnamed: 0"].index[i] for i, label in enumerate(international_ip["Unnamed: 0"]) if label in desired_labels])
ax.set_xticklabels(desired_labels, rotation=0) #These 3 lines of code are allowing us the ability to decide what x labels we want on show
plt.show()