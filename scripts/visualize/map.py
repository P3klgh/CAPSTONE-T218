import folium
import utm
import pandas as pd
from zipfile import ZipFile
import geopandas as gpd
import xml.etree.ElementTree as ET
from shapely.geometry import LineString

kmz_file = "Map/HBTSugarLineLucindaCurveRadii.kmz"

def print_zip_file_list(zip_path):
    files = []
    try:
        # Open the zip file
        with ZipFile(zip_path) as zip_ref:
            # Iterate through the contents of the zip file
            for item in zip_ref.namelist():
                # Print the filename
                files.append(item)
        for files
    except FileNotFoundError:
        print(f"Error: The file {zip_path} was not found.")
    except ZipFile.BadZipFile:
        print(f"Error: {zip_path} is not a valid zip file.")

    # Example usage
    zip_file_path = "Map/HBTSugarLineLucindaCurveRadii.kmz"
    zip_file_list = print_zip_file_list(zip_file_path)
    for i in zip_file_list:
        print(i)

    # Read the xls file
    df = pd.read_excel("Map/HBTSugarLineLucindaGrade.xls")
    #print(df.head(5))

    xStart = df['XStart'].tolist()
    xFinish = df['XFinish'].tolist()
    yStart = df['YStart'].tolist()
    yFinish = df['YFinish'].tolist()
    avgSlope = df['Avg_Slope'].tolist()

    max_rows = len(df)
    mapCenterCoord = utm.to_latlon(xStart[0], yStart[0], 55, 'K')

    m = folium.Map(location=mapCenterCoord, tiles="OpenStreetMap", zoom_start=10)

    for i in range(0, max_rows):
        row = df.iloc[i]
        testCoord1 = utm.to_latlon(xStart[i], yStart[i], 55, 'K')
        testCoord2 = utm.to_latlon(xFinish[i], yFinish[i], 55, 'K')

        line_coordinates = [
            testCoord1,
            testCoord2]
    
    folium.PolyLine(
        locations=line_coordinates,
        color='red',
        weight=5,
        opacity=0.7,
        tooltip=f"""
        <h3>Coordinate {row['FID']}</h3>
        <p>X Start: {row['XStart']}</p>
        <p>Y Start: {row['YStart']}</p>
        <p>X Finish: {row['XFinish']}</p>
        <p>Y Finish: {row['YFinish']}</p>
        <p>Average Slope: {avgSlope[i]:.2f}%</p>
        """
    ).add_to(m)

    m.fit_bounds(m.get_bounds(), padding=(50, 50))

    m.save("GUI/trackMap_interactive.html")
