# celery
from celery import shared_task
from celery_config.controllers import sum_to_n

# standard
import time
import numpy as np
from sklearn.linear_model import LinearRegression
import random

# The "shared_task" decorator allows creation
# of Celery tasks for reusable apps as it doesn't
# need the instance of the Celery app.
# @celery_app.task()
@shared_task()
def add(x, y):
    return x + y

@shared_task
def wait_and_return():
    time.sleep(20)
    return 'Hello World!'

@shared_task
def sum_to_n_job(number):
    result = sum_to_n(number)
    return result

@shared_task
def estimate_stock_value(current_price, last_month_price, day_difference, shares_count):
    """
    Realiza una estimación lineal del precio futuro de una acción y calcula las ganancias esperadas
    
    Parameters:
    - current_price: float - Precio actual de la acción
    - last_month_price: float - Precio de la acción hace un mes
    - day_difference: int - Diferencia de días entre las fechas (típicamente 30 días)
    - shares_count: int - Número de acciones que posee el usuario

    Returns:
    - dict - Diccionario con los resultados (precio estimado y ganancias esperadas)
    """
    # Generamos 100 puntos de datos simulados distribuidos a lo largo del mes
    # Para esto, creamos una tendencia lineal con algo de variación aleatoria
    
    # Preparamos los datos para el modelo de regresión lineal
    num_points = 100  # Número de puntos para la regresión
    
    # Crear una secuencia de días (variable X)
    days = np.linspace(0, day_difference, num_points)
    
    # Calcular la pendiente entre los dos puntos conocidos
    slope = (current_price - last_month_price) / day_difference if day_difference else 0
    
    # Generar precios simulados para cada día con variación aleatoria controlada
    # La variación es proporcional a la diferencia de precios para mantener realismo
    price_variation = abs(current_price - last_month_price) * 0.1  # 10% de la diferencia como variación
    
    # Generar precios para cada día con tendencia lineal + ruido aleatorio
    prices = []
    for day in days:
        base_price = last_month_price + slope * day  # Tendencia lineal
        noise = random.uniform(-price_variation, price_variation)  # Ruido aleatorio
        prices.append(base_price + noise)
    
    # Asegurar que el último punto sea el precio actual
    prices[-1] = current_price
    
    # Convertir a arrays de numpy para el modelo
    X = days.reshape(-1, 1)  # Reshape para scikit-learn
    y = np.array(prices)
    
    # Crear y entrenar el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X, y)
    
    # Predicción para el próximo mes
    # Usamos day_difference como proyección (típicamente 30 días)
    next_month_day = day_difference * 2  # Proyección a un mes más
    predicted_price = model.predict(np.array([[next_month_day]]))[0]
    
    # Asegurarse de que el precio no sea negativo
    estimated_price = max(0, predicted_price)
    
    # Calcular ganancias esperadas
    current_value = current_price * shares_count
    estimated_value = estimated_price * shares_count
    expected_profit = estimated_value - current_value
    
    return {
        "current_price": current_price,
        "last_month_price": last_month_price,
        "estimated_price": round(estimated_price, 2),
        "shares_count": shares_count,
        "current_value": round(current_value, 2),
        "estimated_value": round(estimated_value, 2),
        "expected_profit": round(expected_profit, 2)
    }
