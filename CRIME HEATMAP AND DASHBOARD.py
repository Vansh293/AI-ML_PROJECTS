import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageTk
import webbrowser
import os
import random  


num_sf = 20
num_la = 15
num_ny = 10
num_dates_1 = 10
num_dates_2 = 10
num_dates_3 = 10
num_dates_4 = 10
num_dates_5 = 5
num_theft = 10
num_assault = 10
num_vandalism = 10
num_burglary = 5

total_crimes = num_sf + num_la + num_ny
total_dates = num_dates_1 + num_dates_2 + num_dates_3 + num_dates_4 + num_dates_5
total_categories = num_theft + num_assault + num_vandalism + num_burglary

sample_data = {
    'Latitude': [37.7749 + random.uniform(-0.05, 0.05) for _ in range(num_sf)] +  
                [34.0522 + random.uniform(-0.05, 0.05) for _ in range(num_la)] +  
                [40.7128 + random.uniform(-0.05, 0.05) for _ in range(num_ny)],  
    'Longitude': [-122.4194 + random.uniform(-0.05, 0.05) for _ in range(num_sf)] +
                 [-118.2437 + random.uniform(-0.05, 0.05) for _ in range(num_la)] +
                 [-74.0060 + random.uniform(-0.05, 0.05) for _ in range(num_ny)],
    'Date': ['2025-01-01' for _ in range(num_dates_1)] + ['2025-01-02' for _ in range(num_dates_2)] +
            ['2025-01-03' for _ in range(num_dates_3)] + ['2025-01-04' for _ in range(num_dates_4)] +
            ['2025-01-05' for _ in range(num_dates_5)],
    'Category': ['Theft' for _ in range(num_theft)] + ['Assault' for _ in range(num_assault)] +
                ['Vandalism' for _ in range(num_vandalism)] + ['Burglary' for _ in range(num_burglary)]
}


lengths = [len(sample_data[key]) for key in sample_data]
if len(set(lengths)) != 1:
    print("Error: Lists in sample_data have different lengths!")
    min_length = min(lengths)
    for key in sample_data:
        sample_data[key] = sample_data[key][:min_length]

df = pd.DataFrame(sample_data)


def generate_heatmap():
    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)  

    heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)
    map_file = "crime_heatmap.html"
    m.save(map_file)
    return map_file

def plot_crime_trends():
    plt.figure(figsize=(8, 4))
    df['Date'] = pd.to_datetime(df['Date'])
    trend = df.groupby('Date').size()
    trend.plot(kind='line', color='#FF6F61', marker='o')
    plt.title("Crime Trends Over Time", fontsize=12, color='#3A86FF')
    plt.xlabel("Date")
    plt.ylabel("Number of Crimes")
    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.savefig("trend_plot.png")
    plt.close()

def plot_crime_categories():
    plt.figure(figsize=(6, 6))
    sns.countplot(data=df, x='Category', palette='pastel')
    plt.title("Crime Categories", fontsize=12, color='#3A86FF')
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.tight_layout() 
    plt.savefig("category_plot.png")
    plt.close()

class CrimeDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Heatmap & Analytics Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F4F6FF")

        
        self.main_frame = tk.Frame(root, bg="#EDEFFA", bd=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1100, height=750)
        
        
        self.title_label = tk.Label(self.main_frame, text="Crime Analytics Dashboard", font=("Poppins", 28, "bold"), fg="#3A86FF", bg="#EDEFFA")
        self.title_label.pack(pady=(20, 100))  
        self.animate_title()

       
        self.stats_label = tk.Label(self.main_frame, text="", font=("Poppins", 14), fg="#2D4059", bg="#EDEFFA")
        self.stats_label.pack(pady=(10, 100))  
        self.update_stats()

       
        self.analytics_frame = tk.Frame(self.main_frame, bg="#EDEFFA")
        self.analytics_frame.pack(pady=20, fill="both", expand=True)

        
        self.trend_category_frame = tk.Frame(self.analytics_frame, bg="#EDEFFA")
        self.trend_category_frame.pack(pady=10)

    
        self.trend_button = tk.Button(self.trend_category_frame, text="Show Trends", font=("Poppins", 12), bg="#00C897", fg="white",
                                      bd=0, command=self.show_trends)
        self.trend_button.pack(side="left", padx=20, pady=100)  
        self.animate_button(self.trend_button)

         
        self.map_button = tk.Button(self.trend_category_frame, text="Show Crime Heatmap", font=("Poppins", 14, "bold"), bg="#FF6F61", fg="white",
                                    bd=0, command=self.show_heatmap)
        self.map_button.pack(side="left", padx=20, pady=100)
        self.animate_button(self.map_button)


        self.category_button = tk.Button(self.trend_category_frame, text="Show Categories", font=("Poppins", 12), bg="#00C897", fg="white",
                                         bd=0, command=self.show_categories)
        self.category_button.pack(side="left", padx=20, pady=100)  
        self.animate_button(self.category_button)

    def animate_title(self):
        """Slide-in animation for title"""
        start_y = -100
        end_y = 0
        steps = 20
        for i in range(steps + 1):
            y = start_y + (end_y - start_y) * i / steps
            self.title_label.after(i * 20, lambda y=y: self.title_label.place(relx=0.5, rely=0.1, anchor="center", y=y))

    def animate_button(self, button):
        """Pulse animation for buttons"""
        def pulse():
            for i in range(4):
                bg = "#FF8A80" if i % 2 == 0 else "#FF6F61" if button == self.map_button else "#00E0A8" if i % 2 == 0 else "#00C897"
                button.after(i * 50, lambda b=bg: button.config(bg=b))
        button.bind("<Button-1>", lambda e: pulse())
        self.root.after(500, pulse)  

    def show_heatmap(self):
        map_file = generate_heatmap()
        webbrowser.open(f"file://{os.path.abspath(map_file)}")
        messagebox.showinfo("Heatmap", "Crime Heatmap opened in your browser!")

    def show_trends(self):
        plot_crime_trends()
        self.display_image("trend_plot.png")

    def show_categories(self):
        plot_crime_categories()
        self.display_image("category_plot.png")

    def display_image(self, filepath):
        img = Image.open(filepath)
        img = img.resize((500, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        if hasattr(self, 'img_label'):
            self.img_label.config(image=photo)
            self.img_label.image = photo
        else:
            self.img_label = tk.Label(self.analytics_frame, image=photo, bg="#EDEFFA")
            self.img_label.image = photo
            self.img_label.pack(pady=10)
        self.animate_image_pulse()

    def animate_image_pulse(self):
        """Pulse effect for displayed images"""
        for i in range(4):
            bg = "#E6E9F5" if i % 2 == 0 else "#FFFFFF"
            self.img_label.after(i * 100, lambda b=bg: self.img_label.config(bg=b))

    def update_stats(self):
        total_crimes = len(df)
        top_category = df['Category'].mode()[0]
        stats_text = f"Total Crimes: {total_crimes} | Most Common Category: {top_category}"
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrimeDashboardApp(root)
    root.mainloop()
