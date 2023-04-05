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
        self.requirements = "Must be a parsable string"
    

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