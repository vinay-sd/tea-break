import paramiko
import sys
import time

def ssh_exec(command, host='64.227.188.196', user='root', password='@Astro#123SD', timeout=30):
    """Execute a command on remote server via SSH"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password, timeout=10)
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        exit_code = stdout.channel.recv_exit_status()
        if out:
            print(out)
        if err:
            print(f"STDERR: {err}")
        print(f"[Exit: {exit_code}]")
        return out, err, exit_code
    except Exception as e:
        print(f"ERROR: {e}")
        return '', str(e), 1
    finally:
        client.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        ssh_exec(cmd)
    else:
        print("Usage: python ssh_helper.py <command>")
