from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def main():
    options = webdriver.EdgeOptions()
    print("正在启动 Edge 浏览器...")
    driver = webdriver.Edge(options=options)

    try:
        # 打开初始地址
        url = "xxxxxx"
        driver.get(url)
        print("已打开页面，请在弹出的浏览器中手动完成登录。")
        print("正在监控 URL 变化... (等待进入 main.aspx，最多 300 秒)")

        # 核心修改 1：监听 URL 是否变化为目标页面
        wait = WebDriverWait(driver, 300)
        wait.until(EC.url_contains("A05pjpx/main.aspx"))
        
        print("已成功进入 main.aspx，等待题目元素加载...")

        # 核心修改 2：确认进入 URL 后，再次确认页面内的选项元素已渲染完毕
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='radio'] | //select"))
        )
        time.sleep(1) # 缓冲时间，防止动态 DOM 渲染未彻底完成

        print("正在执行自动选择 A...")

        # 1. 处理单选框 (Radio)
        radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
        radio_groups = {}
        
        for radio in radios:
            name = radio.get_attribute("name")
            if name:
                if name not in radio_groups:
                    radio_groups[name] = []
                radio_groups[name].append(radio)

        for name, group in radio_groups.items():
            selected = False
            for radio in group:
                value = radio.get_attribute("value")
                if value and value.upper() == 'A':
                    driver.execute_script("arguments[0].click();", radio)
                    selected = True
                    break
            
            if not selected and len(group) > 0:
                driver.execute_script("arguments[0].click();", group[0])

        # 2. 处理下拉菜单 (Select)
        selects = driver.find_elements(By.TAG_NAME, "select")
        for sel in selects:
            s_obj = Select(sel)
            found = False
            for i, opt in enumerate(s_obj.options):
                if opt.get_attribute("value").upper() == 'A' or "A" in opt.text:
                    s_obj.select_by_index(i)
                    found = True
                    break
            if not found and len(s_obj.options) > 0:
                s_obj.select_by_index(0)

        print("所有选项已尝试设为 A。请检查无误后自行点击提交。")
        input("按回车键关闭浏览器并结束脚本...")

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()