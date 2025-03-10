import pandas as pd 


ctd_file = pd.read_csv("20081129_0652_CTDDATA.dat", names=['Date', 'Time', 'Depth (m)', 'Temperature (celsius)', 'Salinity (psu)'], delimiter="\t")

ctd_dataframe = pd.DataFrame(ctd_file)

print(ctd_dataframe)
                                                          
                       



                       