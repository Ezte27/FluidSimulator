# def encode_coordinates(x, y, precision=9.5):
#     # Calculate the precision factor
#     precision_factor = 10 ** precision
    
#     # Pad X and Y to 9 digits without decimal
#     x_padded = int(x * precision_factor)
#     y_padded = int(y * precision_factor)
    
#     # Find the next-highest power of 2 greater than 10^9
#     shift_bits = (2**30).bit_length()
    
#     # Encode the coordinates using bitwise OR
#     encoded_value = x_padded | (y_padded << shift_bits)
    
#     return encoded_value

# def decode_coordinates(encoded_value, precision=9.5):
#     # Calculate the precision factor
#     precision_factor = 10 ** precision
    
#     # Extract X and Y using bit masks and shift
#     shift_bits = (2**30).bit_length()
#     x_decoded = encoded_value & (2**shift_bits - 1)
#     y_decoded = (encoded_value >> shift_bits) & (2**shift_bits - 1)
    
#     # Divide by precision factor to get the original coordinates
#     x_original = x_decoded / precision_factor
#     y_original = y_decoded / precision_factor
    
#     return x_original, y_original

# # Example usage
# precision = 9.5
# coordinates = (107.13, 52.22)

# # Encode coordinates
# encoded_value = encode_coordinates(*coordinates, precision=precision)
# print("Encoded Value:", encoded_value)

# # Decode coordinates
# decoded_coordinates = decode_coordinates(encoded_value, precision=precision)
# print("Decoded Coordinates:", decoded_coordinates)

def encode_coordinates(x:float, y:float):
    '''
    Precision is the amount of digits in each coordinate
    Example: 
        x = 42.56
        y = 65.24
        precision = 4

    Note: Decimal digits must match in length
    '''

    # Check for mathcing decimals and precision
    # checkForMatchingDecimals(x, y, decimal_precision)

    # Change x and y to strings

    x = str(x)
    y = str(y)

    difference = len(x) - len(y)
    
    if difference != 0:
        while difference != 0:
            if difference < 0:
                x += '0'  
            else:
                y += '0'
            difference = len(x) - len(y)

    # Move decimals to the other side of the point to make it an integer
    # without losing significant figures
    x_int = x.replace('.', '')
    y_int = y.replace('.', '')

    encoded_value = x_int + y_int

    return encoded_value

def decode_coordinates(encoded_value:str, decimal_precision:int):
    
    # Calculate the length of the encoded value to split it in half
    n = len(encoded_value)

    # Calculate the length of each coordinate
    n_coord = int(n / 2)

    # Calculate the length of the digits without decimals
    n_digits = int(n_coord - decimal_precision)

    # Split enconded value in half with no decimal point
    x_int = encoded_value[:n_coord]
    y_int = encoded_value[n_coord:]

    # Add the decimal point to each coordinate using the decimal_precision
    x = x_int[0:n_digits] + '.' + x_int[n_digits:]
    y = y_int[0:n_digits] + '.' + y_int[n_digits:]

    return (x, y)

def checkForMatchingDecimals(x, y, decimal_precision):
    x_digits = len(str(x).replace('.', ''))
    y_digits = len(str(y).replace('.', ''))

    difference = x_digits - y_digits
    
    if difference != 0:
        print(f"[ERROR] Digits do NOT match!")
        print(f"x_digits = {x_digits}")
        print(f"y_digits = {y_digits}")
        raise Exception("[ERROR] Digits do NOT match! The number of digits in the x coordinate is different from the number of digits in the y coordinate.")
    
    x_decimals = len(str(x).split('.')[-1])
    y_decimals = len(str(y).split('.')[-1])

    difference = x_decimals - y_decimals

    if difference != 0:
        print(f"[ERROR] Decimal digits do NOT match!")
        raise Exception("[ERROR] Decimal digits do NOT match!")

    if x_decimals != decimal_precision:
        print(f"[ERROR] Digit amount and precision factor do NOT match!")
        print(f'x_decimals = {x_decimals}')
        print(f'decimal_precision = {decimal_precision}')
        raise Exception(f"[ERROR] Number of digits and precision factor do NOT match! A simple way to fix this error is to change the decimal_precision value to the number of decimals = {x_decimals}, or change the number of decimals in the coordinates x and y.")

# Example Usage
decimal_precision = 1
coordinates = (0, 0)

# Encode coordinates
encoded_value = encode_coordinates(coordinates[0], coordinates[1])
decoded_value = decode_coordinates(encoded_value, decimal_precision)

print(f'Starting Coordinates: {coordinates}')
print(f'Encoded Value: {encoded_value}')
print(f'Decoded Value: {decoded_value}')
print(f'Decoded Value (float): {float(decoded_value[0]), float(decoded_value[1])}')