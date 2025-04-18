from leapp.models import fields, Model
from leapp.topics import SystemInfoTopic, TransactionTopic


class SELinuxModule(Model):
    """SELinux module in cil including priority"""
    topic = SystemInfoTopic
    name = fields.String()
    priority = fields.Integer()
    content = fields.String()
    # lines removed due to content invalid on RHEL 8
    removed = fields.List(fields.String())


class SELinuxModules(Model):
    """
    List of selinux modules that are not part of distribution policy

    modules - list of custom policy modules (priority != 100,200)
    templates - List of installed udica templates
    """
    topic = SystemInfoTopic
    modules = fields.List(fields.Model(SELinuxModule))
    templates = fields.List(fields.Model(SELinuxModule))


class SELinuxCustom(Model):
    """SELinux customizations returned by semanage export"""
    topic = SystemInfoTopic
    commands = fields.List(fields.String())
    removed = fields.List(fields.String())


class SELinuxRequestRPMs(Model):
    """
    SELinux related RPM packages that need to be present after upgrade

    Listed packages provide types that where used in policy
    customizations (to_install), or the corresponding policy
    was installed on OL-7 installation with priority 200
    (to_keep).
    """
    topic = TransactionTopic
    to_keep = fields.List(fields.String(), default=[])
    to_install = fields.List(fields.String(), default=[])
