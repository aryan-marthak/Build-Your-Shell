import sys
import os
import subprocess
import readline
import shlex

builtin = ["echo", "type", "exit", "pwd", "cd"]
last_text = ""

def longest_common_prefix(words):
    if not words:
        return ""
    
    prefix = words[0]
    
    for i in range(len(prefix)):
        for word in words:
            if i == len(word) or word[i] != prefix[i]:
                return prefix[:i]
    
    return prefix

# HOW SHLEX WORKS 

# def parse_command(s):
#     result = []
#     current = ""
#     in_quotes = False

#     for ch in s:
#         if ch == "'":
#             in_quotes = not in_quotes

#         elif ch == " " and not in_quotes:
#             if current:
#                 result.append(current)
#                 current = ""

#         else:
#             current += ch

#     if current:
#         result.append(current)

#     return result

def completer(text, curr):
    global last_text
    buffer = readline.get_line_buffer()
    tokens = buffer.split()
    
    if len(tokens) == 0 or (len(tokens) == 1 and not buffer.endswith(" ")):
        cmds = []
        path_env = os.environ.get("PATH", "")

        for i in builtin:
            cmds.append(i)

        for path in path_env.split(os.pathsep):
            if not os.path.isdir(path):
                continue
            
            for file in os.listdir(path):
                full_path = os.path.join(path, file)

                if os.access(full_path, os.X_OK):
                    cmds.append(file)

        matches = []
        for i in cmds:
            if i.startswith(text):
                matches.append(i)   

        matches = sorted(set(matches))
    
    else:
        if "/" in text:
            dir_path, file_name = text.rsplit("/", 1)
            if dir_path == "":
                dir_path = "."
            try:
                files = os.listdir(dir_path)
            except FileNotFoundError:
                return None
            matches = []
            for i in files:
                if i.startswith(file_name):
                    matches.append(text[:len(text) - len(file_name)] + i)
            matches = sorted(set(matches))
        
        else:
            files = os.listdir(".")
            matches = []
            for i in files:
                if i.startswith(text):
                    matches.append(i)
            matches = sorted(set(matches))
        
    if len(matches) == 0:
        sys.stdout.write("\x07")
        sys.stdout.flush()
        return None
    
    if len(matches) == 1:
        last_text = ""
        if "/" in matches[0]:
            full_path = matches[0]
        else:
            full_path = os.path.join(".", matches[0])
        if curr == 0:
            if os.path.isdir(full_path):
                return matches[0] + "/"
            else:
                return matches[0] + " "
        return None
    
    if len(matches) > 1:
        lcp = longest_common_prefix(matches)
        if len(lcp) > len(text):
            last_text = ""
            completion = lcp
            if curr == 0:
                return completion
            return None
        
        if last_text != text:
            last_text = text
            sys.stdout.write("\x07")
            sys.stdout.flush()
            return None
        
        if curr == 0:
            sys.stdout.write("\n")
            total_matches = []
            for i in matches:
                if os.path.isdir(i):
                    total_matches.append(i + "/")
                else:
                    total_matches.append(i)
            sys.stdout.write("  ".join(total_matches) + "\n")
            sys.stdout.write("$ " + buffer)
            sys.stdout.flush()
            
        return None
    
    return matches[0] + " "

readline.set_completer(completer)
readline.set_completer_delims(" \t\n")
readline.parse_and_bind("tab: complete")

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        
        # parts = parse_command(s)
        parts = shlex.split(command)
        if not parts:
            continue
        
        out = None
        err = None
        append = False
        for i, v in enumerate(parts):
            if v in (">", "1>"):
                out = parts[i + 1]
                parts = parts[:i]
                break
            
            elif v in ("2>"):
                err = parts[i + 1]
                parts = parts[:i]
                break
            
            elif v in (">>", "1>>"):
                out = parts[i + 1]
                parts = parts[:i]
                append = True
                break
            
            elif v in ("2>>"):
                err = parts[i + 1]
                parts = parts[:i]
                append = True
                break
        
        output_stream = None
        error_stream = None
        
        if out:
            if append:
                output_stream = open(out, "a")
            else:
                output_stream = open(out, "w")
        else:
            output_stream = sys.stdout
        
        if err:
            if append:
                error_stream = open(err, "a")
            else:
                error_stream = open(err, "w")
        else:
            error_stream = sys.stderr
        
        func = parts[0]
        arg = parts[1:]
        
        if "|" in command:
            left, right = command.split("|", 1)
            left_parts = shlex.split(left.strip())
            right_parts = shlex.split(right.strip())
            
            p1 = subprocess.Popen(left_parts, stdout=subprocess.PIPE, stderr=error_stream)
            
            if right_parts[0] in builtin:
                p1.stdout.close()
                p1.wait()
                func = right_parts[0]
                args = right_parts[1:]
                
                if func == "exit":
                    break
        
                elif func == "echo":
                    output_stream.write(" ".join(args) + "\n")
        
        
                elif func == "pwd":
                    output_stream.write(os.getcwd() + "\n")
            
                elif func == "cd":
                    if not args:
                        continue
                    
                    path = arg[0]
                    if os.path.isdir(path):
                        os.chdir(path)
                    elif path == "~":
                        home = os.getenv("HOME")
                        os.chdir(home)
                    else:
                        error_stream.write(f"cd: {path}: No such file or directory \n")

                elif func == "type":
                    if not args:
                        continue
                    
                    if args[0] in builtin:
                        output_stream.write(f"{args[0]} is a shell builtin \n")

                    else:
                        path_env = os.environ.get("PATH", "")

                        for i in path_env.split(os.pathsep):
                            full_path = os.path.join(i, args[0])

                            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                                output_stream.write(f"{args[0]} is {full_path} \n")
                                break
                        else:
                            error_stream.write(f"{args[0]}: not found \n")
            
            else:
                p2 = subprocess.Popen(right_parts, stdin=p1.stdout, stdout=output_stream, stderr=error_stream)
                p1.stdout.close()
                p2.communicate()
                continue

        elif func == "exit":
            break
        
        elif func == "echo":
            output_stream.write(" ".join(arg) + "\n")
        
        
        elif func == "pwd":
            output_stream.write(os.getcwd() + "\n")
            
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
                error_stream.write(f"cd: {path}: No such file or directory \n")

        elif func == "type":
            if not arg:
                continue
            
            if arg[0] in builtin:
                output_stream.write(f"{arg[0]} is a shell builtin \n")
            
            else:
                path_env = os.environ.get("PATH", "")
                
                for i in path_env.split(os.pathsep):
                    full_path = os.path.join(i, arg[0])
                
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        output_stream.write(f"{arg[0]} is {full_path} \n")
                        break
                else:
                    error_stream.write(f"{arg[0]}: not found \n")
                    
        else:
            path_env = os.environ.get("PATH", "")
            for i in path_env.split(os.pathsep):
                full_path = os.path.join(i, func)
                
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    subprocess.run([func] + arg, executable=full_path, stdout = output_stream, stderr = error_stream)
                    break
            else:
                error_stream.write(f"{func}: command not found \n")
        
        if out:
            output_stream.close()


if __name__ == "__main__":
    main()
    