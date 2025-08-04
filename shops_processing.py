# if __name__ == "main":
with open("shops_magnit_16_07_25.txt", "r", encoding='utf-8') as file:
    shop_list = file.readlines()
    shops_filtered = [shop.strip() for shop in shop_list if ("Москва" in shop)]
    shops_moscow = set(shops_filtered)
    shops_moscow.remove("107589, Москва г, Алтайская ул, дом № 33, корпус 7, этаж 1,пом. Iа,комнаты 1,1а,1б,2-9,9а,9б,10-27,пом. I,комнаты 1,1а,2-4,пом. Iб,комнаты 1,1а")
    shops_moscow.add("107589, Москва г, Алтайская ул, дом № 33, корпус 7, этаж 1")
    shops_moscow.remove("127220, Москва г, Петровско-Разумовский проезд, дом № 2")
    shops_moscow.add("127220, Москва г, Петровско-Разумовски проезд, дом № 2")
    shops_moscow.remove("127287, Москва г, Старый Петровско-Разумовский проезд, дом № 2, кв.10Н")
    shops_moscow.add("127287, Москва г, Старый Петровско-Разумовски проезд, дом № 2, кв.10Н")
    shops_moscow.remove("127287, Москва г, Петровско-Разумовский проезд, дом № 24, корпус 19, кв.1/1")
    shops_moscow.add("127287, Москва г, Петровско-Разумовски проезд, дом № 24, корпус 19, кв.1/1")
    shops_moscow.remove("127220, Москва г, Петровско-Разумовский проезд, дом № 10, корпус 1, кв.1")
    shops_moscow.add("127220, Москва г, Петровско-Разумовски проезд, дом № 10, корпус 1, кв.1")
    shops_moscow.remove("107199, Москва г, Щёлковское ш, дом № 27, корпус А")
    shops_moscow.add("107241, Москва г, Щёлковское ш, дом № 27, корпус А")

        #for sh in shops_moscow:
            #if "Алтайская" in sh:
                #print(sh)
        # print(len(shops_moscow))

        # somehow for now a number of existing shops are excluded from the search list by Magnit