import datetime
class Validation:
    def __init__(self) -> None:
        """
        Input validation
        """
        self.requirements = ""

    def validate(self, x):
        return True



class IsString(Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a string
        """
        super().__init__()
        self.requirements = "Must be a parseable string"
    

    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid string
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid string, False otherwise
        """
        try:
            str(x)
        except:
            return False
        else:
            return True
        

class IsCommand(Validation):
    def __init__(self, commandList) -> None:
        """
        Validate that an input is in the list of commands
        """
        super().__init__()
        self.requirements = "Must be in the command list"
        self.commandList = commandList
    

    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is in the command list
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid string, False otherwise
        """
        return (x in [command.trigger for command in self.commandList])


class IsInteger(Validation):
    def __init__(self) -> None:
        """
        Validate that an input is an integer
        """
        self.requirements = "Must be a valid integer"
    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid integer
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid integer, False otherwise
        """
        try:
            inted = int(x)
        except:
            return False
        else:
            floated = float(x)
            return float(inted) == floated
        


class IsISO8601(Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a valid ISO8601 datestring
        """
        self.requirements = "Must be a datestring formatted as YYYY-MM-DD"

    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid ISO8601 date string
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid date string, False otherwise
        """
        dateFormat = "%Y-%m-%d"

        try:
            datetime.datetime.strptime(x, dateFormat)
        except:
            return False
        else:
            return True
        
class IsNumber(Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a number
        """
        self.requirements = "Must be a real number"

    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid number
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid number, False otherwise
        """

        try:
            numericalValue = float(x)
        except:
            return False
        else:
            return True

class IsPositive(Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a positive number
        """
        self.requirements = "Must be greater than or equal to 0"

    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid ISO8601 date string
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid date string, False otherwise
        """

        try:
            numericalValue = float(x)
        except:
            return False
        else:
            return (numericalValue >= 0)
        


class IsBool(Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a valid ISO8601 datestring
        """
        self.requirements = "Must be either true or false"

    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid ISO8601 date string
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid bool, False otherwise
        """
        if x in ["true", "false"]:
            return True
        return False