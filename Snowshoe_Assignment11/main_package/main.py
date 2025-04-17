# main.py

from data_processing.fuel_data_processor import *

processor = fuel_data_processor("Data/fuelPurchaseData.csv")
processor.read_csv()
processor.format_gross_price()
processor.remove_duplicates()
processor.remove_non_fuel_purchases()
processor.save_to_csv()