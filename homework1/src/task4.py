def calculate_discount(price, discount):
    if not isinstance(price, (int, float)) or not isinstance(discount, (int, float)):
        raise TypeError("Inputs must be numeric")
        
    return price - (price * discount / 100)