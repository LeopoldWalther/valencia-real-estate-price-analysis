# valencia-real-estate-price-analysis
An analysis of Valencian real estate prices using the Idealist API.

### Table of Contents

- [valencia-real-estate-price-analysis](#valencia-real-estate-price-analysis)
    - [Table of Contents](#table-of-contents)
  - [Installation ](#installation-)
  - [Project Motivation](#project-motivation)
  - [File Descriptions ](#file-descriptions-)
  - [Results](#results)
  - [Licensing, Authors, Acknowledgements](#licensing-authors-acknowledgements)

## Installation <a name="installation"></a>

The project was created with Python 3.9.11. The requirements.txt file contains alle necessary libraries.

## Project Motivation<a name="motivation"></a>

Motivation of this project was to find out how the real estate market of Valencia is behaving. Especially the following questions should be answered with data:

1. What are the average prices in the different districts/neighborhoods of Valencia?
2. What area in Valencia has the best raito rent/sale price?
3. What are the renting prices in the different districts/neighborhoods of Valencia?
4. Are sale prices for flats in the city centre of Valencia rising or falling over time?
5. How long are sale listings publicated before the flat is bought?

In Spain the most popular website to offer and search real estate is Idealista. Idealista offers an API to download current listings. To answer the above questions it is only necessary to periodically download listings which are for sale or rent. With the data obtaines it is possible to create a time series of sales and rent prices and to create statistics over different districts/neighborhoods.



## File Descriptions <a name="files"></a>

StackOverflow_Survey/
│
├── data/
├── documentation/
├── images/
├── lambda_layers/
├── LICENSE
├── README.md
├── requirements.txt
├── valenciaHousingAnalysis.cfg
├── valenciaIdealistaSalesRentLambda.py
├── valenciaRealEstatePriceAnalysis.ipynb

The jupyter notebook 'valenciaRealEstatePriceAnalysis.ipynb' is used as development environment to test the code before deploying it in a Lambda Function.

## Results<a name="results"></a>

As the Idealista API only allows 100 Requests per month with each request containing a maximum of 50 listings, it was necessary to reduce the data requested with filters and the download frequency to once a week.
The code to request data from the Idealista API is run via an AWS Lamba function once per week and downloads the results as JSON files to an AWS S3 bucket.

The following filter are applied when requesting the idealista API:

'property_type' : 'homes',
'center' : '39.4693441,-0.379561',
'distance' : '1500',
'minSize' : '100',
'maxSize' : '160',
'elevator' : 'True',
'preservation' : 'good',
'order' : 'distance',
'sort' : 'asc',

The combination of center and distance leads to the following area of real estate listings:

![alt text](images/SearchRadius.png)


## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Feel free to use my code as you please. 
