from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=chrome_options)

def extract_sponsored_data(driver, search_query):
    driver.get("https://www.google.com")
    
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        sponsored_results = []
        time.sleep(3)
        
        for page in range(2):
            try:
                sponsored_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uEierd"))
                )
                
                for element in sponsored_elements:
                    try:
                        data = {
                            "search_query": search_query,
                            "title": element.find_element(By.CSS_SELECTOR, "div[role='heading']").text.strip(),
                            "website": element.find_element(By.CSS_SELECTOR, "span.x2VHCd").text.strip(),
                            "description": element.find_element(By.CSS_SELECTOR, "div.Va3FIb.r025kc span:last-child").text.strip()
                        }
                        sponsored_results.append(data)
                    except Exception as e:
                        print(f"Error extracting element data: {str(e)}")
                        continue
                
                # if page < 1:
                #     next_button = driver.find_element(By.ID, "pnnext")
                #     next_button.click()
                #     time.sleep(3)
                    
            except Exception as e:
                print(f"Error on page {page + 1}: {str(e)}")
                break
                
        return sponsored_results
        
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return []

def save_to_csv(results, filename="Data/sponsored_results.csv"):
    fieldnames = ["search_query", "title", "website", "description"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result_list in results.values():
            for result in result_list:
                writer.writerow(result)

def main():
    search_queries = [
        "escape room in london",
        "horror escape room london",
        "haunted escape room london"
    ]
    
    driver = setup_driver()
    all_results = {}
    
    try:
        for query in search_queries:
            print(f"Searching for: {query}")
            results = extract_sponsored_data(driver, query)
            all_results[query] = results
            time.sleep(3)
            
        save_to_csv(all_results)
        print("Results saved to sponsored_results.csv")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()