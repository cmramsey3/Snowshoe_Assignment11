# File Name : Main.py
# Student Name: Lucas Iceman, Colten Ramsey 
# email:  icemanlc@mail.uc.edu, ramseyc6@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   4/16/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment:This assignment requires us to clean data and to save that cleaned data as a CSV
# Brief Description of what this module does: runs each step of the data cleaning process, and saves the final cleaned data to a CSV file.
# Citations: Chat GPT
# Anything else that's relevant:N/A

from data_processing.fuel_data_processor import *

processor = fuel_data_processor("Data/fuelPurchaseData.csv")
processor.read_csv()
processor.format_gross_price()
processor.remove_duplicates()
processor.remove_non_fuel_purchases()
#processor.fill_missing_zipcodes()
processor.save_to_csv()