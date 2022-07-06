#pip install --trusted-host pypi.org selenium
#pip install --trusted-host pypi.org beautifulsoup
#pip install --trusted-host pypi.org webdriver-manager

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://cpangprodweb.highjumpcloud.com/core/Default.html#"
driver.get(url)
driver.implicitly_wait(30)

start_time = time.time()

login = "WCHAFFIN"
password = "QWE123"

login_path = [
"/html/body/hj-logon/div/div/div[2]/hj-field-table/div/hj-field-table-row[2]/div/hj-field-cell/div/hj-field-control/div/div/span[1]/hj-textbox/input",
"/html/body/hj-logon/div/div/div[2]/hj-field-table/div/hj-field-table-row[3]/div/hj-field-cell/div/hj-field-control/div/div/span[1]/hj-password-textbox/input",
"/html/body/hj-logon/div/div/div[3]/hj-button/button"
]

shortandcancel_path = [
"/html/body/div[1]/div[1]/nav[1]/ul/li[1]/a",
"/html/body/div[1]/div[1]/nav[2]/ul/li[2]/a/span",
"/html/body/div[1]/div[1]/nav[2]/ul/li[2]/ul/li[11]/a/span",
"/html/body/div[1]/div[1]/nav[2]/ul/li[2]/ul/li[11]/ul/li[4]/a",
"/html/body/div[1]/div[1]/nav[2]/ul/li[2]/ul/li[11]/ul/li[4]/ul/li[15]/a/span",
"/html/body/header/div[2]/div[2]/ul/li[1]/a" ]

table_path = 'div.k-grid-content.k-auto-scrollable > table > tbody'
full_table_path = 'body > div.page-wrap > div.content-wrap > div > hj-flex-container > div > hj-flex-grow > div > hj-flex-scroll > div > div:nth-child(2) > div:nth-child(3) > div.hj-spaces-page-template-wrap > hj-flex-container > div > hj-flex-grow > div > div > hj-grid > div.hj-grid-container.hj-grid-full-height-container > div > div.k-grid-content.k-auto-scrollable > table'
header_table_path = 'div.k-grid-header > div > table'
full_header_table_path = 'body > div.page-wrap > div.content-wrap > div > hj-flex-container > div > hj-flex-grow > div > hj-flex-scroll > div > div:nth-child(4) > div:nth-child(2) > div.hj-spaces-page-template-wrap > hj-flex-container > div > hj-flex-grow > div > div > hj-grid > div.hj-grid-container.hj-grid-full-height-container > div > div.k-grid-header > div > table'
back_button_path = "body > div.page-wrap > div.content-wrap > div > hj-flex-container > div > hj-flex-shrink > div > div > div.paging > a:nth-child(1) > span > i.fa.fa-angle-left.fa-stack-1x"
save_button_path = "body > header > div.app-bar > div:nth-child(2) > ul > li:nth-child(1) > a"
export_button_path = "body > header > div.app-bar > div.action-group.supply-chain-advantage > ul > li:nth-child(1) > a > span"

for xpath in login_path:
	xpath = xpath
	element = driver.find_element(by=By.XPATH, value=xpath)
 
	if xpath == login_path[0]:
		element.send_keys(login)
	elif xpath == login_path[1]:
		element.send_keys(password)
	elif xpath == login_path[2]:
		element.click()
print("...done logging in!")


for xpath in shortandcancel_path:
	xpath = xpath
	element = driver.find_element(by=By.XPATH, value=xpath)

	if xpath == shortandcancel_path[5]:
		time.sleep(1)
		element = driver.find_element(by=By.XPATH, value=xpath)
		element.click()
	else:
		time.sleep(.1)
		element.click()
print("...done going to S&C page!")


#iterate header to generate index instead of using x,y
col_x = 0
row_y = 0
cancelled_filtered = False
timeout = 90

lines_cancelled = 0
items_cancelled = 0 

driver.find_element(by=By.CSS_SELECTOR, value='body').click() #don't remember why I did this, also don't think it's necessary but it shall remain 
print("...body clicked!") 

try:
	element_present = EC.presence_of_element_located((By.CSS_SELECTOR, table_path))
	print("...waiting for page to load")
	WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

shortandcancel_table = driver.find_element(by=By.CSS_SELECTOR, value=table_path)
print("...short and cancel table found!")

