from leapp.actors import Actor
from leapp.libraries import stdlib
from leapp.libraries.common.rpms import get_installed_rpms
from leapp.libraries.stdlib import api, CalledProcessError, run
from leapp.reporting import Report
from leapp.models import SystemFIPSStatus
from leapp.tags import FinalizationPhaseTag, IPUWorkflowTag, ExperimentalTag


class EnableSystemFIPS(Actor):
    """
    Enable fips depending on previous fips status

    Removal of el7 kernel packages is required to run fips-mode-setup
    """

    name = 'enable_System_fips'
    consumes = (SystemFIPSStatus)
    produces = ()
    tags = (FinalizationPhaseTag.After, IPUWorkflowTag)

    def process(self):
        fips_enabled = next(api.consume(SystemFIPSStatus), None)
        if fips_enabled is None:
            return
        if fips_enabled.fips_status != 'enabled':
            return

        cmd = ['fips-mode-setup', '--enable']
        try:
            stdlib.run(cmd)
        except CalledProcessError:
            api.current_logger().error('fips could not be enabled.')

