# Crimes Analysis and Visualization
This project provides an in-depth analysis of crime rates in three major cities in the United States: Los Angeles, Chicago, and New York. The objectives of this study are to compare and contrast crime rates across the three cities, identify the most prevalent types of crimes, and examine the trends in crime rates over the past year.
# WORKFLOW
1. Data Collection and Description: The crime dataset was retrieved from a JSON file source. (i) New York Data: This dataset spans from 1990 to 2021 and focuses on index crimes in New York. It includes information on seven categories of index crimes, encompassing murder, rape, robbery, aggravated assault, burglary, larceny theft, and motor vehicle theft. The dataset offers a comprehensive view of crime trends in New York over a substantial time period.
(ii) Los Angeles Data: Covering 2020 to the present, this dataset captures crime data in Los Angeles. The information is sourced from local law enforcement agencies and includes various categories of crimes such as homicide, assault, robbery, theft, and burglary. This dataset provides a more recent snapshot of crime trends in Los Angeles.
(iii) Chicago Data: Focused on the year 2022, this dataset provides insights into reported crimes in Chicago. The data, maintained by the Chicago Police Department, covers crime types including assault, robbery, theft, burglary, and certain sexual offences. Additionally, it indicates whether arrests were made and if crimes were committed by locals or visitors.

3. Data Processing Activities: The datasets underwent several key processes to prepare them for visualization:
   
A. Data Fetch: The initial step involved fetching the datasets from different sources in varying formats, including structured and semi-structured formats. The Los Angeles and New York City datasets were obtained in JSON format, while the Chicago City dataset was in Comma-Separated Values (CSV) format. Python programming language was employed for fetching these datasets.

B. Data Load: After downloading and retrieving the files, they were transformed into Pandas DataFrames for easier examination, allowing a better understanding of the data contained in each column. Subsequently, the resulting DataFrames were converted into JSON format, making it feasible to store them within a MongoDB database. MongoDB was chosen due to its flexibility in handling large volumes of unstructured and semi-structured data, making it an appropriate choice for the project's initial phase. It was also simple to set up a cloud instance of MongoDB to facilitate centralized storage of the different datasets.

C. ETL Automation:
The ETL (Extract, Transform, Load) process, a sequence of actions used to collect, modify, and load data, was automated. ETL is vital in combining data from multiple sources for analysis. Two ETL tools were used: Luigi and Apache Airflow. Luigi, developed by Spotify and open-sourced, is designed for building pipelines linked with sizable datasets that necessitate extended batch jobs. On the other hand, Apache Airflow enables automation, monitoring, and scheduling of processes. It is structured around Directed Acyclic Graphs (DAGs) representing workflow tasks. These tools extracted data from MongoDB, executed data cleaning (such as handling missing or duplicate values), and removed unnecessary columns. The structured data was then stored in a PostgreSQL database, created for well-defined schema and intricate queries. Python was selected as the programming language due to its popularity in the data science domain and its robust libraries for data analysis. The Jupyter Notebook environment was employed for data exploration and analysis. For data visualization, libraries like Matplotlib, Seaborn, and Plotly were used, generating a range of visualizations including scatter plots, histograms, and bar charts.
# RESULTS AND EVALUATION
The analysis of crime data from major cities in the United States; Los Angeles, New York, and Chicago led to significant findings:

-CRIME TYPES WITH HIGH OCCURRENCE:
(i) Los Angeles: The most frequent crime types were Battery (Simple Assault), Theft of Identity, and Burglary of Vehicle. Car theft was also consistent across cities, with high occurrence rates in Los Angeles.
(ii) New York: Aggravated Assault and Larceny were the top crime types.
(iii) Chicago: Theft, Battery, and Motor Vehicle Theft were the primary crime types. Assault was consistent across the three cities.
These insights enable law enforcement agencies to focus resources on addressing the prevalent crime types, particularly emphasizing car theft and assault.

-TIME OF YEAR WITH HIGH CRIME INCIDENTS:
(i) Los Angeles: The first quarter of the year exhibited more crime incidents.
(ii) Chicago: There was a spike in crime incidents from July to August, coinciding with the summer period and an increased population due to vacations and activities.
This information allows police departments to allocate more resources during specific times, implement temporary measures, and design programs to engage students and youths constructively.

-CRIME TRENDS OVER TIME:
(i) Los Angeles: In 2022, crime rates were high, possibly attributed to increased police presence and innovative policing strategies.
(ii) Chicago: Certain crime types, such as stalking and sexual offences, exhibited a rising trend, necessitating focused attention.

-DEMOGRAPHICS AND CRIME:
(i) Victims Age: Most victims in Los Angeles were between 20 and 50 years old, with a notable number under 10 years old.
(ii) Victims Gender: Males were more frequently victimized in Los Angeles.
(iii) Victims Descent: Over 80% of victims' descent in Los Angeles were Hispanic.
These demographic insights offer a clearer picture of crime's impact on specific groups.

-GUN-RELATED CRIMES:
In Chicago, robberies and assaults with pistols were prevalent, highlighting the concerning issue of gun-related crimes and the potential link to gun ownership rates in the US.

-TEMPORAL TRENDS:
(i) Crime occurrences increased over the years in Los Angeles.
(ii) In New York, violent crimes increased in 2020 compared to the previous year.

# TOOLS USED
1. Python: Python programming language serves as the primary programming tool for data manipulation, analysis, and visualization. Its extensive libraries and frameworks for data science and analytics contributed to efficient data handling.
2. Luigi: Luigi, a Python-based tool developed by Spotify, played a key role in automating the Extract, Transform, Load (ETL) pipeline. It was employed to create workflows and pipelines for managing the data extraction, cleaning, and loading processes.
3. MongoDB: MongoDB was utilized as a NoSQL database to store the initial datasets and the intermediate data resulting from the ETL process. Its flexibility with unstructured and semi-structured data made it a suitable choice for the project's requirements.
4. PostgreSQL: PostgreSQL, a relational database management system, was chosen to store structured data that required well-defined schemas and complex querying capabilities. It was particularly useful for housing the refined and structured data after the ETL process.
5. Jupyter Notebook: Jupyter Notebook provides an interactive environment for data exploration, analysis, and code execution. Its integration of code, visualizations, and explanatory text was valuable for documenting and sharing the analysis process.
6. Docker: Docker, a platform for containerization, played a role in ensuring consistent environments across different stages of the project. It aids in packaging applications and their dependencies into isolated containers, which can enhance reproducibility and portability.
# LIMITATIONS AND SUGGESTIONS FOR FUTURE WORK
The project's analysis of crime trends in Los Angeles, Chicago, and New York yielded valuable insights into variations in crime rates, types, temporal patterns, and geographic concentrations among these cities. The findings underscored the importance of data-driven decision-making in shaping effective strategies for crime reduction. The study acknowledged limitations in data quality and biases while recommending future work to incorporate diverse crime-related data sources, consider socioeconomic and demographic trends, and explore predictive technologies like machine learning and AI. 
