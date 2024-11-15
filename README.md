# Hydrangea-Athena-Scraper

A tool for downloading files from Athena.

**Supported OS:** MacOS only (for now)

---

## Preparation

### Step 1: Install Chrome and ChromeDriver

1. **Ensure Google Chrome is installed:**

   - Download and install [Google Chrome](https://www.google.com/chrome/).
   - Open `chrome://version/` in Chrome to check your current version.

     **Example:** `130.0.6723.117 (Official Build) (arm64)`

2. **Install ChromeDriver:**

   - Choose one of the following methods to install the matching version of ChromeDriver.

   #### Method A: Install from Chrome for Developers

   - Visit [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver/downloads) to find the version that matches your Chrome version.

   #### Method B: Install via npm

   - Make sure [Node.js](https://nodejs.org) and [npm](https://www.npmjs.com) are installed.
   
   - Install ChromeDriver globally with:
     ```bash
     npm install -g chromedriver@[version]

**Note:** In version `1.1.0` an unstable shell script `chromedriver/installer.sh` is included, which can detect the installed version of Chrome and download the corresponding version of ChromeDriver. This script is not recommended for production use for potential bugs.

### Step 2: Install Python Dependencies

- Run the following command from the project’s root directory to install necessary Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### Step 3: Configure `config.yaml`

- Open the `config.yaml` file located in the root directory.
- Adjust the settings as needed. Refer to any inline comments for guidance.

---

## Running the Scraper

1. Run the Python script with:
   ```bash
   python main.py
   ```
2. Wait for the download process to complete.
