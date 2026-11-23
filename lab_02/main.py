def evaluate_motor_speed(rpm_list, nominal=1500, tolerance=0.05):
    total_cycles = len(rpm_list)
    if total_cycles == 0:
        return 0.0

    max_deviation = nominal * tolerance
    out_of_tolerance_count = 0

    print(f"Контроль электродвигателя (Норма: {nominal} ± {max_deviation:.0f} об/мин)")

    for i, rpm in enumerate(rpm_list, start=1):
        deviation = rpm - nominal
        if abs(deviation) > max_deviation:
            out_of_tolerance_count += 1
            print(f"Цикл {i}: {rpm} об/мин. Отклонение: {deviation:+.0f} -> ВЫХОД ЗА ДОПУСК!")
        else:
            print(f"Цикл {i}: {rpm} об/мин. Отклонение: {deviation:+.0f} -> Норма")

    serviceable_cycles = total_cycles - out_of_tolerance_count
    serviceable_percentage = (serviceable_cycles / total_cycles) * 100
    return serviceable_percentage