import time

def print_number():
    number = 1
    while True:
        print(number)
        number += 1
        time.sleep(5)

if __name__ == "__main__":
    print("開始輸出數字,每5秒一個...")
    print_number()