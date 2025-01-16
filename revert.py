import os
import stat
import json

def update_server_url(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('config.jet'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if isinstance(data, dict):
                        data['serverUrl'] = 'ecast.jackboxgames.com'

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
                                data['serverUrl'] = 'ecast-qa.jackboxgames.com'
                                f.seek(0)
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                f.truncate()
                        print(f"reverted {file_path}")
                    except Exception as e:
                        print(f"failed {file_path}: {e}")
                except (json.JSONDecodeError, IOError):
                    print(f"skipping {file_path}")
    print("done")

if __name__ == "__main__":
    folder_path = input("path: ")
    update_server_url(folder_path)