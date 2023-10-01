import ephem

def calculate_rise_set(latitude, longitude, date, celestial_body):
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.date = date
    
    # Create an object for the celestial body
    body = ephem.__getattribute__(celestial_body)()
    
    rise_time = observer.previous_rising(body).datetime()
    set_time = observer.next_setting(body).datetime()
    
    return rise_time, set_time

if __name__ == "__main__":
    # Example: Calculate rise and set times for Mars on a specific date
    print('Insert Lat')
    latitude = float(input())  # New York City latitude
    print('Insert Long')
    longitude = float(input())  # New York City longitude
    print('Insert Date in yyy-mm-dd')
    date = str(input())  # Specify the date in yyyy-mm-dd format
    print('Object name, eg Mars')
    celestial_body = str(input())  # The name of the celestial object you're interested in
    
    rise_time, set_time = calculate_rise_set(latitude, longitude, date, celestial_body)
    
    print("{0:s} Rise Time: {1:s}".format(celestial_body, rise_time))
    print("{0:s} Set Time: {1:s}".format(celestial_body, set_time))
