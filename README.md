# CAPSTONE-T218 - Train Simulator

A comprehensive train simulation application built with PyQt6, featuring advanced algorithms for train dynamics, energy analysis, and route planning.

## Overview

This train simulator provides a user-friendly graphical interface for simulating train operations with realistic physics calculations including:
- Train kinematics and dynamics
- Energy consumption analysis
- Track curvature and gradient calculations
- Traction and resistance modeling
- Route visualization and analysis

## Features

- **Interactive GUI**: Modern PyQt6-based interface with multiple pages
- **Simulation Dashboard**: Real-time monitoring of train parameters
- **Configuration System**: Customizable train and track parameters
- **Report Generation**: Detailed analysis reports with visualizations
- **Geospatial Support**: Integration with geographical data and mapping
- **Energy Analysis**: Comprehensive energy consumption calculations
- **Track Analysis**: Automatic computation of gradients, curvatures, and distances

## Requirements

### System Requirements
- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux
- Minimum 4GB RAM recommended
- Graphics card with OpenGL support (for 3D visualizations)

### Dependencies
All required packages are listed in `requirements-dev.txt`. Key dependencies include:
- PyQt6 (GUI framework)
- NumPy & Pandas (numerical computations)
- Matplotlib (plotting and visualization)
- GeoPandas (geospatial data handling)
- Shapely (geometric operations)
- GPXpy (GPS data processing)

## Installation

### Method 1: Using pip
```bash
# Clone the repository
git clone <repository-url>
cd CAPSTONE-T218

# Install dependencies
pip install -r requirements-dev.txt

# Alternative: Install using setup.py
pip install -e .
```

### Method 2: Using Pipenv
```bash
# Install pipenv if not already installed
pip install pipenv

# Install dependencies and create virtual environment
pipenv install

# Activate the environment
pipenv shell
```

### Method 3: Using Docker
```bash
# Build the Docker image
docker build -t train-simulator .

# Run the container
docker run -it --rm train-simulator
```

## Usage

### Running the Application
```bash
# Run the main application
python mainwindow.py
```

### Basic Workflow
1. **Welcome Page**: Start by creating a new project or opening an existing one
2. **Configuration**: Set up train parameters, track data, and simulation settings
3. **Simulation**: Run the simulation with real-time monitoring
4. **Analysis**: View results and generate reports

### File Formats
- **Project Files**: `.json` or `.xml` format for saving/loading projects
- **Track Data**: Support for GPX files and custom track formats
- **Configuration**: JSON-based configuration files

## Project Structure

```
CAPSTONE-T218/
├── algorithms/                 # Core simulation algorithms
│   ├── energy/                # Energy consumption calculations
│   ├── kinematics/            # Motion and dynamics
│   ├── resistance/            # Resistance modeling
│   ├── traction_util/         # Traction calculations
│   └── simulation_results/    # Result processing
├── pages/                     # GUI pages and components
│   ├── welcome_page.py        # Application entry point
│   ├── configuration_page.py  # Parameter configuration
│   ├── simulation_dashboard.py # Real-time monitoring
│   └── report_page.py         # Results and reporting
├── modules/                   # Utility modules
├── utils/                     # Helper functions
├── configs/                   # Configuration files
├── assets/                    # Static resources
├── stylesheet/                # UI styling
├── visual_output/            # Generated visualizations
├── given_data/               # Sample data files
└── scripts/                  # Utility scripts
```

## Configuration

### Train Parameters
- Mass and dimensions
- Power and traction characteristics
- Braking parameters
- Aerodynamic properties

### Track Configuration
- Route geometry (coordinates, elevations)
- Speed limits and restrictions
- Station locations
- Signal systems

### Simulation Settings
- Time step resolution
- Output frequency
- Analysis parameters

## Example Data

The project includes example files:
- `train_example.json`: Sample train configuration
- `track_example.json`: Sample track data

## Development

### Running Tests
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests (if available)
python -m pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed correctly
2. **GUI Display Issues**: Update graphics drivers and check OpenGL support
3. **File Permission Errors**: Run with appropriate permissions for file I/O operations

### Getting Help
- Check the built-in user manual (Help → Open User Manual)
- Review example configurations
- Check log files for detailed error messages

## License

MIT License

## Authors

CAPSTONE Project Team - T218

## Version History

- v0.1: Initial release with core simulation functionality

---

For detailed documentation and examples, please refer to the user manual accessible through the application's Help menu.
