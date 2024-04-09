# GAIA
G.A.I.A - Gastronomy Automation Industrial Assembly

This project demonstrates how to use a robotic arm controlled via the RoboDK library to assemble meals automatically. The robot arm moves between stations to prepare various meal components based on user preferences.

## Prerequisites
- [RoboDK](https://robodk.com/download) software installed on your machine.
- APIJaka driver installed and configured in RoboDK.
Important: The JAKA driver requires Visual C++ Redistributable Packages for Visual Studio 2013 installed on the computer. You can download and install it from Microsoft.


## Getting Started
1. Clone or download this repository to your local machine.
2. Install RoboDK and configure the APIJaka driver according to the RoboDK documentation.
3. Open RoboDK and load the provided RoboDK (.rdk) file or HTML file in RoboDK for browser.
4. Run the Python script `main.py` to execute the meal assembly process.

## Usage
1. Customize the meal preferences by editing the `user_preferences.json` file.
2. Run the `main.py` script to start the meal assembly process.
3. Follow the prompts to select the desired meal and portion size.

## Files Included
- `main.py`: Python script to control the meal assembly process.
- `system_setup.json`: Configuration file containing the robot name and item targets.
- `user_preferences.json`: Configuration file containing user meal preferences.
- `meal_assembly.rdk` (or `meal_assembly.html`): RoboDK file containing the robot arm setup and station positions.

## Notes
- Ensure that the APIJaka driver is properly configured in RoboDK for seamless communication with the robot arm.
- For advanced customization or debugging, refer to the RoboDK documentation and API reference.

