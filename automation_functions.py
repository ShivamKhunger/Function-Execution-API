import os
import webbrowser
import psutil
import subprocess

class AutomationTools:
    
    def open_chrome(self):
        webbrowser.open("https://www.google.com")
        return "Brower openend"

    def open_calculator(self):
        if os.name == "nt": 
            os.system("calc")
        else:
            os.system("gnome-calculator")
        return "Calculator opened"

    def get_cpu_usage(self):
        usage = psutil.cpu_percent()
        return f"CPU is at {usage}%"

    def get_ram_usage(self):
        memory = psutil.virtual_memory()
        return f"RAM usage: {memory.percent}%"

    def run_shell_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    def open_notepad(self):
        os.system("notepad")
        return "Notepad opened"