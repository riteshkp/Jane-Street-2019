def avg(iterable):
    return sum(iterable) // len(iterable)


def bond_strategy(exchange, bond_price, order_id):
    # Exchange = TCP connection
    bond_price = avg(bond_price)
    if bond_price < 1000:
        print("---- Attempting to buy bonds for $999. ------ \n")
        exchange.write_to_exchange(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": "BOND",
                "dir": "BUY",
                "price": 999,
                "size": 100,
            }
        )
        print("---- Attempting to sell bonds for $1001. ------ \n")
        exchange.write_to_exchange(
            {
                "type": "add",
                "order_id": order_id + 1,
                "symbol": "BOND",
                "dir": "SELL",
                "price": 1001,
                "size": 100,
            }
        )


def valbz_vale(exchange, valbz_price, vale_price, order_id):
    vale_price_mean = avg(vale_price)
    valbz_price_mean = avg(valbz_price)
    val_price = val_price[-1]
    valbz_price = valbz_price[-1]
    ratio_mean = vale_price_mean / valbz_price_mean
    ratio = val_price / valbz_price

    if ratio > (1.25*ratio_mean):
        print("---- Buy BZ, convert vale, sell vale ------ \n")
        print("Vale price: " + str(vale_price) + "\n")
        print("BZ price: " + str(valbz_price) + "\n")
        exchange.write_to_exchange(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": "VALBZ",
                "dir": "BUY",
                "price": valbz_price,
                "size": 10,
            }
        )
        exchange.write_to_exchange(
            {
                "type": "convert",
                "order_id": order_id + 1,
                "symbol": "VALE",
                "dir": "BUY",
                "size": 10,
            }
        )
        exchange.write_to_exchange(
            {
                "type": "add",
                "order_id": order_id + 2,
                "symbol": "VALE",
                "dir": "SELL",
                "price": vale_price,
                "size": 10,
            }
        )
    elif (1.25*ratio_mean) and ratio < ratio_mean:
        print("---- Buy vale, convert BZ, sell BZ ------ \n")
        print("BZ price: " + str(valbz_price) + "\n")
        print("Vale price: " + str(vale_price) + "\n")
        exchange.write_to_exchange(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": "VALE",
                "dir": "BUY",
                "price": vale_price,
                "size": 10,
            }
        )
        exchange.write_to_exchange(
            {
                "type": "convert",
                "order_id": order_id + 1,
                "symbol": "VALE",
                "dir": "SELL",
                "size": 10,
            }
        )
        exchange.write_to_exchange(
            {
                "type": "add",
                "order_id": order_id + 2,
                "symbol": "VALBZ",
                "dir": "SELL",
                "price": valbz_price,
                "size": 10,
            }
        )

def xlf_strat(exchange, xlf_price, bond_price, gs_price, ms_price, wfc_price, order_id):
    #long
    #print("XLF: " + str(len(xlf_price)))
    #print("Bond: " + str(len(bond_price)))
    #print("GS: " + str(len(gs_price)))
    #print("MS: " + str(len(ms_price)))
    #print("wfc: " + str(len(wfc_price)))
    if(len(xlf_price) != 0 and len(bond_price) != 0 and len(gs_price) != 0 and len(ms_price) != 0 and len(wfc_price) != 0):
        xlf_mean = avg(xlf_price)
        bond_price = avg(bond_price)
        gs_price = avg(gs_price)
        ms_price = avg(ms_price)
        wfc_price = avg(wfc_price)

        if 10 * xlf_mean + 100 < (3 * bond_price + 2 * gs_price + 3 * ms_price + 2 * wfc_price):
            print("XLF: " + str(xlf_mean))
            print("Buying XLF at" + str(xlf_price[1] + 1))
            exchange.write_to_exchange({"type": "add", "order_id": order_id, "symbol": "XLF", "dir": "BUY",
                                            "price": xlf_price[1] + 1, "size": 100})

            exchange.write_to_exchange({"type": "convert", "order_id": order_id  + 1, "symbol": "XLF", "dir": "SELL", "size": 100})

            exchange.write_to_exchange({"type": "add", "order_id": order_id + 2, "symbol": "BOND", "dir": "SELL",
                                            "price": xlf_price[2] - 1, "size": 30})

            exchange.write_to_exchange({"type": "add", "order_id": order_id + 3, "symbol": "GS", "dir": "SELL",
                                            "price": xlf_price[3] - 1, "size": 20})

            exchange.write_to_exchange({"type": "add", "order_id": order_id + 4, "symbol": "MS", "dir": "SELL",
                                            "price": xlf_price[4] - 1, "size": 30})

            exchange.write_to_exchange({"type": "add", "order_id": order_id + 5, "symbol": "WFC", "dir": "SELL",
                                            "price": xlf_price[5] - 1, "size": 20})
        #short
        if 10 * xlf_mean - 100 > (3 * bond_price + 2 * gs_price + 3 * ms_price + 2 * wfc_price):
            print("XLF: " + str(xlf_mean))
            print("Selling XLF at" + str(xlf_price[1] + 1))
            exchange.write_to_exchange({"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY",
                    "price": xlf_price[2] - 1, "size": 30})
            exchange.write_to_exchange({"type": "add", "order_id": order_id + 1, "symbol": "GS", "dir": "BUY",
                                            "price": xlf_price[3] - 1, "size": 20})
            exchange.write_to_exchange({"type": "add", "order_id": order_id + 2, "symbol": "MS", "dir": "BUY",
                                            "price": xlf_price[4] - 1, "size": 30})
            exchange.write_to_exchange({"type": "add", "order_id": order_id + 3, "symbol": "WFC", "dir": "BUY",
                                            "price": xlf_price[5] - 1, "size": 20})
            exchange.write_to_exchange({"type": "convert", "order_id": order_id + 4, "symbol": "XLF", "dir": "BUY", "size": 100})
            exchange.write_to_exchange( {"type": "add", "order_id": order_id + 5, "symbol": "XLF", "dir": "SELL","price": xlf_price[1] + 1, "size": 100})