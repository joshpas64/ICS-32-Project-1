from pathlib import Path
import os
import shutil
def excep_handle(total_files_nested: [Path]) -> [Path]:
    """Exception handling function for when the second input of master_program fails, will retake the input and recall the function"""
    print("ERROR")
    prompt = input()
    promptList = prompt.split()
    mode = promptList[0]
    key = promptList[1]
    return file_filter(mode, key, total_files_nested)
def file_search(u_path:str) -> [Path]:
    """ Search all files and directories and subdirectories for available files"""
    file_list = []
    n_path = Path(u_path)
    if n_path.exists() == False:
        print("ERROR")
        master_program()
        return
    if n_path.is_file():
        file_list.append(n_path)
    elif n_path.is_dir():
        for item in n_path.iterdir():
            try:
                file_list = file_list + file_search(Path(item))
            except PermissionError:
                pass
    return file_list   
        
def file_filter(mode: str, name: str, total_files: [Path]) -> [Path]:
    """ Iterate through file list and returned specific files based on command"""
    filtered_list = []
    if mode == "N":
        for paths in total_files:
            if paths.name == name:
                filtered_list.append(paths)
    elif mode == "E":
        if name[0] != ".":
            name = "." + name
        for paths in total_files:
            if paths.suffix == name:
                filtered_list.append(paths)
    elif mode == "S":
        try:
            mem_size = int(name)
            for paths in total_files:
                try:
                    if paths.stat().st_size > mem_size:
                        filtered_list.append(paths)
                except PermissionError:
                   pass
        except ValueError:
                new_List = excep_handle(total_files)
                return new_List
    
    else:
        new_list = excep_handle(total_files)
        return new_list
    return filtered_list
def file_action(mode: str, flist: list) -> None:
    """Prints file path and makes a duplicate or reads the first line of file, if posssible"""
    for f_path in flist:
        file1 = None
        try:
            if mode == "P":
                print(f_path)
            elif mode == "F":
                file1 = f_path.open()
                lin1 = file1.readline()
                print(f_path)
                print(lin1)
                file1.close()
            elif mode == "D":
                print(f_path)
                new_path = str(f_path) + ".dup"
                shutil.copyfile(str(f_path),new_path)
            elif mode == "T":
                print(f_path)
                f_path.touch()
            else:
                print("ERROR")
                prompt = input()
                file_action(prompt, flist)
                return
        except PermissionError:
            pass
            
        except OSError:
           pass
            
        except FileExistsError:
            pass
            
        finally:
            if file1 != None:
                file1.close()
            

def master_program() -> None:
    """ Main interface of the file sorting program that runs through the full sequence of commmands """
    try:
        path_read = input()
        flist = file_search(path_read)
        opt1_parsed = input()
        command1 = opt1_parsed[0]
        search_key = opt1_parsed[2:]
        f2list = file_filter(command1,search_key,flist)
        command3 = input()
        file_action(command3,f2list)
    except IndexError:
        print("ERROR")
        opt1_parsed = input()
        command1 = opt1_parsed[0]
        search_key = opt1_parsed[2:]
        f2list = file_filter(command1,search_key,flist)
        command3 = input()
        file_action(command3,f2list)
    except:
        print("ERROR")
        master_program()
#
        
        
if __name__ == '__main__': 
    master_program()
