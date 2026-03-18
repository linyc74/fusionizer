from typing import Optional
from .arriba import Arriba
from .template import Processor


class Fusionizer(Processor):

    fq1: str
    fq2: str
    star_index_dir: str
    assembly_fa: str
    annotation_gtf: str
    blacklist_tsv: Optional[str]
    known_fusions_tsv: Optional[str]
    protein_domains_gff3: Optional[str]
    cytobands_tsv: Optional[str]

    def main(
            self,
            fq1: str,
            fq2: str,
            star_index_dir: str,
            assembly_fa: str,
            annotation_gtf: str,
            blacklist_tsv: Optional[str],
            known_fusions_tsv: Optional[str],
            protein_domains_gff3: Optional[str],
            cytobands_tsv: Optional[str]):

        self.fq1 = fq1
        self.fq2 = fq2
        self.star_index_dir = star_index_dir
        self.assembly_fa = assembly_fa
        self.annotation_gtf = annotation_gtf
        self.blacklist_tsv = blacklist_tsv
        self.known_fusions_tsv = known_fusions_tsv
        self.protein_domains_gff3 = protein_domains_gff3
        self.cytobands_tsv = cytobands_tsv

        Arriba(settings=self.settings).main(
            fq1=self.fq1,
            fq2=self.fq2,
            star_index_dir=self.star_index_dir,
            assembly_fa=self.assembly_fa,
            annotation_gtf=self.annotation_gtf,
            blacklist_tsv=self.blacklist_tsv,
            known_fusions_tsv=self.known_fusions_tsv,
            protein_domains_gff3=self.protein_domains_gff3,
            cytobands_tsv=self.cytobands_tsv,
        )
