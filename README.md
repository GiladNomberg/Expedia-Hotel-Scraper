# Expedia-Hotel-Scraper
A Python script that searches for hotels on Expedia based on destination and date range, applies filters and saves the top results to a file.
Required settings:
1. Python 3.9+ installed
2. Google Chrome installed
How to use?
1. Clone/download the project
2. Install required Python packages (pip install -r requirements.txt)
3. Optional - edit input file
4. Run the script (python main.py)
Assumptions:
1. Default travelers (2 adults, one room)
2. Search the first suggested option (not the exact match)
3. If there are no exact matches due to the filters, display the first 3 hotels on the page (assume 'no exact matches' is not an actual hotel name)
