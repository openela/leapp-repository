import os

from leapp.libraries.stdlib import api, run, CalledProcessError
from leapp.actors import Actor
from leapp.tags import FinalizationPhaseTag, IPUWorkflowTag
from leapp.models import FirmwareFacts


BIOS_PATH = '/boot/grub2/grubenv'
EFI_PATH = '/boot/efi/EFI/redhat/grubenv'
EFI_LINK = '../efi/EFI/redhat/grubenv'


class EfiGrubenvFix(Actor):
    """
    Ensure grubenv is symlink on efi systems
    """

    name = 'efi_grubenv_fix'
    consumes = (FirmwareFacts,)
    produces = ()
    tags = (FinalizationPhaseTag.Before, IPUWorkflowTag)

    def process(self):
        for fact in self.consume(FirmwareFacts):
            if fact.firmware == 'efi' and not os.path.islink(BIOS_PATH):
                self.make_grubenv_symlink()
                break


    def make_grubenv_symlink(self):
        if os.path.isfile(EFI_PATH):
            try:
                run(['ln', '-sf', EFI_LINK, BIOS_PATH])
                api.current_logger().info(
                    '{} converted from being a regular file to symlink pointing to {}'.format(BIOS_PATH, EFI_PATH)
                )
            except CalledProcessError as err:
                api.current_logger().warning('Could not create symlink {} pointing to {}: {}'.format(BIOS_PATH, EFI_PATH, str(err)))

