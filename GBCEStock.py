import datetime
import os
import logging
import traceback


class StockMarket(object):
    """
    StockMarket class.
    This class contains two main attributes:
    trades -> memcache "like" for the trades
    exchange_table_data -> stock table
    """

    __slots__ = ["trades", "exchange_table_data"]

    def __init__(self):
        self.trades = {}
        self.exchange_table_data = {
            "TEA": {
                "type": "Common",
                "last_dividend": 0,
                "fixed_dividend": None,
                "value": 100,
            },
            "POP": {
                "type": "Common",
                "last_dividend": 8,
                "fixed_dividend": None,
                "value": 100,
            },
            "ALE": {
                "type": "Common",
                "last_dividend": 23,
                "fixed_dividend": None,
                "value": 60,
            },
            "GIN": {
                "type": "Preferred",
                "last_dividend": 8,
                "fixed_dividend": 0.02,
                "value": 100,
            },
            "JOE": {
                "type": "Common",
                "last_dividend": 13,
                "fixed_dividend": None,
                "value": 250,
            },
        }

    def calculate_dividend(self, stock_name, price):
        """
        Calculate dividend.
        """

        rule = self.exchange_table_data[stock_name]

        if rule["type"] == "Common":
            dividend = rule["last_dividend"] / price
        else:
            dividend = rule["fixed_dividend"] * rule["value"] / price

        return dividend

    def calculate_pe_ration(self, stock_name, price):
        """
        Calculate P/E Ratio.
        """   
        return price / self.calculate_dividend(stock_name=stock_name, price=price)

    def calculate_volume_weighted(self, stock_name):
        """
        Calculate volume weighted.
        """

        last_five_minutes = int((datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%M"))
        total = 0
        quantities = 0
        for trade in self.trades.keys():
            if trade >= last_five_minutes and self.trades[trade]["stock_name"] == stock_name:
                total = self.trades[trade]["quantity"] * self.trades[trade]["price"]
                quantities += self.trades[trade]["quantity"]

        quantities = 1 if quantities == 0 else quantities

        return total / quantities

    def calculate_gbce(self):
        """
        Calculate GBCE
        """
        return sum([trade["price"] for trade in self.trades.values()])

    def add_record(self, stock_name, quantity, buy=False):
        """
        Add record to the mem data.
        """
        timestamp = datetime.datetime.now().strftime("%M")
        self.trades[int(timestamp)] = {
            "stock_name": stock_name,
            "action": "buy" if buy else "sell",
            "quantity": quantity,
            "price": self.exchange_table_data[stock_name]["value"]
        }

        print("Record added successfully! \n")
    def validate_symbol(self, stock_name):
        """
        Validate if the given symbol is present in the table data.
        """
        if stock_name not in self.exchange_table_data:
            raise ValueError("Stock {} does not exist".format(stock_name))

        return stock_name

    def convert_to_float(self, value):
        """
        Convert value to float.
        """

        try:
            value = float(value)
        except ValueError:
            raise ValueError("Value is not correct")

        return value

def menu():
    """
    Global Beverage Corporation Exchange Menu screen.
    """
    clear = lambda: os.system('cls')
    if not new : input()
    clear()
    print("\n\t\t\t\t\tGlobal Beverage Corporation Exchange Menu\n")
    print("\n\t\t\t\t\t1) Calculate dividend\n")
    print("\t\t\t\t\t2) Calculate P/E Ratio\n")
    print("\t\t\t\t\t3) Add trade\n")
    print("\t\t\t\t\t4) Calculate Volume Weighted Stock Price for the past 5 minutes\n")
    print("\t\t\t\t\t5) Calculate GBCE of all shares\n")
    print("\t\t\t\t\t6) Quit\n")


if __name__ == "__main__":
    running = True
    stockmarket = StockMarket()
    new = 1
    # unit_tests = UnitTests()
    logging.basicConfig(filename='server.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    # Loop through the menu
    while running:
        menu()
        new = 0
        option = input("\nEnter Selection  ")

        try:
            if option == "1" or option == "2" or option == "3" or option == "4":
                stock_name = input("\nEnter the stock name: ")
                stock_name = stockmarket.validate_symbol(stock_name)

            if option == "1" or option == "2":
                price = input("\nEnter price: ")
                price = stockmarket.convert_to_float(price)

            if option == "1":
                print("Dividend --> %s\n" % stockmarket.calculate_dividend(stock_name=stock_name, price=price))
            elif option == "2":
                print("P/E Ration --> %s\n" % stockmarket.calculate_pe_ration(stock_name=stock_name, price=price))
            elif option == "3":
                quantity = input("Enter quantity: ")
                quantity = stockmarket.convert_to_float(quantity)
                buy = input("Is to buy? Yes(y) or No(n)")
                buy = True if (buy == "y" or buy == "Y") else False
                stockmarket.add_record(stock_name=stock_name, quantity=quantity, buy=buy)
            elif option == "4":
                print("Volume: {}".format(stockmarket.calculate_volume_weighted(stock_name=stock_name)))
            elif option == "5":
                print("GBCE of all shares:  %s\n" % stockmarket.calculate_gbce())
            elif option == "6":
                running = False
            else:
                print("Invalid Entry")
        except (KeyError, ValueError, Exception) as error:
            if error.__class__.__name__ != 'ValueError':
                    print("Something went error.Please check log file for error details.")
                    logger.error(str(error))
                    logger.error(traceback.format_exc())
            else:
                print(error)