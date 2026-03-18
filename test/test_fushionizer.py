from os.path import dirname
from test.setup import TestCase
from fusionizer.fushionizer import Fusionizer


class TestFusionizer(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        self.settings.threads = 12
        self.arriba_indir = f'{dirname(self.indir)}/test_arriba'  # use the same files to save disk space
        Fusionizer(settings=self.settings).main(
            fq1=f'{self.arriba_indir}/MTCQ_R1.fastq.gz',
            fq2=f'{self.arriba_indir}/MTCQ_R2.fastq.gz',
            star_index_dir=f'{self.arriba_indir}/STAR_index_GRCm39_GENCODEM27',
            assembly_fa=f'{self.arriba_indir}/GRCm39.fa',
            annotation_gtf=f'{self.arriba_indir}/GENCODEM27.gtf',
            blacklist_tsv=f'{self.arriba_indir}/blacklist_mm39_GRCm39_v2.5.1.tsv.gz',
            known_fusions_tsv=f'{self.arriba_indir}/known_fusions_mm39_GRCm39_v2.5.1.tsv.gz',
            protein_domains_gff3=f'{self.arriba_indir}/protein_domains_mm39_GRCm39_v2.5.1.gff3',
            cytobands_tsv=f'{self.arriba_indir}/cytobands_mm39_GRCm39_v2.5.1.tsv',
        )
