"""
vmrun version 1.15.2 build-3272444

Usage: vmrun [AUTHENTICATION-FLAGS] COMMAND [PARAMETERS]



AUTHENTICATION-FLAGS
--------------------
These must appear before the command and any command parameters.

   -h <hostName>  (not needed for Workstation)
   -P <hostPort>  (not needed for Workstation)
   -T <hostType> (ws|server|server1|fusion|esx|vc|player)
     for example, use '-T server' for Server 2.0
                  use '-T server1' for Server 1.0
                  use '-T ws' for VMware Workstation
                  use '-T ws-shared' for VMware Workstation (shared mode)
                  use '-T esx' for VMware ESX
                  use '-T vc' for VMware vCenter Server
   -u <userName in host OS>  (not needed for Workstation)
   -p <password in host OS>  (not needed for Workstation)
   -vp <password for encrypted virtual machine>
   -gu <userName in guest OS>
   -gp <password in guest OS>



POWER COMMANDS           PARAMETERS           DESCRIPTION
--------------           ----------           -----------
start                    Path to vmx file     Start a VM or Team
                         [gui|nogui]

stop                     Path to vmx file     Stop a VM or Team
                         [hard|soft]

reset                    Path to vmx file     Reset a VM or Team
                         [hard|soft]

suspend                  Path to vmx file     Suspend a VM or Team
                         [hard|soft]

pause                    Path to vmx file     Pause a VM

unpause                  Path to vmx file     Unpause a VM



SNAPSHOT COMMANDS        PARAMETERS           DESCRIPTION
-----------------        ----------           -----------
listSnapshots            Path to vmx file     List all snapshots in a VM
                         [showTree]

snapshot                 Path to vmx file     Create a snapshot of a VM
                         Snapshot name

deleteSnapshot           Path to vmx file     Remove a snapshot from a VM
                         Snapshot name
                         [andDeleteChildren]

revertToSnapshot         Path to vmx file     Set VM state to a snapshot
                         Snapshot name



GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
-----------------        ----------           -----------
runProgramInGuest        Path to vmx file     Run a program in Guest OS
                         [-noWait]
                         [-activeWindow]
                         [-interactive]
                         Complete-Path-To-Program
                         [Program arguments]

fileExistsInGuest        Path to vmx file     Check if a file exists in Guest OS
                         Path to file in guest

directoryExistsInGuest   Path to vmx file     Check if a directory exists in Guest OS
                         Path to directory in guest

setSharedFolderState     Path to vmx file     Modify a Host-Guest shared folder
                         Share name
                         Host path
                         writable | readonly

addSharedFolder          Path to vmx file     Add a Host-Guest shared folder
                         Share name
                         New host path

removeSharedFolder       Path to vmx file     Remove a Host-Guest shared folder
                         Share name

enableSharedFolders      Path to vmx file     Enable shared folders in Guest
                         [runtime]

disableSharedFolders     Path to vmx file     Disable shared folders in Guest
                         [runtime]

listProcessesInGuest     Path to vmx file     List running processes in Guest OS

killProcessInGuest       Path to vmx file     Kill a process in Guest OS
                         process id

runScriptInGuest         Path to vmx file     Run a script in Guest OS
                         [-noWait]
                         [-activeWindow]
                         [-interactive]
                         Interpreter path
                         Script text

deleteFileInGuest        Path to vmx file     Delete a file in Guest OS
Path in guest

createDirectoryInGuest   Path to vmx file     Create a directory in Guest OS
Directory path in guest

deleteDirectoryInGuest   Path to vmx file     Delete a directory in Guest OS
Directory path in guest

CreateTempfileInGuest    Path to vmx file     Create a temporary file in Guest OS

listDirectoryInGuest     Path to vmx file     List a directory in Guest OS
                         Directory path in guest

CopyFileFromHostToGuest  Path to vmx file     Copy a file from host OS to guest OS
Path on host             Path in guest


CopyFileFromGuestToHost  Path to vmx file     Copy a file from guest OS to host OS
Path in guest            Path on host


renameFileInGuest        Path to vmx file     Rename a file in Guest OS
                         Original name
                         New name

captureScreen            Path to vmx file     Capture the screen of the VM to a local file
Path on host

writeVariable            Path to vmx file     Write a variable in the VM state
                         [runtimeConfig|guestEnv|guestVar]
                         variable name
                         variable value

readVariable             Path to vmx file     Read a variable in the VM state
                         [runtimeConfig|guestEnv|guestVar]
                         variable name

getGuestIPAddress        Path to vmx file     Gets the IP address of the guest
                         [-wait]



GENERAL COMMANDS         PARAMETERS           DESCRIPTION
----------------         ----------           -----------
list                                          List all running VMs

upgradevm                Path to vmx file     Upgrade VM file format, virtual hw

installTools             Path to vmx file     Install Tools in Guest

checkToolsState          Path to vmx file     Check the current Tools state

register                 Path to vmx file     Register a VM

unregister               Path to vmx file     Unregister a VM

listRegisteredVM                              List registered VMs

deleteVM                 Path to vmx file     Delete a VM

clone                    Path to vmx file     Create a copy of the VM
                         Path to destination vmx file
                         full|linked
                         [-snapshot=Snapshot Name]
                         [-cloneName=Name]




Examples:


Starting a virtual machine with Workstation on a Windows host
   vmrun -T ws start "c:\my VMs\myVM.vmx"


Stopping a virtual machine on an ESX host
   vmrun -T esx -h https://myHost.com/sdk -u hostUser -p hostPassword stop "[storage1] vm/myVM.vmx"


Running a program in a virtual machine with Workstation on a Windows host with Windows guest
   vmrun -T ws -gu guestUser -gp guestPassword runProgramInGuest "c:\my VMs\myVM.vmx" "c:\Program Files\myProgram.exe"


Running a program in a virtual machine with Server on a Linux host with Linux guest
   vmrun -T server -h https://myHost.com:8333/sdk -u hostUser -p hostPassword -gu guestUser -gp guestPassword runProgramInGuest "[standard] vm/myVM.vmx" /usr/bin/X11/xclock -display :0


Creating a snapshot of a virtual machine with Workstation on a Windows host
   vmrun -T ws snapshot "c:\my VMs\myVM.vmx" mySnapshot


Reverting to a snapshot with Workstation on a Windows host
   vmrun -T ws revertToSnapshot "c:\my VMs\myVM.vmx" mySnapshot


Deleting a snapshot with Workstation on a Windows host
   vmrun -T ws deleteSnapshot "c:\my VMs\myVM.vmx" mySnapshot


Enabling Shared Folders with Workstation on a Windows host
   vmrun -T ws enableSharedFolders "c:\my VMs\myVM.vmx"

"""

