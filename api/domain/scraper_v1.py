import re
import json
import logging
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# Set up logging
def writing_logfile(log_message, log_file='scraper.log'):
    logging.basicConfig(filename=log_file,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    logging.info(log_message)

#Handle responses
def handle_response(response):
    if not response.ok:
        writing_logfile(f"FAILED RESPONSE FROM {response.url}, STATUS CODE {response.status}")


def get_feed_urls(BASE_URL):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(BASE_URL)
        except:
            print('\n*** Exception occured while loading the website, wrote to logfile. ***\n')
            # Log and continue all network requests
            page.on("response", handle_response)

        #Initialize the list to store the different feeds, if we find several xml files
        rss_feeds_list = []

        # #Checking if the website is powered by Wordpress
        # #If it is, the RSS feed can be easily accessed by website_url/feed/
        # #For this we look for a regex match in the HTML of the current page
        # if re.search(r'.*wordpress.*|.*WordPress.*|.*Wordpress.*|.*wp-content.*', page.content()):
        #     expected_feed_url = BASE_URL + '/feed/'
        #     try:
        #         page.goto(expected_feed_url)
        #     except:
        #         print('\n*** Exception occured while trying to access the feed page, wrote to logfile. ***\n')
        #         # Log and continue all network requests
        #         page.on("response", handle_response)
        #     #Checks if we are indeed on the feed page
        #     if re.search(r'^<rss|^&lt;rss|^<?xml', page.content()):
        #         rss_feeds_list.append(expected_feed_url)
        #     #If not we go back to homepage
        #     else:
        #         page.goto(BASE_URL)


        #Retrieving all the links from the homepage
        homepage_links = page.query_selector_all("a")

        #Itering through all the links founds in homepage
        for link in homepage_links:

            url = link.get_attribute("href")
            #Only looking at links that have a href attribute
            if url:
                #Checking if the url matches one of an RSS feed
                if re.search(r'.*\/feed\/.*|.*-rss-.*|.*.xml', url):
                    #Completing partial url
                    if url[0] == '/':
                        url = BASE_URL + url

                    try:
                        page.goto(url)
                    except:
                        print('\n*** Exception occured, wrote to logfile. ***\n')
                        # Log and continue all network requests
                        page.on("response", handle_response)
                        continue
                    
                    #Retrieving all the links from the current page
                    feedpage_links = page.query_selector_all("a")
                    
                    #Filtering empty links
                    if feedpage_links:
                        
                        #Getting href attributes i.e the urls
                        for link in feedpage_links:
                            link_url = link.get_attribute('href')

                            #Filtering empty urls
                            if link_url:

                                #Checking if several xml files / rss feeds exists on the page
                                if re.search(r'.*.xml', link_url):
                                    
                                    rss_feeds_list.append(link_url)
                            else:
                                break
                        break

                    else:
                        if re.search(r'.*<rss.*|.*&lt;rss.*', page.content()):
                            rss_feeds_list.append(url)
                            # print(rss_feeds_list)
                        else:
                            print('No RSS feed found.')
                        break
                else:
                    continue
            else:
                print('***** Skipping, not a valid url *****')

        #Initializing a list to store articles urls
        articles_urls = []

        for feed_url in rss_feeds_list:
            print(f"\nVisiting {feed_url} ...")

            try:
                page.goto(feed_url)
            except:
                print('\n*** Exception occured, wrote to logfile. ***\n')
                # Log and continue all network requests
                page.on("response", handle_response)
                continue
                
            feed_content = page.content()
            feed_content = feed_content.replace('&lt;', '<').replace('&gt;', '>')
            soup = BeautifulSoup(feed_content, 'xml')
            current_page_links = []

            for link in soup.find_all('link'):
                clean_link = link.get_text()
                if clean_link != '':
                    current_page_links.append(clean_link)
                
            articles_urls.extend(current_page_links)

            #Removing duplicates
            articles_urls= dict.fromkeys(articles_urls).keys()

        browser.close()

        return articles_urls, rss_feeds_list

def visit_feed_urls(URL_LIST, FEEDS):

    print(f'\nVisiting urls found in {FEEDS}\n')

    #Initializing dict to store for each url the corresponding HTML source code
    result_dict = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in URL_LIST:
            #Checking validity of the url
            if re.match(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', url):
                    # print(url)
                try:
                    page.goto(url)
                except:
                    print('\n*** Exception occured, wrote to logfile. ***\n')
                    # Log and continue all network requests
                    page.on("response", handle_response)
                    continue

                html_content = page.content()
                result_dict[url] = html_content
                print(f'Retrieved HTML content from {url}')
            else:
                print('***** Skipping, not a valid url *****')
                continue
        
    return result_dict

#Defining main()
def main():
    """
    Main function, calls get_feed_urls() and visit_feed_urls()
    
    """
    TARGET_URL_LIST = input("Path to the .txt file of websites to scrap: ")

    while not re.match(r'.*.txt', TARGET_URL_LIST):
        TARGET_URL_LIST = input("Please enter a valid path to the .txt file: ")

    OUTPUT_FILE = input("Output file (leave blank to use default results.json): ")
    if not OUTPUT_FILE:
        OUTPUT_FILE = "results.json"

    print("Scanning file ...")

    websites_urls = open(TARGET_URL_LIST, "r")
    target_websites = websites_urls.read().splitlines()
    print(f'The script will visit each of these websites {target_websites} and retrieve links inside the RSS feed + HTML content')

    for website_url in target_websites:

        #Calling functions
        urls_list, feed_list = get_feed_urls(website_url)
        urls_dict = visit_feed_urls(urls_list, feed_list)

        # Writing to file
        OUTPUT_FILE = 'results.json'

        #file_data = json.load("[" + file.read().replace("}\n{", "},\n{") + "]")

        with open(OUTPUT_FILE, 'a') as file:
            file.seek(0)
            json.dump(urls_dict, file, indent = 4)
            file.write(',\n')
        print(f"\nWrote results to file {file.name}")

     
#Calling main()        
if __name__ == "__main__":
    main()

