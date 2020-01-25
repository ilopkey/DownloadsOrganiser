"""
Downloads Organiser

Author: Alex Clough

Allows the user to move files and folders from a specified directory
to different directories based on file types

"""
import os
import sys

def get_files(Directory):
    """
    Return 3 lists detailing all the Items in the given Directory
    
    Directory should be an Absolute Path
    
    If there are subdirectories, the files in the subdirectories will
    be returned with their relative path to Directory
    
    Also a list containing the absolute paths of the subdirectories and
    the number of items contained will be returned
    
    A third list containing any items in the directory that this
    code could not determine to be either a file, directory or link
    """
    
    
    # Set the CWD to Directory
    os.chdir(Directory)
    
    # Get the list of all items in Directory
    Directory_Items = os.listdir()
    
    # Store the PATHS of all files in the Directory and Subdirectories
    File_Paths = []
    Sub_Dirs = []
    Unknowns = []
    
    # Go through Directory_Items and get the paths of all files inside
    for Item in Directory_Items:
        
        # If the item is a Directory then get the number of items 
        # inside then append the Paths of the items inside to 
        # Directory_Items. 
        if os.path.isdir(Item):
            
            # Get the Absolute Path of the subdirectory
            Sub_Dir_Path = os.path.join(Directory, Item)
            
            # Get the items in the subdirectory
            Sub_Dir_Items = os.listdir(Sub_Dir_Path)
            
            # Change the Path of the Sub_Dir_Items to be relative
            # to Directory
            for Sub_Item_Pos in range(0, len(Sub_Dir_Items)):
                Sub_Dir_Items[Sub_Item_Pos] = os.path.join(
                                                Item,
                                                Sub_Dir_Items[Sub_Item_Pos]
                                                )
            
            # Add the previous 2 details to the Sub_Dirs list
            Sub_Dirs.append([Sub_Dir_Path, len(Sub_Dir_Items)])
            
            # Go through Sub_Dir_Items and add the items to 
            # Directory_Items, positioned after Item
            for Sub_Item_Pos in range(0, len(Sub_Dir_Items)):
                Directory_Items.insert(
                                       Directory_Items.index(Item)
                                       + Sub_Item_Pos
                                       + 1,
                                       Sub_Dir_Items[Sub_Item_Pos]
                                       )
        
        # If the item is a File then add it to File_Paths
        elif os.path.isfile(Item):
        
            File_Paths.append(Item)
        
        # If the item is neither a file or directory then it is
        # likely to be a link/shortcut. This nested if is to 
        # handle different OS links and other known Item types.
        else:
        
            # If this is a windows platform check if it is a shortcut
            # file ending in .lnk, treat this as any other file
            if sys.platform.startswith('win') and Item[4:] == '.lnk':
                
                File_Paths.append(Item)
                
            # Chceking for Linux Symbolic Links - In Progress
            elif sys.platform.startswith('linux'):
                # Code for processing linux symbolic links
                pass
            
            # If this code cannot detect what an item is then
            # add it to the Unknowns list
            else:
                Unknowns.append(Item)
    
    return File_Paths, Sub_Dirs, Unknowns


def get_file_types(File_Paths):
    """
    Return a dictionary linking File Types to the File Paths
    
    Each File Type shall be a new Key and given a list as it's value
    The list will then contain each File Path that has that File Type
    """
    
    
    # Dictionary for storing the File Types as Keys and the
    # corresponding Paths as Values in Lists
    File_Types_And_Paths = {}
    
    # Go through File_Paths and check the file type of each file path
    # If the file type is not already in File_Types_And_Paths then
    # add the file type as a new key with the file path in the list
    # If the file type is in File_Types_And_Paths then add the file path
    # to the list corresponding to the file type key
    for Path in File_Paths:
        
        # Get the position of the last . in the Path
        Type_Start = Path.rfind('.')
        
        # If no file type is found then create a key '' to refer to
        # these files
        if Type_Start == -1:
            if File_Types_And_Paths.get('') == None:
                File_Types_And_Paths[''] = [Path]
            else:
                File_Types_And_Paths[''].append(Path)
        
        else:
            
            # Get the file type
            Type = Path[Type_Start:]
            
            # Create a key if the file type has not already been
            # encountered, if it has then append it to the list
            if File_Types_And_Paths.get(Type) == None:
                File_Types_And_Paths[Type] = [Path]
            else:
                File_Types_And_Paths[Type].append(Path)
    
    return File_Types_And_Paths










# Testing Purposes
# Currently just prints to CMD line
# 
# This is being modified to write the information to a SQL based DB
# to allow for quicker and easier usage 
if __name__ == "__main__":
    Paths, Subs, Unknowns = get_files(input("Enter Directory Path: "))
    
    Types = get_file_types(Paths)
    
    Keys = Types.keys()
    
    print(Subs)
    
    print(Keys)
    for Key in Keys:
        print(Key, Types[Key])