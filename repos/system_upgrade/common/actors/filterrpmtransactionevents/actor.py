from leapp.actors import Actor
from leapp.models import (
    DistributionSignedRPM,
    FilteredRpmTransactionTasks,
    PESRpmTransactionTasks,
    RpmTransactionTasks
)
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class FilterRpmTransactionTasks(Actor):
    """
    Filter RPM transaction events based on installed RPM packages

    In order to calculate a working DNF Upgrade transaction, Leapp can collect data from multiple
    sources and find workarounds for possible problems. This actor will filter all collected
    workarounds and keep only those relevant to current system based on installed packages.
    """

    name = 'check_rpm_transaction_events'
    consumes = (PESRpmTransactionTasks, RpmTransactionTasks, DistributionSignedRPM,)
    produces = (FilteredRpmTransactionTasks,)
    tags = (IPUWorkflowTag, ChecksPhaseTag)

    def process(self):
        installed_pkgs = set()
        for rpm_pkgs in self.consume(DistributionSignedRPM):
            installed_pkgs.update([pkg.name for pkg in rpm_pkgs.items])

        local_rpms = set()
        to_install = set()
        to_remove = set()
        to_keep = set()
        to_upgrade = set()
        to_exclude = set()
        modules_to_enable = {}
        modules_to_reset = {}
        for event in self.consume(RpmTransactionTasks, PESRpmTransactionTasks):
            local_rpms.update(event.local_rpms)
            to_install.update(event.to_install)
            to_remove.update(installed_pkgs.intersection(event.to_remove))
            to_keep.update(installed_pkgs.intersection(event.to_keep))
            modules_to_enable.update({'{}:{}'.format(m.name, m.stream): m for m in event.modules_to_enable})
            modules_to_reset.update({'{}:{}'.format(m.name, m.stream): m for m in event.modules_to_reset})

        to_remove.difference_update(to_keep)

        # run upgrade for the rest of RH signed pkgs which we do not have rule for
        to_upgrade = installed_pkgs - (to_install | to_remove)

        self.produce(FilteredRpmTransactionTasks(
            local_rpms=list(local_rpms),
            to_install=list(to_install),
            to_remove=list(to_remove),
            to_keep=list(to_keep),
            to_upgrade=list(to_upgrade),
            to_exclude.update(event.to_exclude),
            modules_to_reset=list(modules_to_reset.values()),
            modules_to_enable=list(modules_to_enable.values())))
