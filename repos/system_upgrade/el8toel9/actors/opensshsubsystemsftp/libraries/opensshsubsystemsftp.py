from leapp import reporting
from leapp.exceptions import StopActorExecutionError
from leapp.libraries.stdlib import api


def process(openssh_messages):
    config = next(openssh_messages, None)
    if list(openssh_messages):
        api.current_logger().warning('Unexpectedly received more than one OpenSshConfig message.')
    if not config:
        raise StopActorExecutionError(
            'Could not check openssh configuration', details={'details': 'No OpenSshConfig facts found.'}
        )

    # not modified configuration will get updated by RPM automatically
    if not config.modified:
        return

    if not config.subsystem_sftp:
        resources = [
            reporting.RelatedResource('package', 'openssh-server'),
            reporting.RelatedResource('file', '/etc/ssh/sshd_config'),
        ]
        reporting.create_report([
            reporting.Title('OpenSSH configured without SFTP subsystem'),
            reporting.Summary(
                'The OL9 is changing the default SCP behaviour to use SFTP internally '
                'so not having SFTP server enabled can prevent interoperability and break existing '
                'scripts on other systems updated to OL9 to copy files to or from this machine.'
            ),
            reporting.Remediation(
                hint='Add the following line to the /etc/ssh/sshd_config to enable SFTP server: '
                     'Subsystem sftp /usr/libexec/openssh/sftp-server'
            ),
            reporting.Severity(reporting.Severity.MEDIUM),
            reporting.Groups([
                    reporting.Groups.AUTHENTICATION,
                    reporting.Groups.SECURITY,
                    reporting.Groups.NETWORK,
                    reporting.Groups.SERVICES
            ]),
        ] + resources)
