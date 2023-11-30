import discord
import json

def getUserPermissions(userID: str, permissionsPath: str) -> list[str]:
    """
    Returns a list of permissions a user has been granted

    Parameters:
        userID - the user's discord ID, as a string

        permissionPath - the path to the file containing permissions
    """
    with open(permissionsPath, "r") as f:
        perms = json.load(f)

    if not userID in perms["users"]: # For users who aren't in the permissions file
        return []
    
    return perms["users"][userID]


def getPermissionList(permissionsPath: str) -> list[str]:
    """
    Returns a list of all permissions

    Parameters:
        permissionPath - the path to the file containing permissions
    """

    with open(permissionsPath, "r") as f:
        perms = json.load(f)

    return perms["permissions"].keys()


def addUserPermission(userID: str, permission: str, permissionsPath: str):
    """
    Grant a permission to a user.

    Does not check existence of permission before writing.

    Parameters:
        userID - the user's discord ID, as a string

        permission - the permission

        permissionPath - the path to the file containing permissions
    """

    with open(permissionsPath, "r") as f:
        perms = json.load(f)

    if not userID in perms["users"].keys():
        perms["users"][userID] = []

    if not permission in perms["users"][userID]:
        perms["users"][userID].append(permission)

        with open(permissionsPath, "w") as f:
            json.dump(perms, f)

def removeUserPermission(userID: str, permission: str, permissionsPath: str):
    """
    Revoke a permission from the user

    Does not check existence of permission before writing.

    Parameters:
        userID - the user's discord ID, as a string

        permission - the permission

        permissionsPath - the path to the file containing permissions
    """

    with open(permissionsPath, "r") as f:
        perms = json.load(f)

    if not userID in perms["users"].keys():
        return

    perms["users"][userID].remove(permission)

    with open(permissionsPath, "w") as f:
        json.dump(perms, f)


def getPermissionNames(permissionsPath: str) -> dict[str, dict[str, str]]:
    """
    Gets the full permission dictionary

    Parameters:
        permissionsPath - the path to the file containing permissions

    Returns:
        The full permissions dictionary
    
    """
    
    with open(permissionsPath, "r") as f:
        perms = json.load(f)

    return perms["permissions"]