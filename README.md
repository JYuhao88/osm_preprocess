# Installtion

## Create Environement
~~~bash
conda create -n ox -c conda-forge --strict-channel-priority osmnx
conda activate ox
pip install  -r requirements.txt
~~~

## Usage
Download OSM Data by following commands

### Address
~~~bash
python osm_download.py --graph_load_mode "address" --dist 1000 --dist_type "bbox" --save_folder "./data"
~~~

### Place
~~~bash
python osm_download.py --graph_load_mode "place" --query "Nanshan, Shenzhen, China" --save_folder "./data"
~~~

### Point (latiude, longitude)
~~~bash
python osm_download.py --graph_load_mode "point" --point "22.547,113.9416" --dist 1000 --dist_type "bbox"  --network_type "walk" --save_folder "./data"
~~~

### Bbox (north latitude, south latitude, east longitude, west longitude)
~~~bash
python osm_download.py --graph_load_mode "bbox" --bbox "22.5377,22.5193,113.9410,113.9174" --save_folder "./data"
~~~