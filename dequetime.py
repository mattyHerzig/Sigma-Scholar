import multiprocessing
from collections import deque
import time
from concurrent.futures import ThreadPoolExecutor
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_links_from_webpage(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all the links in the main body of the webpage
        dir_list_div = soup.find('div', {'id': 'dir-list'})
        
        # Get all the links within the "dir-list" div
        links = []
        if dir_list_div:
            for anchor_tag in dir_list_div.find_all('a'):
                href = anchor_tag.get('href')
                if href:
                    full_url = urljoin(url, href)
                    links.append(full_url)
        
            return links
        else:
            print("No div with id 'dir-list' found on the webpage.")
            return []
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []


def get_links_with_blacklink_class(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all the links within <a> elements with a class containing "blacklink"
        blacklink_links = []
        for anchor_tag in soup.find_all('a', class_=lambda x: x and 'blacklink' in x):
            href = anchor_tag.get('href')
            if href:
                full_url = urljoin(url, href)
                blacklink_links.append(full_url)
        
        return blacklink_links
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

def get_links_from_table(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get all the links within the <table>
        table_links = []
        for table_row in soup.find_all('tbody'):
            for anchor_tag in table_row.find_all('a'):
                href = anchor_tag.get('href')
                if href:
                    full_url = urljoin(url, href)
                    table_links.append(full_url)
        
        return table_links
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

def get_text_from_elements(url, element_ids):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get text from elements with specified IDs
        element_texts = {}
        for element_id in element_ids:
            element = soup.find(id=element_id)
            if element:
                element_texts[element_id] = element.get_text().strip()
        
        return element_texts
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return {}
    
    
def replace_hyphens_with_space(input_string):
    parts = input_string.split('-')
    modified_parts = [part.replace('-', ' ') for part in parts]
    result = ' '.join(modified_parts)
    return result

def get_subdirectories(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the path components
    path_components = parsed_url.path.split('/')
    
    # Filter out empty path components
    subdirectories = [replace_hyphens_with_space(component) for component in path_components if component]
    
    return subdirectories

def extract_page(link):
    extract_dict = ["page-name", "header-items-award-detail-inner-wrapper", "description"]
    
    element_texts = get_text_from_elements(link, extract_dict)
    first_key = next(iter(element_texts))
    first_value = element_texts [first_key]
    subs=get_subdirectories(link)
    # Display the extracted text
    output=f"""Scholarship: {first_value}\ncategories: [{subs[-3]}, {subs[-2]}]\n website url:{link}\n Extracted from website:\n"""
    
    for element_id, text in element_texts.items():
        output+=f"{element_id}: {text.strip()}\n"
        
    return output





# ... (previous code)
def collect(deque, event, lock):
    while True:
        # Simulate collecting items
        item = f"Item-{time.time()}"
        
        with lock:
            deque.append(item)
            print(f"Collected: {item}")

            if len(deque) == 20:
                # Send batch to process
                event.set()
                event.clear()

def process(deque, event, lock):
    while True:
        event.wait()
        
        with lock:
            batch = []
            while len(deque) > 0:
                batch.append(deque.popleft())

            print(f"Processing Batch: {batch}")
            
def process_link(link, deque, event, lock):
    top = get_subdirectories(link)[-1]
    blacklink_links = get_links_with_blacklink_class(link)

    output = []

    for blacklink in blacklink_links:
        if "military" not in blacklink:
            mid = get_subdirectories(blacklink)[-1]
            table_links = get_links_from_table(blacklink)

            for tablelink in table_links:
                low = get_subdirectories(tablelink)[-1]
                print(f"{top} : {mid} : {low}")
                result = extract_page(tablelink)
                with lock:
                    deque.append(result)
                    print(f"Appended to deque: {result}")

        else:
            mid = get_subdirectories(blacklink)[-1]
            table_links = get_links_from_table(blacklink)

            for tablelink in table_links:
                low = get_subdirectories(tablelink)[-1]
                print(f"{top} : {mid} : {low}")
                result = extract_page(tablelink)
                with lock:
                    deque.append(result)
                    print(f"Appended to deque: {result}")

    # Notify the event to trigger batch processing
    with lock:
        event.set()

def get_all_links(origin_link, deque, event, lock):
    links = get_links_from_webpage(origin_link)

    with ThreadPoolExecutor() as executor:
        futures = []

        for link in links:
            future = executor.submit(process_link, link, deque, event, lock)
            futures.append(future)

        # Wait for all futures to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Shared deque, event, and lock between processes
    shared_deque = deque()
    shared_event = multiprocessing.Event()
    shared_lock = multiprocessing.Lock()

    # Start the processes
    collect_process = multiprocessing.Process(target=collect, args=(shared_deque, shared_event, shared_lock))
    process_process = multiprocessing.Process(target=process, args=(shared_deque, shared_event, shared_lock))

    # Start the additional thread to collect and process links
    link_processing_thread = threading.Thread(target=get_all_links, args=('https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory', shared_deque, shared_event, shared_lock))

    collect_process.start()
    process_process.start()
    link_processing_thread.start()

    # Wait for processes to finish (you may need to manually interrupt the execution)
    collect_process.join()
    process_process.join()
    link_processing_thread.join()
