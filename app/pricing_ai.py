def dynamic_price(cost: float, score: int):

    cost=float(cost)

    if score>=90:
        multiplier=4.0
    elif score>=80:
        multiplier=3.5
    elif score>=70:
        multiplier=3.0
    else:
        multiplier=2.5

    price=round(cost*multiplier,2)

    return {
        "cost":cost,
        "score":score,
        "price":price,
        "multiplier":multiplier
    }


if __name__=="__main__":

    print(dynamic_price(1.74,95))
