import os

def get_oci_region_var():
    if os.path.exists('/etc/yum/vars/ociregion'):
        f = open("/etc/yum/vars/ociregion", "r")
        oci_region = (f.readline())
        oci_region = oci_region.rstrip("\n")
        f.close()
        return oci_region
    else:
        return ''

def get_oci_domain_var():
    if os.path.exists('/etc/yum/vars/ocidomain'):
        f = open("/etc/yum/vars/ocidomain", "r")
        oci_domain = (f.readline())
        oci_domain = oci_domain.rstrip("\n")
        f.close()
        return oci_domain
    else:
        return 'oracle.com'

