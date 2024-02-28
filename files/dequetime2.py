import threading
from collections import deque
import time

# Shared deque
shared_deque = deque()


def process_link(link):
        top = get_subdirectories(link)[-1]
        blacklink_links = get_links_with_blacklink_class(link)
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_blacklink, blacklink, top) for blacklink in blacklink_links]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=top):
                results.extend(future.result())

        return results

def process_blacklink(blacklink, top):
    if "military" not in blacklink:
        mid = get_subdirectories(blacklink)[-1]
        table_links = get_links_from_table(blacklink)
        for tablelink in table_links:
            low = get_subdirectories(tablelink)[-1]
            print(f"{top} : {mid} : {low}")
            shared_deque.append(extract_page(tablelink))
    else:
        mid = get_subdirectories(blacklink)[-1]
        table_links = get_links_from_table(blacklink)
        for tablelink in table_links:
            low = get_subdirectories(tablelink)[-1]
            print(f"{top} : {mid} : {low}")
            shared_deque.append(extract_page(tablelink))


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_link, link) for link in links]

    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Overall Progress"):
        output.extend(future.result())

return output


def get_and_proc_links(origin_link):
    links = get_links_from_webpage(origin_link)
    
    for link in links:
        top = get_subdirectories(link)[-1]
        blacklink_links = get_links_with_blacklink_class(link)
        for blacklink in blacklink_links:
            if not "military" in blacklink:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    shared_deque.append(extract_page(tablelink))
            else:
                mid = get_subdirectories(blacklink)[-1]
                table_links = get_links_from_table(blacklink)
                for tablelink in table_links:
                    low = get_subdirectories(tablelink)[-1]
                    print(f"{top} : {mid} : {low}")
                    shared_deque.append(extract_page(tablelink))
    print("progress")

def process_batch():
    while True:
        if len(shared_deque) >= 20:
            batch = [shared_deque.popleft() for _ in range(20)]
            documents = [Document(text=t) for t in batch]
            nodes = parser.get_nodes_from_documents(documents)
            pipeline_mod(nodes)

# Create and start threads
get_links_thread = threading.Thread(target=get_and_proc_links, args=('https://your_origin_link.com',))
process_batch_thread = threading.Thread(target=process_batch)

get_links_thread.start()
process_batch_thread.start()

# Wait for threads to finish (you may need to manually interrupt the execution)
get_links_thread.join()
process_batch_thread.join()