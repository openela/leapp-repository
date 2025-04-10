from leapp.actors import Actor
from leapp.libraries.actor import persistentnetnamesconfig
from leapp.models import (
    InitrdIncludes,
    PersistentNetNamesFacts,
    PersistentNetNamesFactsInitramfs,
    RenamedInterfaces,
    TargetInitramfsTasks
)
from leapp.tags import ApplicationsPhaseTag, IPUWorkflowTag
from leapp.utils.deprecation import suppress_deprecation


@suppress_deprecation(InitrdIncludes)
class PersistentNetNamesConfig(Actor):
    """
    Generate udev persistent network naming configuration

    This actor generates systemd-udevd link files for each physical ethernet interface present on OL-7
    in case we notice that interface name differs on OL-8. Link file configuration will assign OL-7 version of
    a name. Actors produces list of interfaces which changed name between OL-7 and OL-8.
    """

    name = 'persistentnetnamesconfig'
    consumes = (PersistentNetNamesFacts, PersistentNetNamesFactsInitramfs)
    produces = (RenamedInterfaces, InitrdIncludes, TargetInitramfsTasks)
    tags = (ApplicationsPhaseTag, IPUWorkflowTag)
    initrd_files = []

    def process(self):
        persistentnetnamesconfig.process()
