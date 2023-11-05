# Octopart Web Scraping Automation

This Python script automates the process of web scraping on the Octopart website to gather information about electronic components based on their part numbers. It uses Selenium, a powerful web automation tool, to perform the following tasks:

1. **Search and Scrape Data**:
   - The script reads part numbers from an input CSV file (`old_data.csv`) and searches for each part number on the Octopart website.
   - It extracts information such as scraped part number, alternate part numbers, median price, and other relevant details.

2. **Captcha Handling**:
   - The script handles captchas using an automated method (`presshold()`) to simulate human interaction and bypass captchas.

3. **Data Storage**:
   - The scraped data is stored in a Pandas DataFrame.
   - The script appends the scraped data to the DataFrame and exports it to an Excel file (`new_data.xlsx`).

## Prerequisites

Before running the script, ensure you have the following:

- Python installed on your system.
- Chrome WebDriver downloaded and placed in your system's PATH.
- Selenium library installed (`pip install selenium`).
- pandas library installed (`pip install pandas`).

## How to Use

1. **Prepare Input Data**:
   - Create an input CSV file (`old_data.csv`) containing part numbers and manufacturer details in the following format:
     ```csv
     part_number,manufacturer
     12345,ABC Electronics
     67890,XYZ Inc.
     ...
     ```

2. **Set Chrome Options**:
   - Customize the Chrome options in the script according to your requirements (such as proxy settings, user agent, etc.).

3. **Run the Script**:
   - Execute the Python script (`python script_name.py`).
   - The script will automate the process of searching for part numbers on Octopart, bypass captchas, and store the scraped data in `new_data.xlsx`.

**Note**: Ensure you comply with Octopart's terms of service and use this script responsibly and ethically. Automated interactions should be performed responsibly and within the bounds of legality and website terms of service.
