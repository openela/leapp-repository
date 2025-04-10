from leapp.actors import Actor
from leapp.libraries import stdlib
from leapp.libraries.common.rpms import get_installed_rpms
from leapp.libraries.stdlib import api, CalledProcessError, run
from leapp.reporting import Report
from leapp.models import SystemFIPSStatus
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag, ExperimentalTag
import os


class CheckSystemFIPSStatus(Actor):
    """
    Check fips status for System systems

    """

    name = 'check_System_fips_status'
    consumes = ()
    produces = (SystemFIPSStatus)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        if os.getenv('LEAPP_FIPS','0') == '0':
            return
        with open('/proc/cmdline') as f:
            if 'fips=1' in f.read():
                api.produce(SystemFIPSStatus(fips_status='enabled'))
                api.current_logger().info('Setting System FIPS status to enabled')
            else:
                api.produce(SystemFIPSStatus(fips_status='disabled'))
                api.current_logger().info('Setting System FIPS status to disabled')
