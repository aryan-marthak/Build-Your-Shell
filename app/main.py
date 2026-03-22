import sys
import os
import subprocess

builtin = ["echo", "type", "exit"]

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        func = command.split()[0]
        arg = command.split()[1:]
        
        if func == "exit":
            break
        
        elif func == "echo":
            sys.stdout.write(" ".join(arg) + "\n")
        
        elif func == "pwd":
            sys.stdout.write(os.getcwd() + "\n")

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
    