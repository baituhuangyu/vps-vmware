from django.shortcuts import render, redirect
from operate import *
from models import *
from uuid import uuid4
import re
import time

MAX_VM_COUNT = 8


def index(request):
    return render(request, 'index.html', locals())


def operate_vm(request):
    if request.method == 'GET':
        a_vm_id = request.GET.get('a_vm_id')
        if not a_vm_id:
            # todo
            return redirect('/')

        a_vm_id = int(a_vm_id)
        a_vm = Vm.objects.get(id=a_vm_id)
        return render(request, 'operate.html', locals())

    # POST
    operate = request.POST.get('operate')
    start_type = 'gui'
    a_vm_id = request.POST.get('a_vm_id')
    a_vm_id = int(a_vm_id)
    a_vm = Vm.objects.get(id=a_vm_id)
    vmx_path = a_vm.path_name

    if operate == 'start':
        start_vm(vmx_path=vmx_path, start_type=start_type)

    elif operate == 'stop':
        stop_vm(vmx_path=vmx_path, stop_type='soft')

    elif operate == 'restart':
        reset_vm(vmx_path=vmx_path, reset_type='soft')

    return render(request, 'operate.html', locals())


def new_vm(request):

    # xp host
    # ubuntu host
    # win7 host
    # win10 host
    # todo
    if request.method == 'GET':
        vm_type_s = VmType.objects.all()
        vm_count = Vm.objects.count()
        return render(request, 'new.html', locals())

    operate = request.POST.get('operate')
    if operate == 'new':
        last_vm = Vm.objects.last()
        vm_type_id = request.POST.get('vm_type_id')
        vm_template = VmType.objects.get(id=int(vm_type_id))

        old_vmx_path = vm_template.path_name
        old_vmx_path_split = old_vmx_path.split('/')
        last_vm_id = last_vm.id if last_vm else 1

        vm_count = Vm.objects.count()
        if vm_count > MAX_VM_COUNT:
            return redirect('/vps')

        old_vmx_path_split[-2] = old_vmx_path_split[-2] + '_clone_' + str(last_vm_id)

        old_vmx_path_split[-1] = re.sub(r'.vmx$', '', old_vmx_path_split[-1]) + '_clone_' + str(last_vm_id) + '.vmx'
        new_vmx_path = '/'.join(old_vmx_path_split)

        # # todo
        # clone
        clone_vm(old_vmx_path=old_vmx_path, new_vmx_path=new_vmx_path, clone_type='linked')
        # start to get ip
        time.sleep(5)
        start_vm(vmx_path=new_vmx_path, start_type='nogui')
        time.sleep(5)
        guest_ip = get_guest_ip_address(vmx_path=new_vmx_path)
        login_name = 'Administrator' if vm_type_id == '1' else 'huangyu'
        login_password = '1'

        Vm.objects.create(
            name=old_vmx_path_split[-1],
            vm_id=uuid4().hex,
            type_name=vm_template.name,
            os_name=vm_template.os_name,
            path_name=new_vmx_path,

            # net config todo
            net_type='',
            lan_ip=guest_ip,
            eth_ip='',
            gate_way='',
            network_mask='',

            adsl_pwd='',
            adsl='',
            login_name=login_name,
            login_password=login_password,
        )

    return redirect('/vps')
    # return render(request, 'vps.html', locals())


def show_vps(request):
    if request.method == 'GET':
        vm_s = Vm.objects.all()
        return render(request, 'vps.html', locals())





