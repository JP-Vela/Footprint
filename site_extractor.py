from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import os
import time
import json
from name_bio_extractor import extract

folder_path = f"{os.getcwd()}\\username_checks"
username_files = os.listdir(folder_path)




def remove_unwanted_tags(html_content):
    # Remove script tags and everything inside them
    cleaned_html = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)
    
    # Remove style tags and everything inside them
    cleaned_html = re.sub(r'<style.*?>.*?</style>', '', cleaned_html, flags=re.DOTALL)
    
    # Remove meta tags
    cleaned_html = re.sub(r'<meta.*?>', '', cleaned_html, flags=re.DOTALL)
    
    # Remove link tags
    cleaned_html = re.sub(r'<link.*?>', '', cleaned_html, flags=re.DOTALL)
    
    # Remove everything that isn't inside a tag
    #cleaned_html = re.sub(r'>[^<]+<', '><', cleaned_html)
    
    cleaned_html = cleaned_html.replace("\n", " ")

    return cleaned_html




options = Options()
options.add_argument("browser.ssl_override_behavior=2")
options.add_argument("browser.xul.error_pages.expert_bad_cert=True")
options.add_argument("browser.xul.error_pages.expert_bad_cert_warning=False")
  
driver = webdriver.Firefox(options = options)



babybacon = folder_path+"\\"+username_files[0]

output_dict = dict()

with open(babybacon, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()[:-1]

    for url in lines:
        if not url.startswith("http"):
            print("skipping URL")
            break

        print(f"Checking {url}")
        driver.get(url)

        try:
            time.sleep(2)
            """element = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.ID, "myDynamicElement"))
            )"""
        except:
            pass
        finally:
            html_context = remove_unwanted_tags(driver.page_source)
            total = extract(html_context)
            output_dict[url] = total
  


    output_file = open("cross_output\\output.json", "w", encoding="utf-8")
    output_file.write(json.dumps(output_dict, indent=4))
    output_file.close()
    driver.close()
    driver.quit()
