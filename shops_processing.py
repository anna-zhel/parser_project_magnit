with open("shops_magnit_07_08_25.txt", "r", encoding='utf-8') as file:
    shop_list = file.readlines()
    shops_filtered = [shop.strip() for shop in shop_list if ("Москва" in shop)]
    shops_moscow = set(shops_filtered)
    shops_moscow.remove("107589, Москва г, Алтайская ул, дом № 33, корпус 7, этаж 1,пом. Iа,комнаты 1,1а,1б,2-9,9а,9б,10-27,пом. I,комнаты 1,1а,2-4,пом. Iб,комнаты 1,1а")
    shops_moscow.add("107589, Москва г, Алтайская ул, дом № 33, корпус 7, этаж 1")
    shops_moscow.remove("г Москва, проезд Петровско-Разумовский, д 2")
    shops_moscow.add("г Москва, Петровско-Разумовски д 2")
    # shops_moscow.remove("г Москва, проезд Старый Петровско-Разумовский, д 2")
    shops_moscow.add("г Москва, проезд Старый Петровско-Разумовски д 2")
    shops_moscow.remove("г Москва, проезд Петровско-Разумовский, д 24 к 19")
    shops_moscow.add("г Москва, проезд Петровско-Разумовски д 24 к 19")
    # shops_moscow.remove("г Москва, проезд Петровско-Разумовский, д 10")
    shops_moscow.add("г Москва, проезд Петровско-Разумовски д 10")

with open("shops_moscow.txt", "w", encoding='utf-8') as file:
    for shop in shops_moscow:
        file.write(f"{shop}\n")
