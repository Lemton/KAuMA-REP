class ArithmeticHandler: 

    @staticmethod
    def add_numbers(arguments):
        number1 = arguments.get("number1", 0)
        number2 = arguments.get("number2", 0)
        return {"sum": number1 + number2}
    
    @staticmethod
    def subtract_numbers(arguments):
        number1 = arguments.get("number1", 0)
        number2 = arguments.get("number2", 0)
        return {"difference": number1 - number2}
    
    