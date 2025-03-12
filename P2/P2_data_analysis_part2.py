import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

SA_Agulhas_file = pd.read_csv("SAA2_WC_2017_metocean_10min_avg.csv")
SA_Agulhas_dataframe = pd.DataFrame(SA_Agulhas_file)
print(SA_Agulhas_dataframe)

SA_Agulhas_dataframe['TIME_SERVER'] = pd.to_datetime(SA_Agulhas_dataframe['TIME_SERVER'], format= '%Y/%m/%d %H:%M')
print(SA_Agulhas_dataframe.dtypes)
SA_Agulhas_dataframe.set_index('TIME_SERVER', inplace=True)
SA_Agulhas_dataframe = SA_Agulhas_dataframe.sort_index()

print(SA_Agulhas_dataframe)
print(SA_Agulhas_dataframe.isna())

departure_date_time = pd.to_datetime("2017/06/28 17:10")
arrival_date_time = pd.to_datetime("2017/07/04 23:59")
departure_to_arrival_data = SA_Agulhas_dataframe[(SA_Agulhas_dataframe.index >= departure_date_time) & (SA_Agulhas_dataframe.index <= arrival_date_time)]

# print(departure_to_arrival_data)

#temperature time series 
fig = plt.figure(figsize=(8,6))
plt.plot(departure_to_arrival_data.index, departure_to_arrival_data["TSG_TEMP"])
plt.title("Time Series of Sea Surface Temperature recorded between 2017/06/28-2017/07/04 on the SA Agulhas II cruise of Southern Ocean")
plt.xlabel("Time")
plt.ylabel("Sea Surface Temperature (degrees C)")
plt.style.use("grayscale")
plt.xticks([pd.to_datetime("2017/06/28 17:10"), pd.to_datetime("2017/07/04 23:59")], ["2017/06/28 17:10","2017/07/04 23:59"])
plt.figure(figsize=(12, 6))
fig.savefig("Time_Series_Profiles", bbox_inches='tight')
plt.show()

#plot histogram of salinity 
plt.style.use('default')
plt.figure(figsize=(10, 6))
plt.hist(departure_to_arrival_data["TSG_SALINITY"], bins=10, range=[30,35], color="blue", edgecolor="black")
plt.xlabel("Salinity (psu)")
plt.ylabel("Frequency")
plt.title("Salinity Distribution (30-35 PSU) on SA Agulhas II Cruise")
plt.savefig("Salinity_Histogram.png", bbox_inches="tight")
plt.show()


#Calculations (stats + dataframe)
mean_values = departure_to_arrival_data[["TSG_TEMP", "TSG_SALINITY"]].mean()
print(mean_values)
std_values = departure_to_arrival_data[["TSG_TEMP", "TSG_SALINITY"]].std()
print(std_values)
iqr_values = departure_to_arrival_data[["TSG_TEMP", "TSG_SALINITY"]].quantile(0.75) - departure_to_arrival_data[["TSG_TEMP", "TSG_SALINITY"]].quantile(0.25)
print(iqr_values) 

stats_table = pd.DataFrame({"Mean": mean_values,"Standard Deviation": std_values,"Interquartile Range": iqr_values})
stats_table.index = ["Temperature (°C)", "Salinity (PSU)"]
print("\n=== Temperature and Salinity Statistics ===\n")
stats_table.insert(0, "Parameter", ["Sea Surface Temperature (°C)", "Salinity (PSU)"])
print(stats_table)
plt.figure(figsize=(10, 1))

table = plt.table(cellText=stats_table.values, colLabels= stats_table.columns)
table.scale(3,4)
table.set_fontsize(14)
plt.axis('off')
plt.title("Table showing the mean, standard deviation and the interquartile range for temperature and salinity")
plt.savefig("statistics_table_for_P2", bbox_inches="tight")
plt.show()


#scatter plot of cloud 
def ddmm2dd(ddmm):        
    thedeg = np.floor(ddmm/100.)     
    themin = (ddmm-thedeg*100.)/60.     
    return thedeg+themin

plt.figure(figsize=(8, 6))
scatter = plt.scatter(departure_to_arrival_data['WIND_SPEED_TRUE'], departure_to_arrival_data['AIR_TEMPERATURE'], c= ddmm2dd(departure_to_arrival_data['LATITUDE']), cmap='viridis', edgecolors='k')

plt.colorbar(scatter, label="Latitude")


plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Air Temperature (°C)")
plt.title("Scatter Plot of Wind Speed vs Air Temperature")

plt.savefig("wind_vs_temp.png", dpi=300)
plt.show()

         
         
