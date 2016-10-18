#!/usr/bin/env python
# encoding: utf-8
'''
fabfile -- automation deployment tools.

@author:     FengXi

'''
import os

from fabric.api import sudo, local, run, put, env, cd, settings
from fabric.contrib.files import append

#local home dir
env.local_home = os.path.expanduser('~')

env.svc_user = "nqsky"
env.svc_sudo_pwd = "Nsky@0!6"

env.remote_build_dir = "/home/%s/uc_build/dco" % env.svc_user
env.remote_build_opendj_dir = "%s/" % env.remote_build_dir
env.remote_deploy_opendj_dir = "/usr/local/opendj"
env.remote_build_qa_tools_dir = "/home/%s/uc_build/" % env.svc_user

#CHANGE ME
env.local_build_dir = "%s/work/ROOT/edp_codes/edp_uc" % env.local_home
env.local_build_opendj_dir = "%s/dco/install/uc/opendj/" % env.local_build_dir
env.local_build_qa_tools_dir = "%s/qa/" % env.local_build_dir

def push_public_key(key_file='~/.ssh/id_rsa.pub'):
    """
    push ssh public key to remote server(s).
    """
    remote_authorized_keys = "/home/%s/.ssh/authorized_keys" % env.svc_user

    def _read_key_file(key_file):
        key_file = os.path.expanduser(key_file)
        with open(key_file) as f:
            return f.read()

    key = _read_key_file(key_file)

    with settings(warn_only=True):
        # check if the public exists on remote server.
        ret = run("grep -q '%s' '%s'" %  (key, remote_authorized_keys))
        if ret.return_code == 0:
            pass
        else:
            append(remote_authorized_keys, key)
            run("chmod 600 %s" % remote_authorized_keys)

def greeting(msg="Hello", who="XiFeng"):
    """
    echo on remote server(s)
    """
    run("echo %s %s" % (msg, who))

def create_dir(parent="/tmp", path="xifeng"):
    """
    mkdir on remote server(s)
    """
    full_path = "%s/%s" % (parent, path)
    #delete first then create
    run ("echo rm %s" % full_path)
    run("rm -rf %s 2>/dev/null" % (full_path))

    run ("echo mkdir %s" % full_path)
    run("mkdir -p %s " % (full_path))

def fetch_build():
    """
    @todo: download the build from jenkins
    """
    local("echo downloading build from jenkins...")
    pass

def upload_build():
    """
    upload uc build to remote server(s).
    """
    def _pre():
        run("mkdir -p %s" % env.remote_build_dir)
        run("mkdir -p %s" % env.remote_build_opendj_dir)
        run("mkdir -p %s" % env.remote_build_qa_tools_dir)

    def _upload():
        #upload opendj install pkg
        put(local_path=env.local_build_opendj_dir, remote_path=env.remote_build_opendj_dir, mirror_local_mode=True)

        #upload qa tools
        put(local_path=env.local_build_qa_tools_dir, remote_path=env.remote_build_qa_tools_dir, mirror_local_mode=True)

    fetch_build()
    _pre()
    _upload()

def uninstall():
    """
    trying to stop opendj and uninstall/remove everything.
    """
    with settings(warn_only=True):
        with cd(env.remote_build_opendj_dir):
            sudo(command="./opendj/uninstall.sh")

def install():
    """
    fresh install one OpenDJ server on remote server(s).
    In case an existing OpenDJ is installed, will stop and remove .
    """

    def _install():
        with cd(env.remote_build_opendj_dir):
            sudo(command="./opendj/install.sh")
            sudo(command="./opendj/init_uc.sh")

    """
    disable/stop firewalld for easier QA.
    """
    def _post():
        sudo("systemctl stop firewalld")
        sudo("systemctl disable firewalld")

    upload_build()
    uninstall()
    _install()
    _post()

def sample(tenant=10,subject=100,token=100,org=10,ext=10):
    """
    sample OpenDJ data.
    """
    def _pre():
        sudo("systemctl start opendj")

        #install python-ldap if no.
        with settings(warn_only=True):
            ret = run("rpm -q python-ldap")
            if ret.return_code == 0:
                pass
            else:
                sudo("yum install -y python-ldap")

    #_pre()

    with cd("%s/qa/bin/" % env.remote_build_qa_tools_dir):
        run("python ./tenant.py --tenant %s --subject %s --token %s --org %s --ext %s" % (tenant, subject, token, org, ext))

def audit_log():
    """
     Debug: enable OpenDJ audit log. Find /usr/local/opendj/current/logs/audit
    """
    with cd("%s/qa/bin/" % env.remote_build_qa_tools_dir):
        run("python ./auditlog.py enable")

