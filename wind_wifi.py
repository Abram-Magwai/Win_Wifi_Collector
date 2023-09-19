import argparse
import subprocess
import os
import sys

def get_computer_wifis():        
    output = subprocess.run(args="netsh wlan show profile", shell=True, text=True, capture_output=True)
    wifis = output.stdout.split("All User Profile     :")[1:]
    computer_wifis = []
    for index in range(len(wifis)):
        wifi = wifis[index].replace("\n", "").strip()
        computer_wifis.append(wifi)
    return computer_wifis

def get_wifi_password(wifi):
    output = subprocess.run(args=f"netsh wlan show profile name=\"{wifi}\" key=clear", shell=True, text=True, capture_output=True)
    security_settings = output.stdout.split("Security setting")[1].split("Cost settings")[0].split("-----------------")[1].strip().replace(" ", "").split("\n")
    
    authentication = security_settings[0].split(":")[1]
    password = "N/A"
    if authentication == "Open":
        password = "Open"
    elif authentication == "WPA2-Enterprise":
        password = "WPA2-Enterprise - Couldn't find password"
    try:
        if password == "N/A":
            password = security_settings[5].split(":")[1]
    except IndexError:
        pass
    return password

def get_computer_name():
    try:
        host_name = os.environ["COMPUTERNAME"]
        return host_name
    except KeyError:
        try:
            host_name = os.environ["HOSTNAME"]
            return host_name
        except KeyError as e:
            return "comp"
def get_connected_wifi_details():
    sys.stdout.write("\rStarting script... |\n")
    wifis = get_computer_wifis()
    computer_name = get_computer_name()
    signs = ["/", "-", "\\"]
    sign_index = 0
    file_name = f"{computer_name}_wifis.txt"
    with open(file_name, "w") as file:
        for wifi in wifis:
            sys.stdout.write(f"\rExtracting details... {signs[sign_index]}")
            password = get_wifi_password(wifi)
            file.write(f"{wifi} >> {password}\n")
            sign_index += 1
            if sign_index == len(signs):
                sign_index = 0
    sys.stdout.write(f"\rDone!... {len(wifis)} wifi\"s extracted🎉. Look at {get_computer_name()}_wifis.txt\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windows Script to collect previous connected wifi📶 passwords")
    args = parser.parse_args()
    get_connected_wifi_details()