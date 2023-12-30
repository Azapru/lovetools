import sys
import requests
from tqdm import tqdm
import shutil
import os

def download_file(url, dest_filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    t = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(dest_filename, 'wb') as file, tqdm(
        desc=dest_filename,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        miniters=1,
        ncols=100,
    ) as bar:
        for data in response.iter_content(block_size):
            t.update(len(data))
            bar.update(len(data))
            file.write(data)

    t.close()

def help():
    print("lovetools - a small tool set for an *awesome* framework, LÖVE!\n")
    print("help\t\t\t\tDisplays this help message.")
    print("version\t\t\t\tDisplays lovetools version.")
    print("project setup\t\t\tSetups LÖVE project in current directory.")
    print("project setup [version]\t\tSetups LÖVE project in current directory with specified LÖVE version. (Might need manual fixes)")
    print("project run\t\t\tRuns this LÖVE project, works only on projects setup by lovetools.")

def version():
    print("lovetools v0.2.0stable | Python "+str(sys.version))

def project_setup(loveVer):
    print("lovetools - Setting up LÖVE project in the current directory.\n")
    print(f"Collecting LÖVE package... [https://github.com/love2d/love/releases/download/{loveVer}/love-{loveVer}-win64.zip]")

    download_file(f"https://github.com/love2d/love/releases/download/{loveVer}/love-{loveVer}-win64.zip", f"love-{loveVer}-win64.zip")

    # Unpack archive
    print("Unpacking package...")
    shutil.unpack_archive(f"love-{loveVer}-win64.zip", "runtime")

    # Remove downloaded archive
    print("Cleaning up...")
    try:
        os.remove(f"love-{loveVer}-win64.zip")
    except FileNotFoundError:
        print("File not found. Is it gone already?")
    
    # Set default runtime version
    print(f"Setting default runtime version to \"love-{loveVer}-win64\"")
    with open("runtime\\defaultRuntime.txt", "w") as file:
        file.write(f"love-{loveVer}-win64")

    # Create main.lua
    if not os.path.exists("main.lua"):
        with open("main.lua", "w") as file:
            file.write("function love.load()\n\t\nend\n\nfunction love.update(dt)\n\t\nend\n\nfunction love.draw()\n\t\nend") # wtf

    print("Finished!")

def project_run():
    with open("runtime\\defaultRuntime.txt", 'r') as file:
        runtimeVer = file.read()
    os.system(f"runtime\\{runtimeVer}\\lovec.exe .")

def main():
    if sys.argv[1:] == []:
        help() # Execute help command if no args
    else:
        if sys.argv[1] == "help":
            help()
        elif sys.argv[1] == "version":
            version()
        elif sys.argv[1] == "project" and sys.argv[2] == "setup" and sys.argv[3:] == []:
            project_setup("11.5")
        elif sys.argv[1] == "project" and sys.argv[2] == "setup" and sys.argv[3:] != []:
            project_setup(sys.argv[3])
        elif sys.argv[1] == "project" and sys.argv[2] == "run":
            project_run()
        else:
            print("ERROR: Incorrect command!")

if __name__ == "__main__":
    main()