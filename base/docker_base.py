import subprocess
import platform



def docker_call(command):
    return subprocess.call(command, shell=platform.system() != 'Windows')

def docker_run(task_name):
    command = 'docker run -d --name {} {}'.format(task_name, task_name)
    return subprocess.call(command, shell=platform.system() != 'Windows')

def docker_start(task_name):
    command = 'docker start {}'.format(task_name)
    return subprocess.call(command, shell=platform.system() != 'Windows')


def docker_stop(task_name):
    command = 'docker stop {}'.format(task_name)
    return subprocess.call(command, shell=platform.system() != 'Windows')


def docker_rm(task_name):
    command = 'docker rm {}'.format(task_name)
    return subprocess.call(command, shell=platform.system() != 'Windows')



if __name__ == '__main__':
    task_name = 'redis'
    print(docker_run(task_name))
    #docker_start(task_name)
    print(docker_stop(task_name))
    #print(docker_start(task_name))
    print(docker_rm(task_name))