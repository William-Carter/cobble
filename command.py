import cobble.validations
import cobble.permissions
import cobble.bot
import discord

class Argument:
    def __init__(self, name: str, description: str, validation: cobble.validations.Validation, keywordArg: bool = False) -> None:
        """
        Parameters: 
            name - the name of the argument, to be used when addressing the user, such as in help menus
            description - a description of the argument, to be used when addressing the user
            validation - rules to enforce
            mandatory - whether the argument is required for the command to run
            keywordArg - whether the argument should be passed as a keyword i.e. "argument=foo"
        """
        self.name = name
        self.description = description
        self.validation = validation
        self.keywordArg = keywordArg


class FileArgument:
    def __init__(self, name: str, description: str, fileType: str) -> None:
        """
        Parameters: 
            name - the name of the argument, to be used when addressing the user, such as in help menus
            description - a description of the argument, to be used when addressing the user
            validation - rules to enforce
        """
        self.name = name
        self.description = description
        self.fileType = fileType



class Command:
    def __init__(self, bot: "cobble.bot.Bot", name: str, trigger: str, description: str, permissionLevel: int = 0) -> None:
        """
        Parameters:
            bot - The bot object the command will belong to
            name - the name of the command, to be used when addressing the user, such as in help menus
            trigger - the phrase used to activate the command, usually with a set prefix i.e "help"
            permissionLevel - the authorisation a user is required to have in order to use this command.
        """
        self.bot = bot
        self.name = name
        self.trigger = trigger
        self.description = description
        self.permissionLevel = permissionLevel
        self.arguments = []
        self.fileArguments = []
        self.mandatoryArgs = []
        self.keywordArgs = []


    def addArgument(self, argument: Argument):
        """
        Add an argument to the command
        Parameters:
            argument - A preconfigured argument object
        """
        self.arguments.append(argument)

        if not argument.keywordArg:
            self.mandatoryArgs.append(argument)
        else:
            self.keywordArgs.append(argument)

    def addFileArgument(self, argument: FileArgument):
        """
        Add a file argument to the command
        Parameters:
            argument - A preconfigured FileArgument object
        """
        self.fileArguments.append(argument)

    



class HelpCommand(Command):
    def __init__(self, bot: "cobble.bot.Bot"):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, "Help", "help", "Get help with any commands", cobble.permissions.EVERYONE)
        self.addArgument(Argument("command", "The command you wish to know more about", cobble.validations.IsCommand(self.bot.commands), True))


    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> None:
        """
        Generate a help menu for a given command
        Parameters:
            argumentValues - a dictionary containing values for every argument provided, keyed to the argument name
        """
        if not "command" in argumentValues:
            return await ListCommand.execute(self, messageObject, argumentValues, attachedFiles)

        for command in self.bot.commands:
            if argumentValues["command"] == command.trigger:
                commandToUse = command
                break

    
        finalOutput = ""

        finalOutput += f"Help for {commandToUse.name}:\n"
        usage = f"`{self.bot.prefix}{commandToUse.trigger}"
        
        for argument in commandToUse.arguments:
            usage += " "
            if not argument.keywordArg:
                argText = argument.name
            else:
                argText = f"{argument.name}=[value]"

            usage += argText



        finalOutput += usage+"`"


        for argument in commandToUse.arguments:
            finalOutput += "\n"
            finalOutput += f"{argument.name} - {argument.description}, {argument.validation.requirements}"


        if len(commandToUse.fileArguments) > 0:
            finalOutput += "\n\nFile Arguments:"
            for fileArgument in commandToUse.fileArguments:
                finalOutput += "\n"
                finalOutput += f"{fileArgument.name} - {fileArgument.description}, Must be of type {fileArgument.fileType}"

        return finalOutput
            

            

        
class ListCommand(Command):
    def __init__(self, bot: "cobble.bot.Bot"):
        """
        Parameters:
            bot - The bot object the command will belong to
        """
        super().__init__(bot, "List", "list", "List every command available to you", cobble.permissions.EVERYONE)


    async def execute(self, messageObject: discord.message, argumentValues: dict, attachedFiles: dict) -> None:
        """
        Generate a help menu for a given command
        Parameters:
            argumentValues - a dictionary containing values for every argument provided, keyed to the argument name
        """
        output = "Available commands:"
        for command in self.bot.commands:
            if cobble.permissions.getUserPermissionLevel(messageObject.author, self.bot.admins) >= command.permissionLevel:
                output += f"\n`{command.trigger}` - {command.description}"


        output += "\n\nUse the help command for more information on any command"

        return output