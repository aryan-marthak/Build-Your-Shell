import sys
import os
import subprocess
import shlex

builtin = ["echo", "type", "exit", "pwd"]

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        
        parts = shlex.split(command)
        if not parts:
            continue
        
        func = parts[0]
        arg = parts[1:]
        
        if func == "exit":
            break
        
        elif func == "echo":
            sys.stdout.write(" ".join(arg) + "\n")
        
        elif func == "pwd":
            sys.stdout.write(os.getcwd() + "\n")
            
        elif func == "cd":
            if not arg:
                continue
            
            path = arg[0]
            if os.path.isdir(path):
                os.chdir(path)
            elif path == "~":
                home = os.getenv("HOME")
                os.chdir(home)
            else:
                sys.stdout.write(f"cd: {path}: No such file or directory \n")

        elif func == "type":
            if not arg:
                continue
            
            if arg[0] in builtin:
                sys.stdout.write(f"{arg[0]} is a shell builtin \n")
            
            else:
                path_env = os.environ.get("PATH", "")
                
                for i in path_env.split(os.pathsep):
                    full_path = os.path.join(i, arg[0])
                
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        sys.stdout.write(f"{arg[0]} is {full_path} \n")
                        break
                else:
                    sys.stdout.write(f"{arg[0]}: not found \n")
                    
        else:
            path_env = os.environ.get("PATH", "")
            for i in path_env.split(os.pathsep):
                full_path = os.path.join(i, func)
                
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    subprocess.run([func] + arg, executable=full_path)
                    break
            else:
                sys.stdout.write(f"{func}: command not found \n")


if __name__ == "__main__":
    main()
    