

def get_two_float(f_str, n):
    f_str = str(f_str)     
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return ".".join([a, c])