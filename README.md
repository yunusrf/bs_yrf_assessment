
Thank you for providing opportunity to participate in the assessment process.
Please find the information on the exercises attempted below.

### Exercise 1: Machine Learning Application - Multifidelity Climate Modelling

- Due to time restrictions and research into potential solutions, this assignment is only partially completed. Please see the notebook ['Machine_Learning_Climate_Modelling_Assessment.ipynb'](https://github.com/yunusrf/bs_yrf_assessment/blob/main/Machine_Learning_Climate_Modelling_Assessment.ipynb)
 
##### Possible Approach

-   After reading some literary works. In order to solve this issue, I advise following the recommendations made in the recent paper "Computationally-Efficient Climate Predictions using Multi-Fidelity Surrogate Modelling" ([https://arxiv.org/abs/2109.07468](https://arxiv.org/abs/2109.07468))
- The goal is to use multi-fidelity surrogate modeling based on the Gaussian process to generate high-fidelity climate predictions at a reasonable cost. The authors used the same dataset to test the approach to produce high-fidelity temperature predictions for a mountainous region on the coastline of Peru.
- mukit and GPy are two programs that can be used to implement the models. 

##### Software
Emukit and GPy are two programs that can be used to implement the models. Scikit-learn also provides a `GaussianProcessRegressor` for implementing [GP regression models](http://scikit-learn.org/stable/modules/gaussian_process.html#gaussian-process-regression-gpr).

### Exercise 2: Numerical Modelling

#### Task 1: Data handling and analysis

a. Automatically downloads GFS data from the NOMADS Grib filter service for both resolutions of the GFS gridded data sets, for any desired cycle and only at the given area-of-interest. Provide the cycle information as a script argument.

-  The service to get the grib files (wind, pressure, and temperature) from the nomads NOAA site is implemented by the script ['grib_data_downloader.py'](https://github.com/yunusrf/bs_yrf_assessment/blob/main/grib_data_downloader.py) . This script is invoked from a wrapper script ['download_app.py'](https://github.com/yunusrf/bs_yrf_assessment/blob/main/download_app.py).   The files are downloaded to folder ['**/grib/(wind,pressure,tmpr)**'](https://github.com/yunusrf/bs_yrf_assessment/tree/main/grib/res-0.25)
-  Based on the specified resolution and amount of detail, this script downloads the GRIB data.
	For exmaple: level of detail p25 for the 0.25 Degree resolution, p50 for 0.50 Degree and p1 --> 1 Degree
	- Sample command:  python download_app.py -l "p25" 
		If no arguments passed - it runs with default level of detail p25
- It is assumed that NOMADS Grib filter service generates new files every six hours . The downloaded script handles the cycle internally using timelist = ['00', '06', '12', '12']	
- The written script  specifies the ROI  as (leftlon=0 rightlon=360 toplat=90 bottomlat=-90) . The ROI can be set by changing rhe configured string. Note: When using the proposed ROI, which is 161°E to 180°E and 51°S to 31°S, the URL produced name issues. When using resolutions 0.5 and 1, the server reported URL name problems with this script. Just a quick reminder: it has been noted that if the script is ran without pausing, the server will bolk the IP.
- The sample downloaded data from this script is available in the folder 'grib' ( for wind,pressure,temperature).
	
b. The script should produce plots from the downloaded data that show the differences in relevant variables between both data sets, highlighting the implications from use of each boundary condition for the atmospheric models.
- The Jupyter Python notebook 'grib_reader.ipynb' implements simple code to view the downloaded GRIB file data. This script t is tested to read the files for resolution 0.25  degree only. URL naming issues rased by the server when trying  resolution 0.5 and 1 from GRIB data downloader script.

c. Comment on which data set you think is more suitable for operational usage, considering the differences you have observed. For example, will the increase in the model resolution significantly improve surface wind, temperature, or hydrological processes justify the operational implications such as larger file-sizes and longer download times?
- Since I am unable to get the dataset for multiple resolutions using automated script, I am unable to remark much on this. Generally the model with high resolution perform well, but has the cost of memory due to large files and also the taks to handle download times will be challenging.


#### Task 2: The WRF model set up

- This task is NOT attempted

#### Task 3: Data Assimilation

 * This task is NOT attempted


### Exercise 3: Data Science

#### Task 1: Reanalysis data over Queenstown Airport

	Followed the instructions to get the Subset data from mentioned server.

#### Task 2: Analysis of the CFSRv2 data at Queenstown and Auckland Airports

  Answer the following questions:

1. How well do the distributions of wind speed, temperature and rainfall from the CFSRv2 data compare with the distributions of the observations at Queenstown and Auckland airports for 2018?
		My comments:
	- Jupyter notebook ['analysis_cfsrv2_data.ipynb'](https://github.com/yunusrf/bs_yrf_assessment/blob/main/analysis_cfsrv2_data.ipynb) has the code for analysis of the CFSRv2 data at Queenstown and Auckland Airports ( Supplied csv files)
	- Exploratory Data Analysis in addition to Data Cleaning for the two datasets separately (Auckland Airport and Queenstown Airport)
	 - Plotting the overall data and analysis of specific year 2018 data
	 - Plotting the data to see behavior in different seasons 
	 - Resample the data if required to understand clearly
	 - Provided the correlation plots
	 - Pair Plots to show the correlation of Temperature, Wind Speed and Rainfall 

2. Is there a difference in performance of the CFSR data at Queenstown and Auckland airports. If so, why might this be?
	- Compared distribution of the  variables using two-sample Kolmogorov-Smirnov test (included in the library scipy.stats).  The library denotes the results in the form : KstestResult(statistic=0.04362990516103345, pvalue=9.866535240977302e-08). 
	- Under the null hypothesis the two distributions are identical. If the K-S statistic is small or the p-value is high (greater than the significance level, say 5%), then we cannot reject the hypothesis that the distributions of the two samples are the same. Conversely, we can reject the null hypothesis if the p-value is low. ( For the results specific to two datasets of Airports see the Jupyter notebook "analysis_cfsrv2_data.ipynb" )
	

3. Why did you choose the performance measures you did in answering the previous two questions?
	- We look at p-value to judge how extreme the statistic (which is the "distance" between two distributions here) is. So if p-value is less than 0.05 it means we reject the null hypothesis.


#### Task 3: Improving the CFSRv2 data at Queenstown and Auckland Airports regarding wind speed

Outline the process you would take to improve the CFSRv2 wind speed data at Queenstown Airport and Auckland Airport given the observational data sets for 2018. Give some measure of the improvement that could be expected. Run the improvement process over the data for January 2019 at both locations
- This task is NOT attempted

### Exercise 4: Data Science

Can you write some code to solve this problem and discuss the complexity of your solution?

- The script ['exercise_4.py'](https://github.com/yunusrf/bs_yrf_assessment/blob/main/exercise_4.py)  implements the code to  display top-k numbers that appear more frequently in a given list of N real numbers
- The script execute output of two samples lists given. Run the script using the command : 'python exercise_4.py'
	Sample Output:
		Input Array  to get top 3 - [9, 4, 2, 1, 1, 3, 8, 4, 2, 9, 2]
		['2 : 3 times', '9 : 2 times', '4 : 2 times']
		Input Array  to get top 5 - [15, 12, 11, 13, 12, 15, 16, 17, 100]
		['15 : 2 times', '12 : 2 times', '11 : 1 time', '13 : 1 time', '16 : 1 time']
- Complexity Analysis using the big O notation: 
	Time Complexity: O( n * k ). ( where n = length of input array and k is length of array_nums)
	In each traversal the temp array of size k (length of array_nums) is traversed, So the time Complexity is O( n * k ).
	Space Complexity: O(n). To store the elements O(n) space is required.	
