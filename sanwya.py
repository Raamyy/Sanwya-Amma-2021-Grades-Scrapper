import requests
from bs4 import BeautifulSoup
import pickle
import math
import multiprocessing

url = "https://natega.youm7.com/Home/Result"

def get_student_html(seat_no):
    payload='seating_no='+seat_no
    headers = {
    'authority': 'natega.youm7.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'origin': 'https://natega.youm7.com',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://natega.youm7.com/',
    'accept-language': 'en,ar;q=0.9,en-US;q=0.8',
    'cookie': '__auc=4ac3a7ce17b4a4f6f6150ad5e79; _gid=GA1.2.292691701.1629242608; _ga=GA1.2.273130107.1629039325; _ga_J7S2SZJ3N7=GS1.1.1629287375.4.1.1629287416.0; __asc=373826a617b59aa8942f109ae37; _gat_gtag_UA_204279993_1=1; AWSALB=zEIr3/9ZsK8NpP+UaqalkjJbAOoeFlUsgx465gJDMbDUqvPI4NCIMftzGQCWbrewjHezC6j3xVA8NaMYCJlUQNhGKfqsvr2KuEm6W3NpNn4xQX6CUiaUJLAnABvS; AWSALB=5v5URYf9ed0t9oVlig2KkwGmgYFMW9+IJ70oM98hUjcQQphBtGTVj6HIOzZYGch6wSt+fQmQwNpOHM+8WnLX/n+AnvwBbLFO6dyfBo2sBcveDvfkLXDEkHgiNO5m; AWSALBCORS=5v5URYf9ed0t9oVlig2KkwGmgYFMW9+IJ70oM98hUjcQQphBtGTVj6HIOzZYGch6wSt+fQmQwNpOHM+8WnLX/n+AnvwBbLFO6dyfBo2sBcveDvfkLXDEkHgiNO5m'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response)
    return response.text

def parse_student_object(student_html):
    soup = BeautifulSoup(student_html, 'html.parser')
    # print(soup)
    student_object = {}
    result_items = soup.find_all('li', {'class': 'resultItem'})
    for result_item in result_items:
        # print(result_item.contents)
        key = result_item.contents[1].text.replace(':','').strip()
        value = result_item.contents[3].text.strip()
        student_object[key] = value
    return student_object

def save_pickle(file_name, data):
    pickle_file = open(f"data/{file_name}.pkl", "wb")
    pickle.dump(data, pickle_file)
    pickle_file.close()


def get_students(start_seatNo, end_seatNo):
    print(f'started {str(start_seatNo)}-{str(end_seatNo)}')
    seat_no = start_seatNo
    students = []
    wrong_streak = 0
    while seat_no <= end_seatNo:
        print(end_seatNo - seat_no)
        html = get_student_html(str(seat_no))
        student_Data = parse_student_object(html)
        if(student_Data):
            students.append(student_Data)
            wrong_streak = 0
        else:
            print(seat_no, ' is not available!')
            wrong_streak += 1

        # if 20 consecutive seat numbers are not found jump 20 seat numebrs
        if wrong_streak >= 20:
            print(f'wrong streak at {seat_no}')
            seat_no += 20
        else:
            seat_no += 1

    save_pickle(f'students_data {str(start_seatNo)}-{str(end_seatNo)}', students)
    print(f'saved {str(start_seatNo)}-{str(end_seatNo)} .... HURRRRRRRRAAAAAAAAAAAAAAAAAYYYYYYYYYYYy')
    return students

def start_processing():
    start = 1020533 + 25_000 + 25_000 + 25_000
    end = start + 50_000
    window = min(250, (end - start + 1) )
    threads = []

    thread_count = math.ceil((end - start + 1)  / window)
    
    thread_start = start
    for i in range(thread_count ):
        threads.append(multiprocessing.Process(target=get_students,args=(thread_start + 1 ,thread_start+window)))
        thread_start += window

    for thread in threads:
        thread.start()


if __name__ == '__main__':
    start_processing()