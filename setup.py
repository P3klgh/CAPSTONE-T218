from setuptools import setup, find_packages

setup(
    name="capstone-t218",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'geopandas',
        'shapely',
        'pyproj',
        'gpxpy',
        'PyQt6',
        'PyQt6-WebEngine',
        'qtawesome',
    ],
) 