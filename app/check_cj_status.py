import os

def supplier_ready():
    return bool(os.getenv("SUPPLIER_API_KEY"))
    
if __name__ == "__main__":
    print("CJ API READY" if supplier_ready() else "WAITING FOR CJ API KEY")
