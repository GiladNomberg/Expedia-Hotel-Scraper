import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import json,traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ---------------------------------------------------------------------------
WEBSITE_URL = "https://www.expedia.ca/"
TAB_NAME  = "Stays"
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

def goToStaysTab(drv):
    wait = WebDriverWait(drv, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "egds-tab-custom-text")))
    tabs = drv.find_elements(By.CLASS_NAME, 'egds-tab-custom-text')
    for tab in tabs:
        if TAB_NAME.lower() == tab.text.lower():
            tab.click()
            print(f"Clicked button named: {TAB_NAME}")
            break
    else:
        print(f"No tab found named {TAB_NAME}")
        
# ---------------------------------------------------------------------------

def insertDst(drv, data):
    wait = WebDriverWait(drv, 15)
    # Wait for destination box and then click it
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stid="destination_form_field-menu-trigger"]'))).click()
    # Find the destination input field
    destination_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-stid="destination_form_field-menu-input"]')))
    # Clear, type the destination city from the input file, then press Down+Enter (select first suggestion)
    destination_input.clear()
    destination_input.send_keys(data["Destination"])
    try:
        suggestions = WebDriverWait(drv, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-stid='destination_form_field-result-item']")))
    except:
        s = "No suggestions for the destination"
        raise ValueError(s)
    destination_input.send_keys(Keys.ARROW_DOWN)
    destination_input.send_keys(Keys.ENTER)
    
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
        # Click Stays tab
        goToStaysTab(driver)
        # Insert destination
        insertDst(driver, dataInput)
    finally:
        driver.quit()
        
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        print(f"{e}")
        with open("output", "w", encoding="utf-8") as f:
            json.dump(f"{e}", f, ensure_ascii=False, indent=2)