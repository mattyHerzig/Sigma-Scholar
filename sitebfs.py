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



def send_pages_to_deque(origin_link):
    links = get_links_from_webpage(origin_link)
    for link in links:
        top=get_subdirectories(link)[-1]
        blacklink_links = get_links_with_blacklink_class(link)
        for blacklink in blacklink_links:
            if not "military" in blacklink:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    deque.append(extract_page(tablelink))
            else:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    deque.append(extract_page(tablelink))



deque=[]
def get_and_proc_links(origin_link):
    links = get_links_from_webpage(origin_link)
    
    for link in links:
        top=get_subdirectories(link)[-1]
        blacklink_links = get_links_with_blacklink_class(link)
        for blacklink in blacklink_links:
            if not "military" in blacklink:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    deque.append(extract_page(tablelink))
            else:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
            
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    deque.append(extract_page(tablelink))
    print("progress")

#returns data to be processed
def extract_page(link):
    extract_dict = ["page-name", "header-items-award-detail-inner-wrapper", "description"]
    
    element_texts = get_text_from_elements(link, extract_dict)
    first_key = next(iter(element_texts))
    first_value = element_texts [first_key]
    subs=get_subdirectories(link)
    # Display the extracted text
    data=f"""Scholarship: {first_value}\ncategories: [{subs[-3]}, {subs[-2]}]\n website url:{link}\n Extracted from website:\n"""
    
    for element_id, text in element_texts.items():
        data+=f"{element_id}: {text.strip()}\n"
        
    return data

def get_all_sublinks(link):
    all_links=[]
    top_links = get_links_from_webpage(link)
    
    
    print("Links layer 1:")
    for link in top_links:
        print(link)
        blacklink_links = get_links_with_blacklink_class(link)
        
        # Display links with class "blacklink" on the subsequent page
        print(f"Links layer 2 on {link}:")
        for blacklink in blacklink_links:
            print(blacklink)
            table_links=get_links_from_table(blacklink)
            
            print(f"Links layer 3 {link}:")
            for tablelink in table_links:
                all_links.append(tablelink)
                print(tablelink)
    return all_links

def get_all_docs(links):
    outputs=[]
    for src in links:
        outputs.append(extract_page(src))
    print(len(outputs))
    return outputs
    

def get_all_links(origin_link):
    links = get_links_from_webpage(origin_link)
    output=[]
    for link in links:
        top=get_subdirectories(link)[-1]
        blacklink_links = get_links_with_blacklink_class(link)
        for blacklink in blacklink_links:
            if not "military" in blacklink:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    output.append(extract_page(tablelink))
            else:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
            
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    output.append(extract_page(tablelink))
    return output
results = get_all_links('https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory')



