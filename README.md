# Energy Volatility Prediction
### UMBC Fall 2021 Data Science Capstone
### Instructions for use:
1. We have a data folder saved on our google drive as a shared drive. This contains the data gathered and processed in the notebooks found in this repository.
  a. Permission is required to access this folder (our professor has permission).
2. Open google colab and clone this repository into the environment.
3. Run the code of any notebook you desire- if asked to mount your drive, select the email address we have shared the drive with, and copy and paste the link.
4. Since the shared folder should show up as part of your shared drive at the user end, the folder paths should all work.
## Data: 2001-2020
**Electricity Price**<br>
We have monthly electricity price data by state. The average and standard deviation price was calculated for each state for each year which were used to calculated the coefficient of variation as such: (standard deviation of price across all months in a year)/(mean price across all months in a year).<br>
**Powerplant**<br>
We have historical power generation data from each plant in the United States on a monthly basis. This was aggregated to an annual level.<br>
**Weather**<br>
We have monthly historical temperatures and palmer drought severity index values (pdsi) across the US gridded at a 60km x 60km resolution. Data from 1981 to 2000 was used to calculate averages and standard deviations from each of these locations. These were used to standardize the data for our years of interest (2001-2020). This data is aggregated to a state level. Currently, we are using three derived terms; number of summer months with temperatures above 1 standard deviation above the mean, number of winter months with temperatures below 1 standard deviation below the mean, and number of months with a pdsi value lower than 1 standard deviation below the mean (the lower the pdsi, the worse the drought).<br>
**Futures Contracts**<br>
We started with daily open, high, low, close, and volume for the following futures contracts; NG (natural gas), CL (crude oil), BZ (brent crude oil), and HO (heating oil). Daily price movement was derived as the difference between the high and low price for each day. A moving average and standard deviation of the price movement and volume was used to standardize these variables. For each year and futures symbol, the total number of days with above average price movement and volume is calculated (the current names of these variables is misleading and should be changed).<br>
