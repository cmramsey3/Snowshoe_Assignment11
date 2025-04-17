# File Name: fuel_data_processor.py
# Student Name: Lucas Iceman, Colten Ramsey 
# email:  icemanlc@mail.uc.edu, ramseyc6@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   4/16/2025
# Course #/Section:   IS4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment:This assignment requires us to clean data and to save that cleaned data as a CSV
# Brief Description of what this module does:This module defines a class that performs all data cleaning tasks for the fuel purchase dataset,including formatting prices, removing duplicates, filtering non-fuel items, filling in ZIP codes
# Citations: Chat GPT
# Anything else that's relevant:N/A

import csv
import os
import requests

class fuel_data_processor:
    """
    Cleans and processes fuel purchase data from a CSV file, including formatting, filtering, and ZIP code lookup.
    """
    def __init__(self, file_path, api_key=None):
        """
        Initializes the processor with the CSV file path and optional ZIP code API key.
        @param:File Path API Key
        @Return None
        """
        self.file_path = file_path
        self.data = []
        self.api_key = "6addd430-1b37-11f0-ba94-cdadd7f9298f"
        self.headers = []

    def read_csv(self):
        """
        Reads the CSV file and loads data into memory
        @param:None
        @Return:None
        """
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.headers = reader.fieldnames
            self.data = [row for row in reader]

    def format_gross_price(self):
        """
        Formats the 'Gross Price' column to two decimal places.
        @param:None
        @Return:None
        """
        for row in self.data:
            try:
                price = float(row["Gross Price"])
                row["Gross Price"] = f"{price:.2f}"
            except (ValueError, KeyError):
                row["Gross Price"] = ""

    def remove_duplicates(self):
        """
        Removes duplicate rows from the dataset.
        @param:None
        @Return:None
        """
        unique_rows = []
        seen = set()
        for row in self.data:
            row_tuple = tuple(row.items())
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_rows.append(row)
        self.data = unique_rows

    def remove_non_fuel_purchases(self):
        """
        Removes non-fuel purchases and logs them to a separate anomalies file.
        @param:None
        @Return:None
        """
        fuel_rows = []
        anomaly_rows = []
        for row in self.data:
            fuel_type = row.get("Fuel Type", "").lower()
            if "pepsi" in fuel_type:
                anomaly_rows.append(row)
            else:
                fuel_rows.append(row)
        self.data = fuel_rows
        output_folder = "Data"
        os.makedirs(output_folder, exist_ok=True)
        anomaly_path = os.path.join(output_folder, "dataAnomalies.csv")

        with open(anomaly_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(anomaly_rows)
    def fill_missing_zipcodes(self):
        """
        Fills missing ZIP codes in addresses using the Zipcodebase API (up to 5 rows).
        @param:None
        @Return:None
        """
        if not self.api_key:
            print("No API key provided for zipcode lookup.")
            return
 
        updated_count = 0
        for row in self.data:
            if updated_count >= 5:
                break
 
            address = row.get("Full Address", "")
            parts = address.strip().split()
            if not parts or not parts[-1].isdigit() or len(parts[-1]) != 5:
                if len(parts) < 2:
                    continue
                city = parts[-2].strip(",")
                state = parts[-3].strip(",") if len(parts) >= 3 else ""
                response = requests.get(
                    f"https://app.zipcodebase.com/api/v1/search",
                    params={"apikey": self.api_key, "city": city, "state": state, "country": "US"}
                )
                if response.status_code == 200:
                    data = response.json()
                    zipcodes = data.get("results", {}).get(city, [])
                    if zipcodes:
                        zip_code = zipcodes[0].get("postal_code")
                        if zip_code:
                            row["Full Address"] += f" {zip_code}"
                            updated_count += 1
    def save_to_csv(self):
        """
        Saves the cleaned data to 'cleanedData.csv' in the Data folder.
        @param:None
        @Return:None
        """
        output_folder = "data"
        output_path = os.path.join(output_folder, "cleanedData.csv")
        os.makedirs(output_folder, exist_ok=True)
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.data)