__author__ = 'huangyu'
from fabric.api import *
import subprocess
import sys


def _authentication_flags(**kwargs):
    """
    AUTHENTICATION-FLAGS
    --------------------
    These must appear before the command and any command parameters.

       -h <hostName>  (not needed for Workstation)
       -P <hostPort>  (not needed for Workstation)
       -T <hostType> (ws|server|server1|fusion|esx|vc|player)
         for example, use '-T server' for Server 2.0
                      use '-T server1' for Server 1.0
                      use '-T ws' for VMware Workstation
                      use '-T ws-shared' for VMware Workstation (shared mode)
                      use '-T esx' for VMware ESX
                      use '-T vc' for VMware vCenter Server
       -u <userName in host OS>  (not needed for Workstation)
       -p <password in host OS>  (not needed for Workstation)
       -vp <password for encrypted virtual machine>
       -gu <userName in guest OS>
       -gp <password in guest OS>

    :return: cmd str
    """
    host_name = kwargs.get('host_name')
    host_port = kwargs.get('host_port')
    host_type = kwargs.get('host_type')
    host_user_name = kwargs.get('host_user_name')
    host_user_pwd = kwargs.get('host_user_pwd')
    vp_password = kwargs.get('vp_password')
    guest_user_name = kwargs.get('guest_user_name')
    guest_user_pwd = kwargs.get('guest_user_pwd')

    return 'vmrun ' + ''.join(
        [x+' '+y for x, y in zip(['-h', '-P', '-T', '-u', '-p', '-vp', '-gu', '-gp'],
                                 [host_name, host_port, host_type, host_user_name, host_user_pwd,
                                  vp_password, guest_user_name, guest_user_pwd]) if y])

    # return ''.join([x+' '+y for x, y in zip(['-h', '-P', '-T', '-u', '-p', '-vp', '-gu', '-gp'],
    #                              [host_name, host_port, host_type, host_user_name, host_user_pwd,
    #                               vp_password, guest_user_name, guest_user_pwd]) if y])


