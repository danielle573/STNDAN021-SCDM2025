import pandas as pd 


ctd_file = pd.read_csv("../../Desktop/Assignments/BIO5012W/SCDM/P1_Assignment/20081129_0652_CTDDATA.csv", delimiter=";")

ctd_dataframe = pd.DataFrame(ctd_file)

print(ctd_dataframe)

        
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=1,ncols=2, sharey=True)

depth_column = ctd_dataframe["Depth  (m)"]
reversed_temperature_column = ctd_dataframe["Temperature (celsius)"][::-1]
reversed_salinity_column = ctd_dataframe["Salinity (psu)"][::-1]
reversed_depth_column = ctd_dataframe["Depth  (m)"][::-1]

axes[0].plot(reversed_temperature_column, reversed_depth_column, color= "red")
    
axes[1].plot(reversed_salinity_column, reversed_depth_column, color="blue")

axes[0].invert_yaxis()
axes[1].invert_yaxis()
axes[0].set_ylim(max(depth_column), 0)
axes[1].set_ylim(max(depth_column), 0)

axes[0].set_xlabel("Temperature (celsius)")
axes[0].set_ylabel("Depth  (m)")

axes[1].set_xlabel("Salinity (psu)") 

fig.suptitle("Temperature and Salinity data collected from CTD on the 29th of November 2008 at 06:52.")

plt.figure(figsize=(12, 6))
plt.show()                    

fig.savefig("CTD_Profiles", bbox_inches='tight')
