# celery
from celery import shared_task
from celery_config.controllers import sum_to_n

# standard
import time

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
def estimate_stock_value(current_price, last_month_price, shares_count):
    """
    Realiza una estimación lineal del precio futuro de una acción y calcula las ganancias esperadas
    
    Parameters:
    - current_price: float - Precio actual de la acción
    - last_month_price: float - Precio de la acción hace un mes
    - shares_count: int - Número de acciones que posee el usuario
    
    Returns:
    - dict - Diccionario con los resultados (precio estimado y ganancias esperadas)
    """
    # Calcular la tasa de cambio mensual
    monthly_change_rate = current_price - last_month_price
    
    # Estimar el precio para el próximo mes mediante proyección lineal
    estimated_price = current_price + monthly_change_rate
    
    # Calcular ganancias esperadas (valor actual vs valor estimado)
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
