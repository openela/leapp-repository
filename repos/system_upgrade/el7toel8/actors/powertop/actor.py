from leapp import reporting
from leapp.actors import Actor
from leapp.libraries.common.rpms import has_package
from leapp.models import DistributionSignedRPM
from leapp.reporting import create_report, Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class PowerTop(Actor):
    """
    Check if PowerTOP is installed. If yes, write information about non-compatible changes.
    """

    name = 'powertop'
    consumes = (DistributionSignedRPM,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        if has_package(DistributionSignedRPM, 'powertop'):
            create_report([
                reporting.Title('PowerTOP compatibility options removed in the next major version'),
                reporting.Summary(
                    'The -d (dump) option which has been kept for OpenELA backward compatibility has been '
                    'dropped.\n'
                    'The -h option which has been used for OpenELA backward compatibility is no longer '
                    'alias for --html, but it\'s now an alias for --help to follow the upstream.\n'
                    'The -u option which has been used for OpenELA backward compatibility as an alias for '
                    '--help has been dropped.\n'
                ),
                reporting.Severity(reporting.Severity.LOW),
                reporting.Groups([reporting.Groups.TOOLS, reporting.Groups.MONITORING]),
                reporting.Remediation(hint='Please remove the dropped options from your scripts.'),
                reporting.RelatedResource('package', 'powertop')
            ])
