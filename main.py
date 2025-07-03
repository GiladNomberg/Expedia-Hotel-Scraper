import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import json,traceback

# ---------------------------------------------------------------------------
WEBSITE_URL = "https://www.expedia.ca/"
# ---------------------------------------------------------------------------

def readFileAndCheckValidity(dataInput):
    # Print the file
    print(dataInput)
    print("Destination: ", dataInput["Destination"])
    print("Start date: ", dataInput["Date range start"])
    print("End date: ", dataInput["Date range end"])
    
    startDate = datetime.strptime(dataInput["Date range start"], "%B %d %Y")
    endDate = datetime.strptime(dataInput["Date range end"], "%B %d %Y")

    if endDate > startDate:
        deltaDays = (endDate - startDate).days
        if deltaDays <= 90:
            print("Date range is valid")
        else:
            s = "range must be 90 days or fewer"
            raise ValueError(s)
    else:
        s = "End date must be after start date"
        raise ValueError(s)

# ---------------------------------------------------------------------------

def main():
    dataInput = []
    # Open the input file
    with open("input", "r", encoding="utf-8") as f:
        dataInput = json.load(f)
    readFileAndCheckValidity(dataInput)
    # Interface to control the browser
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 40)
    try:
        # Open url
        driver.get(WEBSITE_URL)
    finally:
        driver.quit()
        
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        print(f"{e}")
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(f"{e}", f, ensure_ascii=False, indent=2)