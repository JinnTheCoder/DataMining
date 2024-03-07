from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv

# Khởi tạo trình duyệt
driver = webdriver.Chrome()
action_chains = ActionChains(driver)
# Mở trang web
for year in range(2011, 2023, 1):
    for month in range(1, 13, 1):
        url = "https://www.timeanddate.com/weather/vietnam/ho-chi-minh/historic?month={}&year={}"
        url = url.format(month, year)
        print(url)
        driver.get(url)

        # Đợi trang web tải hoàn tất (có thể tùy chỉnh thời gian chờ)
        driver.implicitly_wait(10)

        # Tìm và lấy dữ liệu từ div có id là "weather"
        weather_div = driver.find_element(By.ID, "weather")

        # Tìm tất cả các div con có id bắt đầu bằng "ws_"
        ws_divs = weather_div.find_elements(By.XPATH, "//div[starts-with(@id, 'ws_')]")
        path = 'weather_data_{}-{}.csv'
        path = path.format(year, month)
        with open(path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date', 'Temperature', 'Weather Description', 'Humidity', 'Barometer', 'WindDirection', 'WindSpeed'])
            # Lặp qua từng div con và lấy thông tin
            for ws_div in ws_divs:
                # Di chuột vào div để hiển thị thông tin
                action_chains.move_to_element(ws_div).perform()
                
                # Lấy thông tin từ tooltip
                tooltip_div = driver.find_element(By.CLASS_NAME, "weatherTooltip")
                date = tooltip_div.find_element(By.CLASS_NAME, "date").text
                temp = tooltip_div.find_element(By.CLASS_NAME, "temp").text
                wdesc = tooltip_div.find_element(By.CLASS_NAME, "wdesc").text

                midblock = tooltip_div.find_element(By.CLASS_NAME, "mid__block")
                humidity = midblock.find_elements(By.TAG_NAME, "div")[0].text
                barometer = midblock.find_elements(By.TAG_NAME, "div")[1].text

                rightblock = tooltip_div.find_element(By.CLASS_NAME, "right__block")
                winddirection = tooltip_div.find_element(By.CLASS_NAME, "windDirection").text
                windspeed = rightblock.find_elements(By.TAG_NAME, "div")[1].text
                
                # In thông tins
                csv_writer.writerow([date, temp, wdesc, humidity, barometer, winddirection, windspeed])
            
# Đóng trình duyệt
driver.quit()
