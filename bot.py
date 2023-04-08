import cobble.command
import json
import discord
class Bot:
    def __init__(self, configFilePath: str, name: str, prefix: str = "."):
        self.loadConfig(configFilePath)
        self.name = name
        self.prefix = prefix
        self.commands = []

    def addCommand(self, command: cobble.command.Command):
        """
        Add a command to the bot
        Parameters:
            command - A preconfigured Command object
        """
        self.commands.append(command)

    def loadConfig(self, configFilePath: str) -> None:
            """
            Load sensitive bot data from a config file
            Parameters:
                configFilePath - A path to a .json file containing the relevant data
            """
            with open(configFilePath, "r") as f:
                config = json.load(f)
                self.token = config["token"]
                self.admins = config["admins"]


    def processCommand(self, messageObject: discord.message, fullString: str, senderPermissionLevel = 0) -> str:
        """
        Process a received command
        Parameters:
            fullString - the entire command string, as inputted by the user, excluding the prefix
        Returns:
            response - the response to be sent back to the user either containing the requested information, or just as confirmation.
        """
        
        # Ensure the command exists
        processedCommand = None
        trigger = fullString.split(" ")[0]
        for command in self.commands:
            if trigger == command.trigger:
                processedCommand = command

        if processedCommand == None:
            return f"Command \"{trigger}\" unknown!"
        
        if senderPermissionLevel < processedCommand.permissionLevel:
            return f"User is not authorised to use this command!"
        
        # We want to not split on spaces that are inside quotation marks, so we'll keep track of whether we're currently inside a quote block
        inQuotes = False

        commandElements = []
        element = ""
        for character in fullString:
            match character:
                case '"':
                    inQuotes = not inQuotes
                case " ":
                    if not inQuotes:
                        if not element == "":
                            commandElements.append(element)
                        element = ""

                    else:
                        element += character
                case _:
                    element += character

        if not element == "":
            commandElements.append(element)

        commandElements.pop(0)


        if len(commandElements) > len(processedCommand.arguments):
            return f"Too many arguments supplied!\n{processedCommand.name} takes up to {len(processedCommand.arguments)}, but {len(commandElements)} were supplied!"
        

        argumentValues = {}


        if len(commandElements) < len(processedCommand.mandatoryArgs):
            return f"Not enough arguments supplied!\n{processedCommand.name} takes at least {len(processedCommand.mandatoryArgs)}, but {len(commandElements)} were supplied!"

        for index, arg in enumerate(processedCommand.mandatoryArgs):
            if arg.validation.validate(commandElements[index]):
                argumentValues[arg.name] = commandElements[index]

            else:
                return f"{commandElements[index]} is not a valid value for {arg.name}! {arg.validation.requirements}!"

        mandatoryArgsOffset = len(processedCommand.mandatoryArgs)
        for i in range(len(commandElements)-mandatoryArgsOffset):
            currentElement = commandElements[i+mandatoryArgsOffset]
            if not "=" in currentElement:
                return f"Argument with value '{currentElement}' needs to be a keyword argument!"
            else:
                key = currentElement.split("=")[0]
                if not key in [arg.name for arg in processedCommand.keywordArgs]:
                    return f"Unknown argument: {key}"
                else:
                    for arg in processedCommand.keywordArgs:
                        if key == arg.name:
                            identifiedArgument = arg
                value = currentElement.split("=")[1]
                if identifiedArgument.validation.validate(value):
                    argumentValues[key] = value
                else:
                    return f"{value} is not a valid value for {key}! {identifiedArgument.validation.requirements}!"



        response = processedCommand.execute(messageObject, argumentValues)
        return response
                        



        
        


