from leapp.actors import Actor
from leapp.libraries.actor.checkchrony import check_chrony
from leapp.libraries.common.rpms import has_package
from leapp.models import DistributionSignedRPM
from leapp.reporting import Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class CheckChrony(Actor):
    """
    Check for incompatible changes in chrony configuration.

    Warn that the default chrony configuration in OL8 uses the leapsectz
    directive.
    """

    name = 'check_chrony'
    consumes = (DistributionSignedRPM,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        check_chrony(has_package(DistributionSignedRPM, 'chrony'))
