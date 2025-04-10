from leapp import reporting
from leapp.actors import Actor
from leapp.models import QuaggaToFrrFacts, Report
from leapp.reporting import create_report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag

COMMON_REPORT_TAGS = [
    reporting.Groups.NETWORK,
    reporting.Groups.SERVICES
]


class QuaggaReport(Actor):
    """
    Checking for babeld on OL-7.

    This actor is supposed to report that babeld was used on OL-7
    and it is no longer available in OL-8.
    """

    name = 'quagga_report'
    consumes = (QuaggaToFrrFacts, )
    produces = (Report, )
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        try:
            quagga_facts = next(self.consume(QuaggaToFrrFacts))
        except StopIteration:
            return
        if 'babeld' in quagga_facts.active_daemons or 'babeld' in quagga_facts.enabled_daemons:
            create_report([
                reporting.Title('Babeld is not available in FRR'),
                reporting.ExternalLink(
                    url='https://github.com/openela"
                    title='Setting routing protocols in OL8'),
                reporting.Summary(
                    'babeld daemon which was a part of quagga implementation in OL7 '
                    'is not available in OL8 in FRR due to licensing issues.'
                ),
                reporting.Severity(reporting.Severity.HIGH),
                reporting.Groups(COMMON_REPORT_TAGS),
                reporting.Groups([reporting.Groups.INHIBITOR]),
                reporting.Remediation(hint='Please use RIP, OSPF or EIGRP instead of Babel')
            ])
        else:
            self.log.debug('babeld not used, moving on.')
