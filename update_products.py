import pandas as pd
import random

# List of ECE-related products
ece_products = [
    "Arduino Uno R3 Development Board",
    "Raspberry Pi 4 Model B",
    "ESP32 WiFi Development Board",
    "Digital Multimeter",
    "Logic Analyzer",
    "Function Generator",
    "Oscilloscope Probe Set",
    "Power Supply Unit",
    "PCB Etching Kit",
    "Soldering Station",
    "Component Starter Kit",
    "FPGA Development Board",
    "Signal Generator",
    "RF Spectrum Analyzer",
    "Network Analyzer",
    "Logic Gate Trainer Kit",
    "Microcontroller Starter Kit",
    "Digital Storage Oscilloscope",
    "Signal Conditioning Module",
    "RF Power Meter",
    "Breadboard Kit",
    "Resistor Assortment Kit",
    "Capacitor Kit",
    "Inductor Set",
    "Transistor Pack",
    "IC Chip Collection",
    "LED Assortment",
    "Sensor Kit",
    "Motor Driver Module",
    "Relay Module",
    "WiFi Module",
    "Bluetooth Module",
    "GPS Module",
    "RF Transceiver",
    "Antenna Kit",
    "PCB Prototype Board",
    "Wire Kit",
    "Connector Set",
    "Heat Sink Kit",
    "Test Lead Set"
]

# Read the original CSV file
df = pd.read_csv('online_retail_II.csv', low_memory=False)

# Create a mapping of unique product descriptions to ECE products
unique_products = df['Description'].unique()
num_unique = len(unique_products)

# If we have more unique products than ECE products, we'll reuse some ECE products
if num_unique > len(ece_products):
    # Calculate how many times we need to repeat the ECE products
    repeat_times = (num_unique + len(ece_products) - 1) // len(ece_products)
    # Create a list of repeated ECE products
    repeated_products = ece_products * repeat_times
    # Take only the number of products we need
    repeated_products = repeated_products[:num_unique]
    # Shuffle the products
    random.shuffle(repeated_products)
    # Create the mapping
    product_mapping = dict(zip(unique_products, repeated_products))
else:
    # If we have fewer unique products, just sample from ECE products
    product_mapping = dict(zip(unique_products, 
                              random.sample(ece_products, num_unique)))

# Replace the descriptions with ECE products
df['Description'] = df['Description'].map(product_mapping)

# Save the updated dataset
df.to_csv('online_retail_II_ece.csv', index=False)

print("Dataset has been updated with ECE-related product names.") 