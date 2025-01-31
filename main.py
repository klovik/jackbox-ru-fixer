import os
import stat
import json

serverlist = [ "blobcast.jackboxgames.com", "ecast.jackboxgames.com", "ecast-qa.jackboxgames.com", "rujackbox.vercel.app", "jb-ecast.klucva.ru" ]

def update_server_url(folder_path, server):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('config.jet'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if isinstance(data, dict):
                        data['serverUrl'] = server

                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        print(f"fixed {file_path}")
                except PermissionError:
                    print(f"permission error: {file_path}, trying to change perms.")
                    try:
                        os.chmod(file_path, stat.S_IWUSR)
                        with open(file_path, 'r+', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, dict):
                                data['serverUrl'] = server
                                f.seek(0)
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                f.truncate()
                        print(f"reverted {file_path}")
                    except Exception as e:
                        print(f"failed {file_path}: {e}")
                except (json.JSONDecodeError, IOError):
                    print(f"skipping {file_path}")
    print("done")

def main():
    os.system("cls")
    path = input("Game path: ")
    s = ""
    last = 1
    for server in enumerate(serverlist):
        s += f"[{server[0]+1}] {server[1]}\n"
        last = server[0]+1
    s += f"[{last+1}] custom\n"

    sel = input(f"Select a server:\n{s}")
    if sel == str(last+1):
        server = input("Server: ")
        update_server_url(path, server)
    else:
        update_server_url(path, serverlist[int(sel)-1])

if __name__ == "__main__":
    main()