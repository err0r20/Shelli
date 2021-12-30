import os
import subprocess

def execute_command(command):
    try:
        if "|" in command:
            s_in, s_out = (0, 0)
            s_in = os.dup(0)
            s_out = os.dup(1)

            fdin = os.dup(s_in)

            for cmd in command.split("|"):
                os.dup2(fdin, 0)
                os.close(fdin)

                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print("Shelli: command not found: {}".format(cmd.strip()))

            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            subprocess.run(command.split(" "))
    except Exception:
        print("Shelli: command not found: {}".format(command))

def shelli_cd(path):
    """Change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))

def shelli_help():
    print("""\
        Usage: help

        help        Displays this message

        cd          Changes to a directory
        
        cat         Creates single or multiple files/view file content/redirects output
            """)

def main():
    while True:
        inp = input("$ ")
        if inp == "exit":
            break
        elif inp[:3] == "cd ":
            shelli_cd(inp[3:])
        elif inp == "help":
            shelli_help()
        else:
            execute_command(inp)

if '__main__' == __name__:
    main()
