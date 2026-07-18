import requests

# ---------------------------------------------------------
# GOAL OF THIS SCRIPT:
# Some APIs give you data in "pages" instead of all at once.
# This script asks for page 1, page 2, page 3... and keeps
# asking for the next page until the API says "no more data."
# It collects everything into one big list as it goes.
# ---------------------------------------------------------

base_url = "https://jsonplaceholder.typicode.com/posts"

current_page_number = 1
all_results_collected = []
keep_going = True

while keep_going == True:

    print("Requesting page number:", current_page_number)

    request_parameters = {
        "_page": current_page_number,
        "_limit": 10
    }

    response = requests.get(base_url, params=request_parameters)

    print("Status code received:", response.status_code)

    page_data = response.json()

    number_of_items_on_this_page = len(page_data)

    print("Number of items on this page:", number_of_items_on_this_page)

    if number_of_items_on_this_page == 0:
        print("No more items found. Stopping the loop.")
        keep_going = False
    else:
        all_results_collected = all_results_collected + page_data
        current_page_number = current_page_number + 1

    if current_page_number > 5:
        print("Safety limit reached. Stopping the loop.")
        keep_going = False

print("")
print("Finished collecting data.")
print("Total items collected across all pages:", len(all_results_collected))
