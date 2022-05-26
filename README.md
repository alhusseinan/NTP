Clone this repo in your local machine typing on your terminal:
git clone https://github.com/agmanuelian/config_manager.git

Install the required dependencies specified on the requirements.txt file:
pip install requirements.txt

Edit the devices.csv file with the parameters (IP address and RESTCONF port) of the list of devices that you want to configure.
Modify on the main_file.py script the directory from where the devices.csv file is read, with your local directory.
Replace the confgen_response JSON object with your infrastructure parameters (NTP server, SNMP and Logging parameters).
Run the main_file.py script.
python main_file.py

You will be prompted to enter your TACACS credentials (demo credentials specified on previous section) to access the list of devices.
You will be prompted to enter the desired option (whether to configure NTP, Logging or SNMP)
Based on your selection, the script will configure it on the list of devices.
