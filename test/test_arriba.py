from test.setup import TestCase
from fusionizer.arriba import Arriba


class TestArriba(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        self.settings.threads = 12
        arriba = Arriba(settings=self.settings).main(
            fq1=f'{self.indir}/MTCQ_R1.fastq.gz',
            fq2=f'{self.indir}/MTCQ_R2.fastq.gz',
            star_index_dir=f'{self.indir}/STAR_index_GRCm39_GENCODEM27',
            assembly_fa=f'{self.indir}/GRCm39.fa',
            annotation_gtf=f'{self.indir}/GENCODEM27.gtf',
            blacklist_tsv=f'{self.indir}/blacklist_mm39_GRCm39_v2.5.1.tsv.gz',
            known_fusions_tsv=f'{self.indir}/known_fusions_mm39_GRCm39_v2.5.1.tsv.gz',
            protein_domains_gff3=f'{self.indir}/protein_domains_mm39_GRCm39_v2.5.1.gff3',
        )
    
    def test_without_resource_files(self):
        self.settings.threads = 12
        arriba = Arriba(settings=self.settings).main(
            fq1=f'{self.indir}/MTCQ_R1.fastq.gz',
            fq2=f'{self.indir}/MTCQ_R2.fastq.gz',
            star_index_dir=f'{self.indir}/STAR_index_GRCm39_GENCODEM27',
            assembly_fa=f'{self.indir}/GRCm39.fa',
            annotation_gtf=f'{self.indir}/GENCODEM27.gtf',
            blacklist_tsv=None,
            known_fusions_tsv=None,
            protein_domains_gff3=None,
        )
