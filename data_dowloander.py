import requests
import json
import requests, getpass, socket, json, zipfile, io, math, os, shutil, pprint, re, time
from statistics import mean
from requests.auth import HTTPBasicAuth
import os
# Earthdata Login 0

'''
    YOU NEED TO BE REGISTER TO NASA ERATH DATA
    https://urs.earthdata.nasa.gov/users/new?client_id=KImTfO7IF9gBW0uORyB2Ag&redirect_uri=https%3A%2F%2Fnsidc.org%2Fearthdata%2Fdrupal%2Flogin&response_type=code&state=node%2F46769
'''

uid = input('Earthdata Login user name: ')
pswd = getpass.getpass('Earthdata Login password: ')
email = input('Email address associated with Earthdata Login account: ')
#Input bounding box.



LL_lon = input('Input lower left longitude in decimal degrees: ')
LL_lat = input('Input lower left latitude in decimal degrees: ')
UR_lon = input('Input upper right longitude in decimal degrees: ')
UR_lat = input('Input upper right latitude in decimal degrees: ')


bounding_box = LL_lon + ',' + LL_lat + ',' + UR_lon + ',' + UR_lat
#Input temporal range 


start_date = input('Input start date in yyyy-MM-dd format: ')
start_time = input('Input start time in HH:mm:ss format: ')
end_date = input('Input end date in yyyy-MM-dd format: ')
end_time = input('Input end time in HH:mm:ss format: ')


temporal = start_date + 'T' + start_time + 'Z' + ',' + end_date + 'T' + end_time + 'Z'
#short_name = input('Input short name, e.g. ATL03, here: ')
short_name = 'ATL08'
params = {
    'short_name': short_name
}

cmr_collections_url = 'https://cmr.earthdata.nasa.gov/search/collections.json'
response = requests.get(cmr_collections_url, params=params)
results = json.loads(response.content)
versions = [el['version_id'] for el in results['feed']['entry']]
latest_version = max(versions)
print('The most recent version of ', short_name, ' is ', latest_version)
granule_search_url = 'https://cmr.earthdata.nasa.gov/search/granules'
params = {
    'short_name': short_name,
    'version': latest_version,
    'bounding_box': bounding_box,
    'temporal': temporal,
    'page_size': 100,
    'page_num': 1
}
granules = []
headers={'Accept': 'application/json'}

jsonlinks = []
all_links = []

while True:
    response = requests.get(granule_search_url, params=params, headers=headers)
    results = json.loads(response.content)

    
    if len(results['feed']['entry']) == 0:
        # Out of results
        break

    # Collect results
    granules.extend(results["feed"]["entry"])
    jsonlinks.append(results['feed']['id'])
    params['page_num'] += 1
for a in granules:
    #.H5 FORMATTED DATASETS 
    for c in a['links']:
        all_links.append(c['href'])
        #print(c['href'])
        if c['href'].endswith('.jpg') == True:    
            img_data = requests.get(c['href']).content
            def download():
                try:
                    os.chdir('./downloaded_img_data')
                except:
                    os.mkdir('./downloaded_img_data')
                with open(c['href'][63:], 'wb') as handler:
                    handler.write(img_data)
            download()
                #print(c['href'])
        


print('There are', len(granules), 'granules of', short_name, 'version', latest_version, 'over my area and time of interest.')
granule_sizes = [float(granule['granule_size']) for granule in granules]

#print(f'The average size of each granule is {mean(granule_sizes):.2f} MB and the total size of all {len(granules)} granules is {sum(granule_sizes):.2f} MB')





