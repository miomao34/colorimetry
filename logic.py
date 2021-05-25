import json
import csv
import colour
from colour.plotting import *
from typing import Dict, List, Union
from scipy.interpolate import interp1d

DEFAULT_CONFIG = 'default-config.json'

def read_config(filename: str = None) -> Dict:
    # has to be flat; values not present in provided config will be substituted with values from the default config
    if filename is None:
        with open(DEFAULT_CONFIG, 'r') as default_config_file:
            config = json.load(default_config_file)
            return config
    
    with open(DEFAULT_CONFIG, 'r') as default_config_file, \
    open(filename, 'r') as config_file:
        default_config = json.load(default_config_file)
        config = json.load(config_file)
        
    for key in default_config.keys():
        config[key] = default_config[key] if key not in config else config[key]
    return config

def get_value(row: List, index: int) -> float:
    if isinstance(row[index], str):
        return float(row[index].replace(',','.'))
    return row[index]

def get_interpolated_data(filename: str, row_begin: int, wl_column: int, norm_column: int) -> Dict:
    raw = {}
    with open(filename) as file:
        reader = csv.reader(file)

        index = 0
        for row in reader:
            # skip header
            if index < row_begin - 1:
                index = index + 1
                continue

            # a bit dirty but will do for now
            raw[get_value(row, wl_column - 1)] = get_value(row, norm_column - 1)

            index = index + 1
        
        wavelengths = [i for i in range(360, 830+1)]
        function = interp1d(list(raw.keys()), list(raw.values()), kind='cubic')

        retval = {}

        for value in wavelengths:
            retval[value] = function(value)
        
        return retval


def get_data(config: Dict) -> Union[Dict, Dict, Dict]:
    x_raw, y_raw, z_raw = {}, {}, {}
    with open(config['filename']) as file:
        reader = csv.reader(file)

        index = 0
        for row in reader:
            # skip header
            if index < config['row_begin'] - 1:
                index = index + 1
                continue

            # checking if all values exist; if not, return existing 
            # -1 is for normal language column numbering
            if not row[config['x_wl_column'] - 1] or \
            not row[config['x_norm_column'] - 1] or \
            not row[config['y_wl_column'] - 1] or \
            not row[config['y_norm_column'] - 1] or \
            not row[config['z_wl_column'] - 1] or \
            not row[config['z_norm_column'] - 1]:
                break

            # a bit dirty but will do for now
            x_raw[get_value(row, config['x_wl_column'] - 1)] = get_value(row, config['x_norm_column'] - 1)
            y_raw[get_value(row, config['y_wl_column'] - 1)] = get_value(row, config['y_norm_column'] - 1)
            z_raw[get_value(row, config['z_wl_column'] - 1)] = get_value(row, config['z_norm_column'] - 1)
            # if get_value(row, config['x_wl_column'] - 1) >= 360 and get_value(row, config['x_wl_column'] - 1) <= 840:
            # if get_value(row, config['y_wl_column'] - 1) >= 360 and get_value(row, config['y_wl_column'] - 1) <= 840:
            # if get_value(row, config['z_wl_column'] - 1) >= 360 and get_value(row, config['z_wl_column'] - 1) <= 840:

            index = index + 1
        
        wavelengths = [i for i in range(360, 830+1)]
        x_function = interp1d(list(x_raw.keys()), list(x_raw.values()), kind='cubic')
        y_function = interp1d(list(y_raw.keys()), list(y_raw.values()), kind='cubic')
        z_function = interp1d(list(z_raw.keys()), list(z_raw.values()), kind='cubic')

        x, y, z = {}, {}, {}

        for value in wavelengths:
            x[value] = x_function(value)
            y[value] = y_function(value)
            z[value] = z_function(value)
        
        return x, y, z

    # return get_interpolated_data(config['filename'], config['row_begin'], config['x_wl_column'], config['x_norm_column']), \
    #     get_interpolated_data(config['filename'], config['row_begin'], config['y_wl_column'], config['y_norm_column']), \
    #     get_interpolated_data(config['filename'], config['row_begin'], config['z_wl_column'], config['z_norm_column']),
    

def get_coordinates(data: List) -> List:
    sd = colour.SpectralDistribution(data, name='Sample')
    cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
    illuminant = colour.SDS_ILLUMINANTS['D65']
    XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
    xy =  colour.XYZ_to_xy(XYZ)
    return xy

def get_coordinates_manual(data: List) -> List:
    with open('docs/addition-curves-lookup-table.json', 'r') as table_file:
        table = json.load(table_file)
    
    x, y, z = 0, 0, 0
    for wavelength in range(360, 830+1):
        x += data[wavelength] * table['CIE_X_entries'][wavelength - 360]
        y += data[wavelength] * table['CIE_Y_entries'][wavelength - 360]
        z += data[wavelength] * table['CIE_Z_entries'][wavelength - 360]

    return [x / (x + y + z), y / (x + y + z)], x + y + z

# def get_coordinates_manual_coef(data: List) -> List:
#     with open('docs/addition-curves-lookup-table.json', 'r') as table_file:
#         table = json.load(table_file)
    
#     k = 0
#     for wavelength in range(360, 830+1):
#         k += data[wavelength] * table['CIE_Y_entries'][wavelength - 360]
#     k =/ k

#     x, z = 0, 0
#     y = 100
#     for wavelength in range(360, 830+1):
#         x += k * data[wavelength] * table['CIE_X_entries'][wavelength - 360]
#         z += k * data[wavelength] * table['CIE_Z_entries'][wavelength - 360]

#     return [x / (x + y + z), y / (x + y + z)]