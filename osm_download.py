import networkx as nx
import osmnx as ox

from argparse import ArgumentParser
import warnings
import shutil
import os

warnings.filterwarnings("ignore")
ox.settings.all_oneway = True
ox.settings.log_console = False

def load_osm(osm_func, osm_args, save_filename, save_folder="./data"):
    G = osm_func(*osm_args)
    path = f"{save_folder}/{save_filename}"
    ox.save_graph_xml(G, filepath=f"{path}.osm")

    print(f"Successfully saved OpenStreetMap data to {path}.osm")


def load_osm_buildings(osm_building_func, osm_building_args, save_filename, save_folder="/data"):
    gdf = osm_building_func(*osm_building_args)
    gdf = gdf.apply(lambda c: c.astype(str) if c.name != "geometry" else c, axis=0)

    path = f"{save_folder}/{save_filename}_buildings"
    gdf.to_file(f"{path}.shp", driver="GeoJSON")

    os.system(f"ogr2osm -f {path}.shp -o {path}.osm")
    os.remove(f"{path}.shp")
    print(f"Successfully saved OpenStreetMap Building data to {path}.osm")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--graph_load_mode", 
                        type=str, 
                        default="address", 
                        choices=["address", "bbox", "place", "point"])
    # address
    parser.add_argument("--address", type=str, default="Nanshan, Shenzhen, China")
    # point
    parser.add_argument("--point", type=str, default="114.0931,22.6696")
    parser.add_argument("--dist", type=int, default=1000)
    parser.add_argument("--dist_type", type=str, default="bbox", choices=["bbox", "network"])
    # place
    parser.add_argument("--query", type=str, default="Nanshan, Shenzhen, China")
    # bbox
    parser.add_argument("--bbox", type=str, default="113.9416,22.547,114.0931,22.6696")

    parser.add_argument("--network_type", type=str, default="walk", 
                        choices=["all_private", "all", "bike", "drive", "drive_service", "walk"])
    
    parser.add_argument("--save_folder", type=str, default="./data")
    args = parser.parse_args()

    feature_tags = {"building": True,}
    match args.graph_load_mode:
        case "address":
            osm_func = ox.graph_from_address
            osm_building_func = ox.features_from_address
            osm_args = [args.address, args.dist, args.dist_type, args.network_type]
            osm_building_args = [args.address, feature_tags, args.dist]
            filename = args.address.replace(", ", "_").lower()
        case "bbox":
            osm_func = ox.graph_from_bbox
            osm_building_func = ox.features_from_bbox
            bbox = [float(value) for value in args.bbox.split(",")]
            osm_args = [*bbox, args.network_type]
            osm_building_args = [*bbox, feature_tags]

            filename = [str(lat_lon).replace(".", "p") for lat_lon in bbox]
            filename = [f"{direction}{lat_lon}" for direction, lat_lon in zip(["north", "south", "east", "west"], filename)]
            filename = f"{"_".join(filename)}_dist{args.dist}"
        case "place":
            osm_func = ox.graph_from_place
            osm_building_func = ox.features_from_place
            osm_args = [args.query, args.network_type]
            osm_building_args = [args.query, feature_tags]
            filename = args.query.replace(", ", "_").lower()
        case "point":
            osm_func = ox.graph_from_point
            osm_building_func = ox.features_from_point
            center = tuple(float(value) for value in args.point.split(","))
            osm_args = [center, args.dist, args.dist_type, args.network_type]
            osm_building_args = [center, feature_tags, args.dist]

            filename = [str(lat_lon).replace(".", "p") for lat_lon in center]
            filename = f"center_{"_".join(filename)}_dist{args.dist}"
        case _:
            raise ValueError(f"{args.mode} is not a valid mode")

    shutil.rmtree(args.save_folder, ignore_errors=True)
    os.makedirs(args.save_folder, exist_ok=True)

    load_osm(osm_func, osm_args, filename, args.save_folder)
    load_osm_buildings(osm_building_func, osm_building_args, filename, args.save_folder)