for row in shortandcancel_table.find_elements(by=By.CSS_SELECTOR, value='tr'):
	col_x = 0

	
	for cell in row.find_elements(by=By.TAG_NAME, value='td'):
		print(cell.text, end = ' ')

		if col_x == 2 and cell.text != "0":
			short_orders_link = cell.find_element(by=By.CSS_SELECTOR, value="a")

			short_orders_link.click()
			time.sleep(30)
			page_sorted = False

			# try:
			#     element_present = EC.presence_of_element_located((By.CSS_SELECTOR, full_header_table_path))
			#     print("...waiting for page to load")
			#     WebDriverWait(driver, timeout).until(element_present)
			# except TimeoutException:
			#     print("Timed out waiting for page to load")


			if(not page_sorted):
				header_table = driver.find_elements(by=By.CSS_SELECTOR, value=header_table_path)[1]
				print("...Header table found!")

				time.sleep(1)

				for row in header_table.find_elements(by=By.CSS_SELECTOR, value='tr'): #this sort is necessary to relieve the bug where HJ only shows part of the table
					for cell in row.find_elements(by=By.TAG_NAME, value='th'):
						if cell.get_attribute("data-title") == "Order Status":
							sort_button = cell.find_element(by=By.CSS_SELECTOR, value='a.k-link')
							try:
								sort_button.click()
								page_sorted = True
								print("...Page sorted!")
							except:
								print("!!!...sort button click failed!")
							finally:
								pass

							time.sleep(10)

			if(not cancelled_filtered):
				header_table = driver.find_elements(by=By.CSS_SELECTOR, value=header_table_path)[1]
				print("...Header table found!")

				time.sleep(1)

				for row in header_table.find_elements(by=By.CSS_SELECTOR, value='tr'):
					for cell in row.find_elements(by=By.TAG_NAME, value='th'):
						#print(cell.get_attribute("data-title"))
						if cell.get_attribute("data-title") == "Order Status":

							filter_button = cell.find_element(by=By.CSS_SELECTOR, value='a')
							filter_button.click()

							order_status_list = driver.find_element(by=By.CSS_SELECTOR, value='body > div.k-animation-container > div')
							for row in order_status_list.find_elements(by=By.CSS_SELECTOR, value='li'):
								if row.text == 'Filter':
									filter_button = row.find_element(by=By.CSS_SELECTOR, value='span')
									filter_button.click()
									
									time.sleep(1)
									filter_input = driver.find_element(by=By.CSS_SELECTOR, value='li.k-item.k-filter-item.k-state-default.k-last.k-state-border-right > div > ul')
									filter_input = filter_input.find_element(by=By.CSS_SELECTOR, value='input')
									filter_input.send_keys("cancelled")

									submit_button = driver.find_element(by=By.CSS_SELECTOR, value='div.k-action-buttons > button.k-button.k-primary')
									submit_button.click()

									print("...Orders filtered to \'cancelled!\'")

									#at this point we're inside the oldest day, and filtered - need to check list again
			if(not cancelled_filtered):
				#time.sleep(10)

				try:
					print("...waiting for page to load")
					element_clickable = EC.element_to_be_clickable((By.CSS_SELECTOR, export_button_path)) #hanging here atm
					WebDriverWait(driver, timeout).until(element_clickable)
				except TimeoutException:
					print("Timed out waiting for page to load")

			cancelled_filtered = True
			
			#need to click to sort to get full tables

			#short logic goes here

			shortandcancel_orders_table = driver.find_elements(by=By.CSS_SELECTOR, value=table_path)[1]
			row_index = 0
			for row in shortandcancel_orders_table.find_elements(by=By.CSS_SELECTOR, value='tr'):
				col_index = 0 

				for cell in row.find_elements(by=By.TAG_NAME, value='td'):
					if col_index == 1 and row.find_elements(by=By.TAG_NAME, value='td')[3].text == "Cancelled":
						time.sleep(1)
						cell.click()
						time.sleep(1)


						order_table = driver.find_elements(by=By.CSS_SELECTOR, value=table_path)[2]
						for i in range(len(order_table.find_elements(by=By.CSS_SELECTOR, value='tr'))): #iterating like this is a necessity, as we are changing the DOM
							order_table = driver.find_elements(by=By.CSS_SELECTOR, value=table_path)[2] 
							row = order_table.find_elements(by=By.CSS_SELECTOR, value='tr')
							cols = row[i].find_elements(by=By.TAG_NAME, value='td')

							order_number = cols[2].text
							item_number = cols[3].text
							order_qty = cols[6].text
							picked_qty = cols[7].text
							alloc_qty = cols[8].text
							short_qty = cols[9].text
							cancel_qty = cols[10].text

							cancel_request = cols[12]			

							print(order_number + " " + item_number + " Order QTY = " + order_qty + " Picked QTY = " + picked_qty + " Alloc QTY = " + alloc_qty + " Short QTY = " + short_qty + " Cancel QTY = " + cancel_qty)
							
							if(picked_qty == "0" and short_qty != order_qty and cancel_qty == "0"):
								print("...short found!")

							
								#cancel_request.click()
								
								action = ActionChains(driver)
								action.double_click(cancel_request).perform()

								cancel_input = cancel_request.find_element(by=By.CSS_SELECTOR, value='hj-textbox > input')
								cancel_input.send_keys( str(int(order_qty) - int(short_qty)) )

								save_button = driver.find_element(by=By.CSS_SELECTOR, value = save_button_path)

								save_button.click()
								print("...Line shorted!")
								lines_cancelled += 1
								items_cancelled += int(order_qty) - int(short_qty)

								print("Total lines cancelled: ", lines_cancelled)
								print("Total items cancelled: ", items_cancelled)

								time.sleep(1.5)

						time.sleep(2)
						back_button = driver.find_element(by=By.CSS_SELECTOR, value=back_button_path)
						back_button.click()

					print(cell.text, end = ' ')
					col_index += 1

				row_index += 1

				print('\n')

			#short logic goes here

			time.sleep(1)
			back_button = driver.find_element(by=By.CSS_SELECTOR, value=back_button_path)
			back_button.click()
			print("...Going back a page!")
			time.sleep(1)

		col_x += 1

	else:
		print('\n')

	row_y += 1

print("Total lines cancelled: ", lines_cancelled)
print("Total items cancelled: ", items_cancelled)

end_time = time.time()

elapsed_time = round((end_time - start_time)/60.0, 2)
print("\nIt took ", elapsed_time, " minutes to run the script")
lines_per_hour = round(float(lines_cancelled) / elapsed_time, 2)
print("That's ", lines_per_hour, " lines per minute")

#loads after clicking S&C, after clicking each day, after sort, after filter
#need to rework using wait.until - this is trickier than i thought... speed is not that mcuch of a concern, time.sleep is fine for the most part
#need to handle more than 100, go to next page - or not? just run it twice lmfao
#need to handle error message pop ups (in a wave) - haven't run into this yet, might not be worth doing as long as waves are not allocated.


