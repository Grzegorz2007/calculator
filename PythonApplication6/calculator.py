from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def summa(a: float, b: float) -> float:
    return a + b

def sub(a: float, b: float) -> float:
    return a - b

def mult(a: float, b: float) -> float:
    return a * b

def div(a: float, b: float) -> float:
    if b != 0:
        return a / b
    raise ZeroDivisionError("Деление на ноль невозможно")

def sqrt(a: float) -> float:
    if a >= 0:
        return math.sqrt(a)
    raise ValueError("Нельзя извлечь корень из отрицательного числа")

def percentage(a: float, b: float) -> float:
    if b != 0:
        return (a / b) * 100
    raise ZeroDivisionError("Деление на ноль невозможно")

def logarithm(a: float, b: float) -> float:
    if a <= 0:
        raise ValueError("Логарифм определён только для положительных чисел")
    if b <= 0 or b == 1:
        raise ValueError("Основание логарифма должно быть положительным и не равным 1")
    return math.log(a, b)

from typing import Optional

def validate_numbers(first: str, second: Optional[str], oper: str) -> tuple[float, Optional[float]]:
    try:
        first_num = float(first)
        second_num = float(second) if second is not None and oper != 'sqrt' else None
        
        if oper == 'sqrt' and first_num < 0:
            raise ValueError("Нельзя извлечь корень из отрицательного числа")
        
        return first_num, second_num
    except ValueError as e:
        if "could not convert string to float" in str(e):
            raise ValueError("Некорректный формат числа")
        raise

from typing import Union, Optional

def calc(first: str, second: Optional[str], oper: str) -> tuple[Optional[Union[float, str]], Optional[str]]:
    try:
        # Валидация и преобразование входных данных
        first_num, second_num = validate_numbers(first, second, oper)
        
        # Выполнение операции
        if oper == '+':
            result = summa(first_num, second_num)
        elif oper == '-':
            result = sub(first_num, second_num)
        elif oper == '*':
            result = mult(first_num, second_num)
        elif oper == '/':
            result = div(first_num, second_num)
        elif oper == '**':
            result = first_num ** second_num
        elif oper == '%':
            result = percentage(first_num, second_num)
        elif oper == 'log':
            result = logarithm(first_num, second_num)
        elif oper == 'sqrt':
            result = sqrt(first_num)
        else:
            return None, "Некорректная операция"

        # Форматирование результата
        if isinstance(result, float):
            # Округляем до 6 знаков после запятой и убираем лишние нули
            result = float(f"{result:.6f}".rstrip('0').rstrip('.'))
        
        return result, None

    except ValueError as e:
        return None, str(e)
    except ZeroDivisionError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Произошла ошибка: {str(e)}"

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Отсутствуют данные запроса'}), 400
        
        first = data.get('first')
        second = data.get('second')
        oper = data.get('operation')
        
        if first is None or oper is None:
            return jsonify({'error': 'Отсутствуют обязательные параметры'}), 400

        result, error = calc(first, second, oper)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': f'Ошибка сервера: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
