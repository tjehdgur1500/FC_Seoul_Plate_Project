import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from .models import Restaurant


class Crawling:
    # 망고플레이트 성수동 검색 결과 하단 다음페이지 모음

    # base_url = 'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page='
    # for i in range(1, 20):
    #     url = f'{base_url}{i}'
    #     response = requests.get(url)
    #
    #     if requests.status_code == 200:
    #         pass

    search_paging_array = [
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=1',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=2',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=3',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=4',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=5',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=6',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=7',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=8',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=9',
        'https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99?keyword=%EC%84%B1%EC%88%98%EB%8F%99&page=10',
    ]

    driver = webdriver.Chrome('/Users/mellomasi/Downloads/chromedriver')

    driver.implicitly_wait(3)

    # driver 필요 여부 확인
    driver.get('https://www.mangoplate.com/search/%EC%84%B1%EC%88%98%EB%8F%99')

    rs = []
    # 식당 상세페이지 url get
    for page_index in range(len(search_paging_array)):
        driver.get(search_paging_array[page_index])
        for val in driver.find_elements_by_xpath(
                '/html/body/main/article/div[2]/div/div/section/div[3]/ul/li/div/figure/a'):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/83.0.4103.106 Safari/537.36 '
            }
            url = val.get_attribute('href')
            print(url)
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')

            rest_name = soup.find(class_='restaurant_name').text.strip().replace('\n', '')
            if soup.find(class_='rate-point'):
                rest_star = soup.find(class_='rate-point').text.strip().replace('\n', '')
            else:
                rest_star = None

            source = soup.find('tbody')
            name = source.find_all('td')
            value = source.find_all('th')

            rest_address = None
            rest_food = None
            rest_phone_number = None
            rest_sale = None
            rest_time = None
            rest_break_time = None

            for key, value in zip(value, name):
                key = key.text.strip().replace('\n', '')
                value = value.text.strip().replace('\n', '')

                if key == '주소':
                    rest_address = value
                elif key == '음식 종류':
                    rest_food = value
                elif key == '전화번호':
                    rest_phone_number = value
                elif key == '가격대':
                    rest_sale = value
                elif key == '영업시간':
                    rest_time = value
                elif key == '쉬는시간':
                    rest_break_time = value

            # unique 값을 기준으로 get_or_create() 호출
            Restaurant.objects.get_or_create(
                rest_name=rest_name,
                rest_star=rest_star,
                rest_address=rest_address,
                rest_food=rest_food,
                rest_phone_number=rest_phone_number,
                rest_sale=rest_sale,
                rest_time=rest_time,
                rest_break_time=rest_break_time,
            )

    driver.close()


start_crawling = Crawling()
start_crawling
