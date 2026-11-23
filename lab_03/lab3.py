import sys
import variant_mod
def main():
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Ошибка: аргумент должен быть целым числом. Используем значение по умолчанию: 3.")
            n = 3
    else:
        n = 3
    loads = {
        'A': [110, 115, 120, 118],
        'B': [95, 98, 92, 96],
        'C': [140, 145, 150, 148]
    }
    total_loads = variant_mod.analyze_phases(loads)
    is_imbalanced, max_diff = variant_mod.detect_imbalance(loads, max_diff=15.0)
    recent_samples = variant_mod.get_last_n_samples(loads, n)
    print("=== МОНИТОРИНГ ТРЕХФАЗНОЙ СЕТИ ===")
    print(f"Суммарные токи фаз: A={total_loads['A']}A, B={total_loads['B']}A, C={total_loads['C']}A")
    if is_imbalanced:
        print(f"Перекос фаз (ДА, макс. расхождение: {max_diff} A)")
    else:
        print(f"Перекос фаз (НЕТ, макс. расхождение: {max_diff} A)")

    print(f"Свежие замеры (срез [-{n}:]): {recent_samples}")

if __name__ == '__main__':
    main()