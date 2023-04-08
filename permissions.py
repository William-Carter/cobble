import discord
ADMIN = 2
TRUSTED = 1
EVERYONE = 0

def getUserPermissionLevel(user: discord.user, adminList: list):
    """
    Gets the correct permission level for a user object
    Parameters:
        user - the user object to get the permission level of
        adminList - the list of administrator accounts
    """
    if  user.id in adminList:
        permissionLevel = ADMIN
    elif "Trusted" in [role.name for role in user.roles]:
        permissionLevel = TRUSTED
    else:
        permissionLevel = EVERYONE

    return permissionLevel