
# Geo Gemmer

Geo Gemmer is a social media-based web application that allows users to discover hidden gems in their vicinity. It provides a platform for users to share and explore unique and lesser-known places, such as local attractions, restaurants, parks, and more. By leveraging geolocation data, Geo Gemmer helps users uncover hidden gems that may not be widely known or easily discoverable through traditional means. With Geo Gemmer, users can connect with like-minded individuals, discover new places, and contribute to a vibrant community of explorers.


### Table of Contents
Introduction
  [Getting Started](#getting-started)
  [Prerequisites](#prerequisites)

Setup
  [Setting Up the PostGIS Extension](#setting-up-the-postgis-extension)
  [Setting Up a Development Environment](#setting-up-a-development-environment)

Usage
  [Running the Application](#running-the-application)
  [Exiting the Virtual Environment](#exiting-the-virtual-environment)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python (at the time of writing, Python 3.8 or newer is recommended).
- You have a Windows/Linux/Mac machine capable of running Python.
- Make sure PostgreSQL is installed on your system, as psycopg2 requires PostgreSQL client libraries to run. 


### Setting Up the PostGIS Extension
   The database uses the PostGIS extension for PostgreSQL. If you don't have it already, here is how you install it.

1. **Open Application Stack Builder**
   To install the PostGIS extension for PostgreSQL, first open the Application Stack Builder that installs with PostgreSQL
   ![shortcut found in my computer under C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PostgreSQL 16](https://github.com/ZanderCow/geo-gemmer/blob/main/readme_instruction_images/stack_builder1.png)

2. **Select Your PostgreSQL server**
   Make sure to select your PostgreSQL server, and click "Next >"
   ![shortcut found in my computer under C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PostgreSQL 16](https://github.com/ZanderCow/geo-gemmer/blob/main/readme_instruction_images/stack_builder2.png)

3. **Install PostGIS**
   Under Categories -> Spatial Extensions, you will find the option for the PostGIS extension. Click that and click "Next ->" and continue to finish the installation
   ![shortcut found in my computer under C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PostgreSQL 16](https://github.com/ZanderCow/geo-gemmer/blob/main/readme_instruction_images/stack_builder3.png)

### Setting Up a Development Environment

1. **Clone the Repository**

   First, clone the project repository to your local machine. Open a terminal and run:

   ```bash
   git clone https://github.com/ZanderCow/Geo-Gemmer.git
   ```


2. **Create a Virtual Environment**

   It's recommended to create a virtual environment to isolate project dependencies. Run the following command in the root of your project directory:

   Windows
   
   ```bash
   python -m venv venv
   ```
   Mac
   ```bash
   python3 -m venv venv
    ```
   This will create a virtual environment named `venv`.

3. **Activate the Virtual Environment**

   - On Windows, activate the virtual environment by running:

     ```bash
     .\venv\Scripts\activate
     ```

   - On Unix or MacOS, use:

     ```bash
     source venv/bin/activate
     ```

   You should now see the name of your virtual environment (`venv`) in the command prompt, indicating that it is active.

4. **Install Dependencies**

   With the virtual environment activated, install the project dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

   This command reads the `requirements.txt` file in your project directory and installs all the required Python packages.

5. **Make `.env` file**

   At the same directory level as the `app.py` file, make a file called `.env` and put the following in the file:

   ```bash
   DATABASE_URL=postgresql://Username:Password@localhost:5432
   ```
   Change the following to however your postgres is setup:
    - `Username`: whatever your username is 
    - `Password`: whatever your password is
    - `@localhost` : hostname or IP address where the database server is running
    - `5432` whatever port the database is running on

### Running the Application

Go to the main folder with the `app.py` file and either 

Run in the terminal with
```
flask run
```
Or click the play button thing in the top right corner


### Exiting the Virtual Environment

When you're done working in the virtual environment, you can deactivate it by running:

```bash
deactivate
```

