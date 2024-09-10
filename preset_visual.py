import tkinter as tk
from tkinter import filedialog
import os, sys

# Method to read a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the file line by line
            lines = file.readlines()
            decode_file(lines)
    except Exception as e:
        label.config(text=f"Error reading file: {e}")

# Method to decode a preset file and print to the screen the informations extracted
def decode_file(lines):
    # Initialize a flag to check if the string is found
    found = False
    
    # Iterate through each line
    for line in lines:
        # Skip lines that start with # (comments)
        if line.strip().startswith('#'):
            continue
        # Find the RF output frequency
        if 'output.rf.frequency' in line and not '.output.rf.frequency' in line and not 'output.rf.frequency.' in line:
            freq = line.strip().split('=')[1].strip()
        # Find the IP Address
        if 'system.comm.ip.flan.addr' in line:
            IP = line.strip().split('=')[1].strip()
        # Find the modulation standard
        if 'system.modulation.standard' in line:
            modul_std = line.strip().split('=')[1].strip()
            found = True
    
    # Iterate through each line again to get more parameters based on modulation standard
    for line in lines:
        # Skip lines that start with #
        if line.strip().startswith('#'):
            continue
        # If the modulation standard is DVB-T
        if modul_std == "DVBT":
            # Get the local SFN delay 
            if 'mode.local.delay.offset' in line:
                sfn_delay = line.strip().split('=')[1].strip()
            # Get the cell ID 
            if 'mode.cellid.value' in line:
                cell_id = line.strip().split('=')[1].strip()
        # If the modulation standard is DVB-T2
        if modul_std == "DVBT2":
            # Get the local SFN delay 
            if 't2.mi.local.sfn_delay' in line:
                sfn_delay = line.strip().split('=')[1].strip()
            # Get the cell ID 
            if 't2.mi.local.cell_id' in line:
                cell_id = line.strip().split('=')[1].strip()

    # If we can't determine the modulation standard, show an error
    if not found:
        label.config(text=f"Error decoding: Not valid file")
    
    else:
        # Calculate the channel and band from frequency
        frequency = int(freq) / 1000000
        if frequency >= 474:
            band = "UHF"
            channel = ((frequency - 474) / 8) + 21
        else:
            band = "VHF"
            channel = ((frequency - 177.5) / 7) + 5

        # Print the values to output
        content = "Transm. Standard:\t{}\n".format(modul_std)
        content += "Frequency:\t{}MHz\n".format(frequency)
        content += "Channel:\t\t{:.0f} ({})\n".format(channel, band)
        content += "SFN Delay:\t{}ms\n".format(int(sfn_delay)/10) 
        content += "Cell ID:\t\t{}\n".format(cell_id)
        content += "IP Address:\t{}".format(IP)
        label.config(text=content)

# Method to open file with the file dialog
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        read_file(file_path)

# Main loop
root = tk.Tk()
root.title("Itelco Preset Reader - v1.0.0 - Marco Fantauzzo")
if getattr(sys, 'frozen', False):
    root.iconbitmap(os.path.join(sys._MEIPASS, "icon.ico"))
else:
    root.iconbitmap("icon.ico")

root.geometry("450x200")

label = tk.Label(root, text="Click on the button below to open a preset file", padx=10, pady=10, wraplength=380, justify="left")
label.pack(expand=True, fill=tk.BOTH)

button = tk.Button(root, text="Open file", command=open_file)
button.pack(pady=20)

root.mainloop()
