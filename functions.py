def validate_input(prompt, min_value, max_value):
    """Проверка ввода для выбора номера строки
    """    
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if min_value <= value <= max_value and value != 0:
                return value
            elif value == 0:
                return -1
            else:
                print(f"Введенное значение должно быть в диапазоне от {min_value} до {max_value}")
        except ValueError:
            print("Введенное значение должно быть числом.")
        