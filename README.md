
# Geo Gemmer

Geo Gemmer is a social media-based web application that allows users to discover hidden gems in their vicinity. It provides a platform for users to share and explore unique and lesser-known places, such as local attractions, restaurants, parks, and more. By leveraging geolocation data, Geo Gemmer helps users uncover hidden gems that may not be widely known or easily discoverable through traditional means. With Geo Gemmer, users can connect with like-minded individuals, discover new places, and contribute to a vibrant community of explorers.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python (at the time of writing, Python 3.8 or newer is recommended).
- You have a Windows/Linux/Mac machine capable of running Python.

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

### Running the Application

Go to the `app.py` file and either 

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