def clone_vm(old_vmx_path, new_vmx_path, clone_type='full'):
    """
    Create a copy of the VM
    :param old_vmx_path: Path to vmx file
    :param new_vmx_path: Path to destination vmx file
    :param clone_type: full|linked
    :return: None
    """
    proc = subprocess.Popen(['vmrun', 'clone', old_vmx_path, new_vmx_path, clone_type],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    print 'stdout:\n', proc.stdout.read()
    print 'stderr:\n', proc.stderr.read()


def delete_vm(vmx_path):
    """
    delete VM
    :param vmx_path: Path to vmx file
    :return: None
    """
    proc = subprocess.Popen(['vmrun', 'deleteVM', vmx_path])


def start_vm(**kwargs):
    start_type = kwargs.get('start_type') or 'nogui'
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)

    # method 1
    # proc = subprocess.Popen(flags_params + 'start "' + vmx_path + '" ' + start_type, shell=True,
    #                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

    # method 2
    proc = subprocess.Popen([_ for _ in flags_params.split(' ') if _] + ['start', vmx_path, start_type],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

    print 'stdout:\n', proc.stdout.read()
    print 'stderr:\n', proc.stderr.read()


def stop_vm(**kwargs):
    stop_type = kwargs.get('stop_type') or 'soft'
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] + ['stop', vmx_path, stop_type])


def reset_vm(**kwargs):
    reset_type = kwargs.get('reset_type') or 'soft'
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] + ['reset', vmx_path, reset_type])


def run_program_in_guest(**kwargs):
    guest_program_path = kwargs.get('guest_program_path')
    if not guest_program_path:
        raise Exception('no guest_program_path')

    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['runProgramInGuest', vmx_path, '-noWait', '-activeWindow', '-interactive', guest_program_path])


def run_program_with_params_in_guest(**kwargs):
    """
    need program receive params
    :param kwargs:
    :return:
    """
    pass


def delete_file_in_guest(**kwargs):
    file_path_in_guest = kwargs.get('file_path_in_guest')
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['deleteFileInGuest', vmx_path, file_path_in_guest])


def create_file_in_guest(**kwargs):
    file_path_in_guest = kwargs.get('file_path_in_guest')

    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['CreateTempfileInGuest', vmx_path, file_path_in_guest])


def create_directory_in_guest(**kwargs):
    directory_path_in_guest = kwargs.get('directory_path_in_guest')
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['createDirectoryInGuest', vmx_path, directory_path_in_guest])


def delete_directory_in_guest(**kwargs):
    directory_path_in_guest = kwargs.get('directory_path_in_guest')
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['deleteDirectoryInGuest', vmx_path, directory_path_in_guest])


def list_directory_in_guest(**kwargs):
    directory_path_in_guest = kwargs.get('directory_path_in_guest')
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['listDirectoryInGuest', vmx_path, directory_path_in_guest])


def copy_file_from_host_to_guest(**kwargs):
    path_to_vm_file = kwargs.get('path_to_vm_file')
    path_in_guest = kwargs.get('path_in_guest')

    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['CopyFileFromHostToGuest', vmx_path, path_to_vm_file, path_in_guest])


def copy_file_from_guest_to_host(**kwargs):
    path_to_vm_file = kwargs.get('path_to_vm_file')
    path_on_host = kwargs.get('path_on_host')

    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['CopyFileFromGuestToHost', vmx_path, path_to_vm_file, path_on_host])


def rename_file_in_guest(**kwargs):
    path_to_vm_file = kwargs.get('path_to_vm_file')
    original_name = kwargs.get('original_name')
    new_name = kwargs.get('new_name')

    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    subprocess.Popen([_ for _ in flags_params.split(' ') if _] +
                     ['renameFileInGuest', vmx_path, path_to_vm_file, original_name, new_name])


def get_guest_ip_address(**kwargs):
    """
    you must ensure the guest vm is open
    :param kwargs:
    :return:
    """
    vmx_path = kwargs.get('vmx_path')
    flags_params = _authentication_flags(**kwargs)
    # import pdb
    # pdb.set_trace()
    proc = subprocess.Popen([_ for _ in flags_params.split(' ') if _] + ['getGuestIPAddress', vmx_path, '-wait'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    return proc.stdout.read()

if __name__ == '__main__':

    # a_old_vmx_path = '/home/huangyu/vmware/Windows XP Professional/Windows XP Professional.vmx'
    a_new_vmx_path = '/home/huangyu/vmware/Windows XP Professional_clone_1/Windows XP Professional_clone_1.vmx'

    # start_vm(vmx_path=a_new_vmx_path)
    # guest_ip = get_guest_ip_address(vmx_path=a_new_vmx_path)
    # print guest_ip

    # clone_vm(a_old_vmx_path, a_new_vmx_path, clone_type='full')
    # reset_vm(vmx_path=a_old_vmx_path, reset_type='soft')
    # delete_vm(vmx_path=a_new_vmx_path)

    # subprocess.Popen('vmrun -T ws -gu Administrator -gp 1 '
    #                  'runProgramInGuest "/home/huangyu/vmware/Windows XP Professional/Windows XP Professional.vmx" '
    #                  '-noWait -activeWindow -interactive "C:\\test\\dir.bat"',
    #                  shell=True)



