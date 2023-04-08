import base64
import json
import boto3
import csv
import io
from datetime import datetime, timedelta
import urllib3
import requests


def get_oauth_token(key, secret):
    '''Function creates personalised idealista token from key secret pair.'''
    
    message = key + ":" + secret # Combine the API key and  secret to personalised message
    auth = "Basic " + base64.b64encode(message.encode("ascii")).decode("ascii") # Encode the message   
    headers = {"Authorization" : auth, "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"} # Define headers   
    params = {"grant_type" : "client_credentials", "scope" : "read"} # Define request params
    request = requests.post("https://api.idealista.com/oauth/token", headers=headers, params=params)  # Perform the request with the api url, headers and params
    token = json.loads(request.text)['access_token'] # Obtain  personalised token, as a json  

    return token
    
    
# function to create search url
def define_request_url(operation):
    '''Function combines search parameters with the url to create search url for request.'''
    
    config = {
       'base_url': 'https://api.idealista.com/3.5/',
       'country': 'es',
       'max_items' : '50',
       'order' : 'distance',
       'center' : '39.4693441,-0.379561',
       'distance' : '1500',
       'property_type' : 'homes',
       'sort' : 'asc',
       'minSize' : '100',
       'maxSize' : '160',
       'elevator' : 'True',
       'airConditioning' : 'True',
       'preservation' : 'good',
       'language': 'en'
       }
    
    url = (config['base_url'] 
           + config['country'] 
           +'/search?operation=' + operation 
           +'&maxItems=' + config['max_items'] 
           + '&order=' + config['order'] 
           + '&center=' + config['center'] 
           + '&distance=' + config['distance'] 
           + '&propertyType=' + config['property_type'] 
           + '&sort=' + config['sort'] 
           + '&minSize=' +config['minSize']
           + '&maxSize=' + config['maxSize']
           + '&numPage=%s' 
           + '&elevator=' + config['elevator'] 
           #+'&airConditioning' + config['airConditioning']
           + '&preservation' + config['preservation'] 
           + '&language=' + config['language'])
    
    return url


# function to request data from idealista API
def query_api(key, secret, url):  
    '''Function uses requests package to query the idealista API with given token and search url.'''
    
    token = get_oauth_token(key, secret) # get the personalised token  
    headers = {'Content-Type': 'Content-Type: multipart/form-data;', # define the search headers  
               'Authorization' : 'Bearer ' + token}

    content = requests.post(url, headers = headers) # return the content from the request  

    if content.text == '': # Transform the result as a json file
        print('Error: Exceeded API call limit or wrong parameters')
        result = None
    else: result = content.text #json.loads(content.text)   

    return result


def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    bucket = 'valencialistings'
    
    now=datetime.now()
    date_time=now.strftime('%Y%m%d_%H%M%S')

    # SALE #####################################################################

    # idealista acces key and secret leo
    key_leo = ''
    secret_leo = ''

    url = define_request_url('sale')
    page = 1
    total_pages = 5
    
    # loop through all pages
    while page <= total_pages:
        
        url_of_page = url %(page)   
        page_result_json = query_api(key_leo, secret_leo, url_of_page) 
        page_result = json.loads(page_result_json)
        total_pages = page_result['totalPages']
        
        filename='sale_' + date_time + '_' + str(page) + '.json'
        
        s3.put_object(
            Bucket=bucket, 
            Key=filename,
            Body=page_result_json
            )
        
        page += 1
    
    print('Put sales file complete, ' + str(total_pages) + ' page written to S3')
    
    # RENT #####################################################################
    
    # idealista acces key and secret paula
    key_pau = ''
    secret_pau = ''
    
    url = define_request_url('rent')
    page = 1
    total_pages = 5
    
    # loop through all pages
    while page <= total_pages:
        
        url_of_page = url %(page)   
        page_result_json = query_api(key_pau, secret_pau, url_of_page) 
        page_result = json.loads(page_result_json)
        total_pages = page_result['totalPages']
        
        filename='rent_' + date_time + '_' + str(page) + '.json'
        
        s3.put_object(
            Bucket=bucket, 
            Key=filename,
            Body=page_result_json
            )
        
        page += 1
    
    print('Put rent file complete, ' + str(total_pages) + ' page written to S3')
    
    
    return {
        'statusCode': 200,
    }
