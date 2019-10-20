# Tetrapod-Spaceapps2019

ICESat-2 photon datas are used to detecting landslide  


TRY DEMO APP @ 
[INVISION](https://projects.invisionapp.com/prototype/ooo-ck1y9xme40014k901k48oks69/play/b99d0579)

# DOC

BEFORE START
YOU NEED A [NASAEARTH](https://urs.earthdata.nasa.gov/users/new?client_id=KImTfO7IF9gBW0uORyB2Ag&redirect_uri=https%3A%2F%2Fnsidc.org%2Fearthdata%2Fdrupal%2Flogin&response_type=code&state=node%2F46766) ACCOUNT TO DOWLOAND DATA


'data_dowloander.py' is a python script allow you to dowloand ICESat-2 data at spesific time range we used for get data to our app


you need to specify few thing : NASAEARTH USERRNAME-PASSWORD-THE MAIL WHICH ACCOUNT YOU REGISTERED | [ICESat-2 ID](https://nsidc.org/data/icesat-2/data-sets) | TIME RANGE (THERE IS NO DATA BEFORE 2018/10/14 !!) | 2-latitude 2-longitude for restrict the field

# WHY ?
In our world there is alot of trouble with natural disaster. 
They cause severe damage to artifects and destroy human lifes.
One of this natural disaster called landslide.

# HOW? 
We compared returned photon datas according to their confidence 

At Graph 2 lanslide threat level is more than Graph 1 
results are calculating by returned photon frequency 

> Graph 1
![photon_data](https://raw.githubusercontent.com/Mustaley/tetrapod-spaceapps/master/photon_data_graph_1.png)

> Graph 2  
![photon_data2](https://raw.githubusercontent.com/Mustaley/tetrapod-spaceapps/master/photon_data_graph_2.png)
 