'''
from xml.etree import ElementTree as ET

capability_url = f'https://n5eil02u.ecs.nsidc.org/egi/capabilities/{short_name}.{latest_version}.xml'

# Create session to store cookie and pass credentials to capabilities url

session = requests.session()
s = session.get(capability_url)
response = session.get(s.url,auth=(uid,pswd))

root = ET.fromstring(response.content)

#collect lists with each service option

subagent = [subset_agent.attrib for subset_agent in root.iter('SubsetAgent')]

# variable subsetting
variables = [SubsetVariable.attrib for SubsetVariable in root.iter('SubsetVariable')]  
variables_raw = [variables[i]['value'] for i in range(len(variables))]
variables_join = [''.join(('/',v)) if v.startswith('/') == False else v for v in variables_raw] 
variable_vals = [v.replace(':', '/') for v in variables_join]

# reformatting
formats = [Format.attrib for Format in root.iter('Format')]
format_vals = [formats[i]['value'] for i in range(len(formats))]
format_vals.remove('')

# reformatting options that support reprojection
normalproj = [Projections.attrib for Projections in root.iter('Projections')]
normalproj_vals = []
normalproj_vals.append(normalproj[0]['normalProj'])
format_proj = normalproj_vals[0].split(',')
format_proj.remove('')
format_proj.append('No reformatting')

# reprojection options
projections = [Projection.attrib for Projection in root.iter('Projection')]
proj_vals = []
for i in range(len(projections)):
    if (projections[i]['value']) != 'NO_CHANGE' :
        proj_vals.append(projections[i]['value'])
        
# reformatting options that do not support reprojection
no_proj = [i for i in format_vals if i not in format_proj]

# SMAP-specific reprojection logic

#L1-L2 reprojection/reformatting options
if short_name == 'SPL1CTB' or 'SPL1CTB_E' or 'SPL2SMA' or 'SPL2SMP' or 'SPL2SMP_E' or 'SPL2SMAP': 
    format_proj = ['GeoTIFF', 'NetCDF4-CF', 'HDF-EOS5']
    no_proj = [i for i in format_vals if i not in format_proj]
elif short_name == 'SPL2SMAP_S' or 'SPL3SMA' or 'SPL3SMP' or 'SPL3SMP_E' or 'SPL3SMAP' or 'SPL3FTA' or 'SPL3FTP' or 'SPL3FTP_E' or 'SPL4SMAU' or 'SPL4SMGP' or 'SPL4SMLM' or 'SPL4CMDL': 
    format_proj = ['No reformatting', 'GeoTIFF', 'NetCDF4-CF', 'HDF-EOS5']
    no_proj = [i for i in format_vals if i not in format_proj]
    #print service information depending on service availability and select service options
    
if len(subagent) < 1 :
    print('No services exist for', short_name, 'version', latest_version)
    agent = 'NO'
    bbox = ''
    time_var = ''
    reformat = ''
    projection = ''
    projection_parameters = ''
    coverage = ''
else:
    agent = ''
    subdict = subagent[0]
    if subdict['spatialSubsetting'] == 'true':
        ss = input('Subsetting by bounding box, based on the area of interest inputted above, is available. Would you like to request this service? (y/n)')
        if ss == 'y': bbox = bounding_box
        else: bbox = ''
    if subdict['temporalSubsetting'] == 'true':
        ts = input('Subsetting by time, based on the temporal range inputted above, is available. Would you like to request this service? (y/n)')
        if ts == 'y': time_var = start_date + 'T' + start_time + ',' + end_date + 'T' + end_time 
        else: time_var = ''
    else: time_var = ''
    if len(format_vals) > 0 :
        print('These reformatting options are available:', format_vals)
        reformat = input('If you would like to reformat, copy and paste the reformatting option you would like (make sure to omit quotes, e.g. GeoTIFF), otherwise leave blank.')
        # select reprojection options based on reformatting selection
        if reformat in format_proj and len(proj_vals) > 0 : 
            print('These reprojection options are available with your requested format:', proj_vals)
            projection = input('If you would like to reproject, copy and paste the reprojection option you would like (make sure to omit quotes, e.g. GEOGRAPHIC), otherwise leave blank.')
            # Enter required parameters for UTM North and South
            if projection == 'UTM NORTHERN HEMISPHERE' or projection == 'UTM SOUTHERN HEMISPHERE': 
                NZone = input('Please enter a UTM zone (1 to 60 for Northern Hemisphere; -60 to -1 for Southern Hemisphere):')
                projection_parameters = str('NZone:' + NZone)
            else: projection_parameters = ''
        else: 
            print('No reprojection options are supported with your requested format')
            projection = ''
            projection_parameters = ''
    else: 
        reformat = ''
        projection = ''
        projection_parameters = ''
# Select variable subsetting

if len(variable_vals) > 0:
        v = input('Variable subsetting is available. Would you like to subset a selection of variables? (y/n)')
        if v == 'y':
            print('The', short_name, 'variables to select from include:')
            print(*variable_vals, sep = "\n") 
            coverage = input('If you would like to subset by variable, copy and paste the variables you would like separated by comma (be sure to remove spaces and retain all forward slashes: ')
        else: coverage = ''

#no services selected
if reformat == '' and projection == '' and projection_parameters == '' and coverage == '' and time_var == '' and bbox == '':
    agent = 'NO'
#Set NSIDC data access base URL
base_url = 'https://n5eil02u.ecs.nsidc.org/egi/request'

#Set the request mode to asynchronous if the number of granules is over 100, otherwise synchronous is enabled by default
if len(granules) > 100:
    request_mode = 'async'
    page_size = 2000
else: 
    page_size = 100
    request_mode = 'stream'

#Determine number of orders needed for requests over 2000 granules. 
page_num = math.ceil(len(granules)/page_size)

print('There will be', page_num, 'total order(s) processed for our', short_name, 'request.')
#Create request parameter dictionary
param_dict = {'short_name': short_name, 
                  'version': latest_version, 
                  'temporal': temporal, 
                  'time': time_var, 
                  'bounding_box': bounding_box, 
                  'bbox': bbox, 
                  'format': reformat, 
                  'projection': projection, 
                  'projection_parameters': projection_parameters, 
                  'Coverage': coverage, 
                  'page_size': page_size, 
                  'request_mode': request_mode, 
                  'agent': agent, 
                  'email': email, }

#Remove blank key-value-pairs
param_dict = {k: v for k, v in param_dict.items() if v != ''}

#Convert to string
param_string = '&'.join("{!s}={!r}".format(k,v) for (k,v) in param_dict.items())
param_string = param_string.replace("'","")

#Print API base URL + request parameters
endpoint_list = [] 
for i in range(page_num):
    page_val = i + 1
    API_request = api_request = f'{base_url}?{param_string}&page_num={page_val}'
    endpoint_list.append(API_request)

print(*endpoint_list, sep = "\n") 
# Create an output folder if the folder does not already exist.

path = str(os.getcwd() + '/Outputs')
if not os.path.exists(path):
    os.mkdir(path)

# Different access methods depending on request mode:

if request_mode=='async':
    # Request data service for each page number, and unzip outputs
    for i in range(page_num):
        page_val = i + 1
        print('Order: ', page_val)

    # For all requests other than spatial file upload, use get function
        request = session.get(base_url, params=param_dict)

        print('Request HTTP response: ', request.status_code)

    # Raise bad request: Loop will stop for bad response code.
        request.raise_for_status()
        print('Order request URL: ', request.url)
        esir_root = ET.fromstring(request.content)
        print('Order request response XML content: ', request.content)

    #Look up order ID
        orderlist = []   
        for order in esir_root.findall("./order/"):
            orderlist.append(order.text)
        orderID = orderlist[0]
        print('order ID: ', orderID)

    #Create status URL
        statusURL = base_url + '/' + orderID
        print('status URL: ', statusURL)

    #Find order status
        request_response = session.get(statusURL)    
        print('HTTP response from order response URL: ', request_response.status_code)

    # Raise bad request: Loop will stop for bad response code.
        request_response.raise_for_status()
        request_root = ET.fromstring(request_response.content)
        statuslist = []
        for status in request_root.findall("./requestStatus/"):
            statuslist.append(status.text)
        status = statuslist[0]
        print('Data request ', page_val, ' is submitting...')
        print('Initial request status is ', status)

    #Continue loop while request is still processing
        while status == 'pending' or status == 'processing': 
            print('Status is not complete. Trying again.')
            time.sleep(10)
            loop_response = session.get(statusURL)

    # Raise bad request: Loop will stop for bad response code.
            loop_response.raise_for_status()
            loop_root = ET.fromstring(loop_response.content)

    #find status
            statuslist = []
            for status in loop_root.findall("./requestStatus/"):
                statuslist.append(status.text)
            status = statuslist[0]
            print('Retry request status is: ', status)
            if status == 'pending' or status == 'processing':
                continue

    #Order can either complete, complete_with_errors, or fail:
    # Provide complete_with_errors error message:
        if status == 'complete_with_errors' or status == 'failed':
            messagelist = []
            for message in loop_root.findall("./processInfo/"):
                messagelist.append(message.text)
            print('error messages:')
            pprint.pprint(messagelist)

    # Download zipped order if status is complete or complete_with_errors
        if status == 'complete' or status == 'complete_with_errors':
            downloadURL = 'https://n5eil02u.ecs.nsidc.org/esir/' + orderID + '.zip'
            print('Zip download URL: ', downloadURL)
            print('Beginning download of zipped output...')
            zip_response = session.get(downloadURL)
            # Raise bad request: Loop will stop for bad response code.
            zip_response.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
                z.extractall(path)
            print('Data request', page_val, 'is complete.')
        else: print('Request failed.')
            
else:
    for i in range(page_num):
        page_val = i + 1
        print('Order: ', page_val)
        print('Requesting...')
        request = requests.get(base_url, params=param_dict)
        print('HTTP response from order response URL: ', request.status_code)
        request.raise_for_status()
        d = request.headers['content-disposition']
        fname = re.findall('filename=(.+)', d)
        dirname = os.path.join(path,fname[0].strip('\"'))
        print('Downloading...')
        open(dirname, 'wb').write(request.content)
        print('Data request', page_val, 'is complete.')
    
    # Unzip outputs
    for z in os.listdir(path): 
        if z.endswith('.zip'): 
            zip_name = path + "/" + z 
            zip_ref = zipfile.ZipFile(zip_name) 
            zip_ref.extractall(path) 
            zip_ref.close() 
            os.remove(zip_name) 
# Clean up Outputs folder by removing individual granule folders 

for root, dirs, files in os.walk(path, topdown=False):
    for file in files:
        try:
            shutil.move(os.path.join(root, file), path)
        except OSError:
            pass
    for name in dirs:
        os.rmdir(os.path.join(root, name))   






r = requests.get('https://api.opencagedata.com/geocode/v1/json?q={},{}&key=bb96fa530eeb49129611efce17a18b76'.format(provience_name,country_name))
cordx = r.json()['results'][0]['annotations']['Mercator']['x']
cordy = r.json()['results'][0]['annotations']['Mercator']['y']

count_month = 1
count_day = 1

while count_day < 30:
    link = 'http://openaltimetry.org/data/icesat2/elevation?maxx={}&maxy={}&zoom_level=10&beams=1,2,3,4,5,6&tracks=680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695&date=2018-{}-{}&mapType=geographic'.format(cordx,cordy,count_month,count_day)
    re = requests.get(link)
    print(re.content)
    count_day += 1
    if count_day == 30:
        count_day = 1
        country_name +=1
'''