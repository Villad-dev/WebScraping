import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException


class Driver:
    def __init__(self):
        self.index = 1
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--enable-features=VaapiVideoDecode")
        chrome_options.add_argument("--ignore-gpu-blocklist")
        self.driver = webdriver.Chrome(options=chrome_options)

    def exec_task(self, column_names):
        self.driver.get("https://aviation-safety.net/database/")

        for i in range(1919, 2024):
            self.link = "https://aviation-safety.net/database/dblist.php?Year=%d" % i
            self.driver.get(self.link)
            elements = self.driver.find_elements(
                By.XPATH, f'//a[contains(text(), "{i}")]'
            )

            page_number = 1
            if len(elements) != 100:
                self.getDataFromPage(elements, column_names)
            else:
                while len(elements) == 100:
                    self.link += "&lang=&page=%d" % page_number
                    self.driver.get(self.link)
                    elements = self.driver.find_elements(
                        By.XPATH, f'//a[contains(text(), "{i}")]'
                    )
                    self.getDataFromPage(elements, column_names)
                    page_number += 1

        self.driver.quit()

    def getDataFromPage(self, elements, column_names):
        arr = [""] * 30
        for ind, el in enumerate(elements):
            arr[0] = self.index
            arr[1] = self.getObject(f"//table/tbody/tr[{ind+2}]/td[5]")
            arr[2] = self.getObject(f"//table/tbody/tr[{ind+2}]/td[6]")
            arr[3] = self.getObject(f"//table/tbody/tr[{ind+2}]/td[9]")

            #    print(self.index, "COUNT!!!", len(elements), el.accessible_name)

            try:
                el.click()
            except StaleElementReferenceException:
                print("Click not working ")

            try:
                tbody_element = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[6]/div/div/table/tbody")
            except NoSuchElementException:
                print("Element is stale")
                break

                
            tr_el = tbody_element.find_elements(By.CLASS_NAME, "caption")
            tr_count = len(tr_el)
            #print(tr_count)
            for tr in range(2, tr_count):
                if tr == 3:
                    if (self.getObject('//*[@id="contentcolumn"]/div/table/tbody/tr[3]/td[1]')!= "Time:"):
                        arr[5] = ","
                        arr[6] = self.getImageLink('//*[@id="contentcolumn"]/div/table/tbody/tr[3]/td[2]/img')  # Image
                        arr[7] = self.getObject('//*[@id="contentcolumn"]/div/table/tbody/tr[3]/td[2]')  # Type
                    else:
                        arr[5] = self.getObject('//*[@id="contentcolumn"]/div/table/tbody/tr[3]/td[2]')
                        arr[6] = self.getImageLink('//*[@id="contentcolumn"]/div/table/tbody/tr[3]/td[2]/img')
                else:
                    try:
                        arr[self.get_index(column_names,self.getObject('//*[@id="contentcolumn"]/div/table/tbody/tr[%d]/td[1]'% tr))] = self.getObject('//*[@id="contentcolumn"]/div/table/tbody/tr[%d]/td[2]' % tr)
                    except IndexError:
                        print("Index error %d" % tr, self.index)
            
            arr[27] = self.getObject('//*[@id="contentcolumn"]/div/span[2]')
            self.index += 1
            self.parseData("a", arr)
            arr = [""] * 30
            try:
                self.driver.back()
            except WebDriverException:
                self.driver.get(self.link)
                print("Failed to navigate back")

    def getObject(self, strXPath):

        try:
            o = self.driver.find_element(By.XPATH, strXPath)
            if o.text == "" or o.text is None or o.text == " ":
                res = ","
            else:
                res = o.text
        except NoSuchElementException:
            print("No such object", strXPath)
            return " ,"
        except NoSuchWindowException:
            print("No such window", strXPath)
            return " ,"
        except StaleElementReferenceException:
            print("Element is stale")
            return " ,"

        return res

    def get_index(self, column_names, column_name):
        try:
            index = column_names.index(column_name)
            return index
        except ValueError:
            print("ERROR", column_name, self.index)
            return 29

    def getImageLink(self, strXPath):
        try:
            image_link = self.driver.find_element(By.XPATH, strXPath).get_attribute(
                "src"
            )
        except NoSuchElementException:
            #print("Image does not exist")
            return ","
        except NoSuchWindowException:
            print("No such window")
            return ","
        except StaleElementReferenceException:
            print("Image is stale")
            return ","

        return image_link

    def parseData(self, option, row):
        filecsv = "data.csv"

        with open(filecsv, option, newline="\n", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def printData(self):
        filecsv = "data.csv"

        with open(filecsv, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                print(row)


column_names = ["Index:", "Fatalities:", "Location accident:", "Category:", "Date:", "Time:",
    "Image link:","Type:","Operator:","Registration:","MSN:","First flight:","Engines:",
    "Crew:","Passengers:","Total:","Aircraft damage:","Aircraft fate:","Location:",
    "Phase:","Nature:","Departure airport:","Destination airport:","Flightnumber:",
    "Collision casualties:","Total airframe hrs:","Ground casualties:","Narrative:","Unknown:",
    "Crash site elevation:"
]
tasker = Driver()
print(column_names.count)
tasker.parseData("w", column_names)
tasker.exec_task(column_names)



