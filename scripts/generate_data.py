import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(filename="data/sample_data.csv", periods=100):
    start_date = datetime(2024, 1, 1, 9, 0)
    data = []
    
    current_price = 1.0850
    
    for i in range(periods):
        timestamp = start_date + timedelta(minutes=15 * i)
        
        # Generar un movimiento aleatorio pero controlado
        open_p = current_price
        high_p = open_p + abs(np.random.normal(0, 0.0005))
        low_p = open_p - abs(np.random.normal(0, 0.0005))
        close_p = np.random.uniform(low_p, high_p)
        volume = np.random.randint(100, 1000)
        
        data.append([timestamp, open_p, high_p, low_p, close_p, volume])
        current_price = close_p

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df.to_csv(filename, index=False)
    print(f"Archivo {filename} generado con {periods} velas.")

if __name__ == "__main__":
    generate_sample_data()
