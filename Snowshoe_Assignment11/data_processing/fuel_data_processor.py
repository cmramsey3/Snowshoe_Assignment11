# fuel_data_processor.py

import csv
import os
import requests

class fuel_data_processor:
    def __init__(self, file_path, api_key=None):
        self.file_path = file_path
        self.data = []
        self.headers = []

    def read_csv(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.headers = reader.fieldnames
            self.data = [row for row in reader]

    def format_gross_price(self):
        for row in self.data:
            try:
                price = float(row["Gross Price"])
                row["Gross Price"] = f"{price:.2f}"
            except (ValueError, KeyError):
                row["Gross Price"] = ""

    def remove_duplicates(self):
        unique_rows = []
        seen = set()
        for row in self.data:
            # Convert row to a tuple of items so it can be added to a set
            row_tuple = tuple(row.items())
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_rows.append(row)
        self.data = unique_rows

    def remove_non_fuel_purchases(self):
        fuel_rows = []
        anomaly_rows = []
        for row in self.data:
            fuel_type = row.get("Fuel Type", "").lower()
            if "pepsi" in fuel_type:
                anomaly_rows.append(row)
            else:
                fuel_rows.append(row)
        self.data = fuel_rows

        # Save anomalies to a separate CSV
        output_folder = "Data"
        os.makedirs(output_folder, exist_ok=True)
        anomaly_path = os.path.join(output_folder, "dataAnomalies.csv")

        with open(anomaly_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(anomaly_rows)


    def save_to_csv(self):
        output_folder = "data"
        output_path = os.path.join(output_folder, "cleanedData.csv")
        # Create the folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.data)
