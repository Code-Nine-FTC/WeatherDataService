import datetime
import math
import random

# --- Configuration ---
# These parameter_ids are assumed to map to your parameter_types as follows:
# Parameter ID 1 -> Parameter Type ID 1 (Umidade)
# Parameter ID 2 -> Parameter Type ID 2 (Temperatura)
# Parameter ID 3 -> Parameter Type ID 3 (Pressão atmosférica)
# Parameter ID 4 -> Parameter Type ID 4 (Chuva)
PARAMETER_IDS_TO_SIMULATE = [1, 2, 3, 4]
MONTHS_AGO_START = 6
HOURLY_INTERVAL = 1


# --- Realistic Value Generation ---
def get_seasonal_temperature_base(month_of_year):
    """
    Provides a very basic seasonal base temperature.
    Adjust these ranges for your typical climate.
    (1=Jan, 12=Dec)
    """
    if month_of_year in [12, 1, 2]:  # Winter months
        return random.uniform(5.0, 15.0)
    if month_of_year in [3, 4, 5]:  # Spring months
        return random.uniform(12.0, 22.0)
    if month_of_year in [6, 7, 8]:  # Summer months
        return random.uniform(20.0, 32.0)
    if month_of_year in [9, 10, 11]:  # Autumn months
        return random.uniform(10.0, 20.0)
    return random.uniform(15.0, 25.0)  # Default


def generate_realistic_value(parameter_id, current_datetime_utc):
    """Generates a realistic value based on the parameter_id and current datetime."""

    hour_of_day = current_datetime_utc.hour
    month_of_year = current_datetime_utc.month

    if parameter_id == 1:  # Umidade (%)
        # Humidity can be higher at night/cooler times
        base_humidity = random.uniform(40.0, 70.0)
        if hour_of_day < 6 or hour_of_day > 20:  # Night/Early morning
            value = round(base_humidity + random.uniform(10.0, 25.0), 1)
        else:  # Daytime
            value = round(base_humidity + random.uniform(-10.0, 10.0), 1)
        return max(20.0, min(100.0, value))  # Clamp between 20% and 100%

    if parameter_id == 2:  # Temperatura (ºC)
        seasonal_base = get_seasonal_temperature_base(month_of_year)
        # Simple daily cycle: sine wave approximation
        # Max temp around 2 PM (14:00), min around 4 AM (04:00)
        daily_variation_amplitude = random.uniform(3.0, 8.0)  # How much temp varies in a day
        temp_offset = math.sin((hour_of_day - 10) * (math.pi / 12)) * daily_variation_amplitude
        value = round(
            seasonal_base + temp_offset + random.uniform(-1.0, 1.0), 2
        )  # Add some noise
        return value

    if parameter_id == 3:  # Pressão atmosférica (hPa)
        # Pressure doesn't vary as wildly or predictably on short scales without weather systems
        value = round(random.uniform(980.0, 1040.0), 2)
        return value

    if parameter_id == 4:  # Chuva (mm)
        # Rain is often zero, with occasional bursts.
        # Chance of rain might vary by season (simplified here)
        chance_of_rain = 0.05  # Base 5% chance of rain in any given hour
        if month_of_year in [4, 5, 10, 11]:  # Wetter months example
            chance_of_rain = 0.10

        if random.random() < chance_of_rain:
            if random.random() < 0.7:  # 70% of rain events are light
                value = round(random.uniform(0.1, 2.5), 2)  # Light rain
            elif random.random() < 0.9:  # Next 20% are moderate
                value = round(random.uniform(2.5, 10.0), 2)  # Moderate rain
            else:  # Remaining 10% are heavy
                value = round(random.uniform(10.0, 25.0), 2)  # Heavy rain
        else:
            value = 0.0
        return value
    # Fallback for unknown parameter_id
    return round(random.uniform(0.0, 10.0), 2)


# --- Main Script Logic ---
def generate_measure_inserts():
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # Calculate start_date: X months ago
    # This is an approximation; for exact month boundaries, use dateutil.relativedelta
    start_date_utc = now_utc - datetime.timedelta(days=MONTHS_AGO_START * 30)
    # Set to the beginning of the hour for clean intervals
    start_date_utc = start_date_utc.replace(minute=0, second=0, microsecond=0)

    current_datetime_utc = start_date_utc
    time_interval = datetime.timedelta(hours=HOURLY_INTERVAL)

    sql_inserts = []

    print(
        f"-- Generating measures from approximately {start_date_utc.strftime('%Y-%m-%d %H:%M:%S %Z')} to {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    print(f"-- for parameter IDs: {PARAMETER_IDS_TO_SIMULATE}")
    print(f"-- Occurring every {HOURLY_INTERVAL} hour(s) with realistic values.\n")

    while current_datetime_utc <= now_utc:
        measure_date_epoch = int(current_datetime_utc.timestamp())

        for param_id in PARAMETER_IDS_TO_SIMULATE:
            measure_value = generate_realistic_value(param_id, current_datetime_utc)

            # Assuming 'id' in 'measures' is auto-incrementing.
            sql_inserts.append(
                f"INSERT INTO measures (value, measure_date, parameter_id) "
                f"VALUES ({measure_value}, {measure_date_epoch}, {param_id});"
            )

        current_datetime_utc += time_interval

    return sql_inserts


if __name__ == "__main__":
    inserts = generate_measure_inserts()
    for insert_statement in inserts:
        print(insert_statement)

    print(f"\n-- Generated {len(inserts)} measure records.")
