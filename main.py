from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from utils.driver_setup import setup_driver

def extract_sponsored_data(driver, search_query):
    driver.get("https://www.google.com")
    
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    
    sponsored_results = []
    
    # Wait for sponsored results
    time.sleep(3)
    
    for page in range(2):  # First 2 pages
        try:
            sponsored_elements = driver.find_elements(By.CSS_SELECTOR, "div.uEierd")
            
            for element in sponsored_elements:
                try:
                    data = {
                        "company_name": element.find_element(By.CSS_SELECTOR, "div.CCgQ5").text.strip(),
                        "website": element.find_element(By.CSS_SELECTOR, "span.yKd8Hd").text.strip(),
                        "title": element.find_element(By.CSS_SELECTOR, "div.v7jaNc").text.strip(),
                        "description": element.find_element(By.CSS_SELECTOR, "div.ySSKvd div.p4wth").text.strip()
                    }
                    sponsored_results.append(data)
                except:
                    continue
            
            # Go to next page if exists
            # if page < 1:
            #     next_button = driver.find_element(By.ID, "pnnext")
            #     next_button.click()
            #     time.sleep(2)
                
        except Exception as e:
            print(f"Error on page {page + 1}: {str(e)}")
    
    return sponsored_results

def save_results(results, filename="sponsored_results.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    search_queries = [
        "escape room in london",
        "horror escape room london",
        "haunted escape room london"
    ]
    
    driver = setup_driver(headless=False)
    all_results = {}
    
    try:
        for query in search_queries:
            print(f"Searching for: {query}")
            results = extract_sponsored_data(driver, query)
            all_results[query] = results
            time.sleep(3)
            
        save_results(all_results)
        print("Results saved to sponsored_results.json")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()