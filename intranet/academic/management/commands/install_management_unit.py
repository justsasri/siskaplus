from django.db import transaction
from django.core.management import CommandError, BaseCommand
from campusgo.academic.models import ManagementUnit


def create_rmu_roots():
    Rmu = ManagementUnit
    ibi = Rmu.objects.create(parent=None, name='IBI Darmajaya', number='000', code='IBI', type=1)

    fik = Rmu.objects.create(parent=ibi, name='Fakultas Ilmu Komputer', number='100', code='FIK', type=2)
    feb = Rmu.objects.create(parent=ibi, name='Fakultas Ekonomi dan Bisnis', number='200', code='FEB', type=2)

    dmi = Rmu.objects.create(parent=fik, name='D3 Manajemen Informatika', number='101', code='DMI', type=4)
    dtk = Rmu.objects.create(parent=fik, name='D3 Teknik Komputer', number='102', code='DTK', type=4)
    sti = Rmu.objects.create(parent=fik, name='S1 Teknik Informatika', number='103', code='STI', type=4)
    ssi = Rmu.objects.create(parent=fik, name='S1 Sistem Informasi', number='104', code='SSI', type=4)
    ssk = Rmu.objects.create(parent=fik, name='S1 Sistem Komputer', number='105', code='SSK', type=4)
    sdk = Rmu.objects.create(parent=fik, name='S1 Desain Komunikasi Visual', number='106', code='SDK', type=4)
    mti = Rmu.objects.create(parent=fik, name='S2 Teknik Informatika', number='107', code='MTI', type=4)

    dmm = Rmu.objects.create(parent=feb, name='D3 Akuntansi', number='201', code='DMM', type=4)
    sak = Rmu.objects.create(parent=feb, name='S1 Akuntansi', number='202', code='SAK', type=4)
    sem = Rmu.objects.create(parent=feb, name='S1 Manajemen', number='203', code='SEM', type=4)
    sbd = Rmu.objects.create(parent=feb, name='S1 Bisnis Digital', number='204', code='SBD', type=4)
    mem = Rmu.objects.create(parent=feb, name='S2 Manajemen', number='205', code='MEM', type=4)


def clean_rmu_roots():
    ManagementUnit.objects.filter(code__in=[
        'IBI', 'FIK', 'FEB', 'DMI', 'DTK', 'STI', 'SSI', 'SSK', 'SDK', 'MTI', 'DMM', 'SAK', 'SEM', 'SBD', 'MEM'
    ]).delete()


def install_management_unit(clean=True):
    with transaction.atomic():
        if clean:
            clean_rmu_roots()
        create_rmu_roots()
    print('Successfully install academic management_unit.')


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        clean = options.get('clean')
        install_management_unit(clean)
        self.stdout.write(self.style.SUCCESS('Successfully install academic management_unit.'))
