def format_weather(data):
    loc = data["location"]
    cur = data["current"]
    return (f"Thời tiết tại {loc['name']}, {loc['country']}:\n"
            f"Tình trạng: {cur['condition']['text']}\n"
            f"Nhiệt độ: {cur['temp_c']}°C\n"
            f"Cảm giác như: {cur['feelslike_c']}°C\n"
            f"Độ ẩm: {cur['humidity']}%\n"
            f"Gió: {cur['wind_kph']} km/h {cur['wind_dir']}\n")


