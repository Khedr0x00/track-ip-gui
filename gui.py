import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class IPTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Tracker by khedr0x00") # Updated title
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#282c34")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#282c34')
        self.style.configure('TLabel', background='#282c34', foreground='#61dafb', font=('Inter', 12))
        self.style.configure('TButton', background='#61dafb', foreground='#282c34', font=('Inter', 12, 'bold'), borderwidth=0, focusthickness=3, focuscolor='none')
        self.style.map('TButton', background=[('active', '#98c379')])
        self.style.configure('TEntry', fieldbackground='#3e4451', foreground='#abb2bf', font=('Inter', 12), borderwidth=0)
        self.style.configure('TText', fieldbackground='#3e4451', foreground='#abb2bf', font=('Inter', 12), borderwidth=0)

        self.create_widgets()
        self.show_main_menu()

    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(expand=True, fill='both')

        # Banner
        self.banner_label = ttk.Label(self.main_frame, text=self.get_banner_text(), font=('Inter', 10, 'bold'), foreground='#e6c07b')
        self.banner_label.pack(pady=10)

        # Content frame for dynamic content
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(expand=True, fill='both', pady=20)

    def get_banner_text(self):
        # Replicate the ASCII art banner
        banner_text = """
   _______             _       _____       
  |__   __|           | |     |_   _|      
     | |_ __ __ _  ___| | __    | |  _ __  
     | |  __/ _  |/ __| |/ /    | | |  _ \\ 
     | | | | (_| | (__|   <    _| |_| |_) |
     |_|_|  \\__,_|\\___|_|\\_\\  |_____| .__/ 
                                    | |    
                                    |_|    

    Created By khedr0x00 
        """
        return banner_text

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_content_frame()

        ttk.Button(self.content_frame, text="My IP", command=self.my_ip_address).pack(pady=10, ipadx=20, ipady=10)
        ttk.Button(self.content_frame, text="Track IP", command=self.track_ip_input).pack(pady=10, ipadx=20, ipady=10)
        ttk.Button(self.content_frame, text="Exit", command=self.root.quit).pack(pady=10, ipadx=20, ipady=10)

    def fetch_ip_info(self, ip_address=None):
        try:
            if ip_address:
                ipapi_co_url = f"https://ipapi.co/{ip_address}/json"
                ip_api_com_url = f"http://ip-api.com/json/{ip_address}"
            else:
                ipapi_co_url = "https://ipapi.co/json"
                ip_api_com_url = "http://ip-api.com/json/"

            response_ipapi_co = requests.get(ipapi_co_url)
            response_ipapi_co.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data_ipapi_co = response_ipapi_co.json()

            response_ip_api_com = requests.get(ip_api_com_url)
            response_ip_api_com.raise_for_status()
            data_ip_api_com = response_ip_api_com.json()

            return data_ipapi_co, data_ip_api_com
        except requests.exceptions.RequestException as e:
            # Do not show error message here, handle it in display_ip_info
            return None, None
        except json.JSONDecodeError:
            # Do not show error message here, handle it in display_ip_info
            return None, None

    def display_ip_info(self, data_ipapi_co, data_ip_api_com, info_text_widget):
        if not data_ipapi_co or not data_ip_api_com:
            info_text_widget.insert(tk.END, "Error: Could not retrieve IP information for this address.\n\n")
            return

        # Extract data from ipapi.co
        ip = data_ipapi_co.get('ip', 'N/A')
        city = data_ipapi_co.get('city', 'N/A')
        region = data_ipapi_co.get('region', 'N/A')
        country = data_ipapi_co.get('country_name', 'N/A')
        isp = data_ipapi_co.get('org', 'N/A')
        asn = data_ipapi_co.get('asn', 'N/A')
        country_code = data_ipapi_co.get('country_code', 'N/A')
        currency = data_ipapi_co.get('currency', 'N/A')
        languages = data_ipapi_co.get('languages', 'N/A')
        calling_code = data_ipapi_co.get('country_calling_code', 'N/A')

        # Extract data from ip-api.com
        lat = data_ip_api_com.get('lat', 'N/A')
        lon = data_ip_api_com.get('lon', 'N/A')
        timezone = data_ip_api_com.get('timezone', 'N/A')
        postal = data_ip_api_com.get('zip', 'N/A')

        google_maps_link = f"https://maps.google.com/?q={lat},{lon}" if lat != 'N/A' and lon != 'N/A' else 'N/A'

        output_lines = [
            f"--- IP Address: {ip} ---",
            f"  City          :   {city}",
            f"  Region        :   {region}",
            f"  Country       :   {country}",
            "",
            f"  Latitude      :    {lat}",
            f"  Longitude     :    {lon}",
            f"  Time Zone     :    {timezone}",
            f"  Postal Code   :    {postal}",
            "",
            f"  ISP           :   {isp}",
            f"  ASN           :   {asn}",
            "",
            f"  Country Code  :   {country_code}",
            f"  Currency      :   {currency}",
            f"  Languages     :   {languages}",
            f"  Calling Code  :   {calling_code}",
            "",
            f"  GOOGLE Maps   :  {google_maps_link}",
            "\n" + "="*70 + "\n\n" # Separator for multiple IPs
        ]

        for line in output_lines:
            info_text_widget.insert(tk.END, line + "\n")

    def my_ip_address(self):
        self.clear_content_frame()
        
        # Frame to hold Text widget and Scrollbar
        text_frame = ttk.Frame(self.content_frame)
        text_frame.pack(pady=10, padx=10, fill='both', expand=True)

        info_text = tk.Text(text_frame, wrap='word', height=20, width=70)
        info_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        info_text.config(yscrollcommand=scrollbar.set)

        info_text.config(state='normal') # Enable editing to insert text
        data_ipapi_co, data_ip_api_com = self.fetch_ip_info()
        self.display_ip_info(data_ipapi_co, data_ip_api_com, info_text)
        info_text.config(state='disabled') # Disable editing after inserting text

        ttk.Button(self.content_frame, text="Return To Main Menu", command=self.show_main_menu).pack(pady=10, ipadx=20, ipady=10)
        ttk.Button(self.content_frame, text="Exit", command=self.root.quit).pack(pady=10, ipadx=20, ipady=10)

    def track_ip_input(self):
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="Input IP Address(es) (one per line):").pack(pady=10)
        
        # Frame to hold Text widget and Scrollbar for input
        input_text_frame = ttk.Frame(self.content_frame)
        input_text_frame.pack(pady=5, fill='x', padx=10)

        self.ip_input_text = tk.Text(input_text_frame, wrap='word', height=5, width=40)
        self.ip_input_text.pack(side=tk.LEFT, fill='x', expand=True)
        
        input_scrollbar = ttk.Scrollbar(input_text_frame, command=self.ip_input_text.yview)
        input_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.ip_input_text.config(yscrollcommand=input_scrollbar.set)
        
        self.ip_input_text.focus_set()

        ttk.Button(self.content_frame, text="Track", command=self.track_user_ip).pack(pady=10, ipadx=20, ipady=10)
        ttk.Button(self.content_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10, ipadx=20, ipady=10)

    def track_user_ip(self):
        ip_addresses_raw = self.ip_input_text.get("1.0", tk.END).strip()
        ip_addresses = [ip.strip() for ip in ip_addresses_raw.split('\n') if ip.strip()]

        if not ip_addresses:
            messagebox.showwarning("Input Error", "Please enter at least one IP address.")
            return

        self.clear_content_frame()

        # Frame to hold Text widget and Scrollbar for output
        text_frame = ttk.Frame(self.content_frame)
        text_frame.pack(pady=10, padx=10, fill='both', expand=True)

        info_text = tk.Text(text_frame, wrap='word', height=20, width=70)
        info_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        info_text.config(yscrollcommand=scrollbar.set)

        info_text.config(state='normal') # Enable editing to insert text
        
        for ip_address in ip_addresses:
            data_ipapi_co, data_ip_api_com = self.fetch_ip_info(ip_address)
            self.display_ip_info(data_ipapi_co, data_ip_api_com, info_text)
        
        info_text.config(state='disabled') # Disable editing after inserting text

        ttk.Button(self.content_frame, text="Return To Main Menu", command=self.show_main_menu).pack(pady=10, ipadx=20, ipady=10)
        ttk.Button(self.content_frame, text="Exit", command=self.root.quit).pack(pady=10, ipadx=20, ipady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPTrackerGUI(root)
    root.mainloop()
