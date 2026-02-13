from typing import Optional
from .template import Processor


class Arriba(Processor):

    fq1: str
    fq2: str
    star_index_dir: str
    assembly_fa: str
    annotation_gtf: str
    blacklist_tsv: Optional[str]
    known_fusions_tsv: Optional[str]
    protein_domains_gff3: Optional[str]

    def main(
            self,
            fq1: str,
            fq2: str,
            star_index_dir: str,
            assembly_fa: str,
            annotation_gtf: str,
            blacklist_tsv: str,
            known_fusions_tsv: str,
            protein_domains_gff3: str):

        self.fq1 = fq1
        self.fq2 = fq2
        self.star_index_dir = star_index_dir
        self.assembly_fa = assembly_fa
        self.annotation_gtf = annotation_gtf
        self.blacklist_tsv = blacklist_tsv
        self.known_fusions_tsv = known_fusions_tsv
        self.protein_domains_gff3 = protein_domains_gff3

        lines = [
            'STAR',
            f'--runThreadN {self.threads}',
            f'--genomeDir {self.star_index_dir}',
            f'--outFileNamePrefix {self.outdir}/STAR/',
            '--genomeLoad NoSharedMemory',
            f'--readFilesIn {self.fq1} {self.fq2}',
            '--readFilesCommand zcat',
            '--outStd BAM_Unsorted',
            '--outSAMtype BAM Unsorted',
            '--outSAMunmapped Within',
            '--outBAMcompression 0',
            '--outFilterMultimapNmax 50',
            '--peOverlapNbasesMin 10',
            '--alignSplicedMateMapLminOverLmate 0.5',
            '--alignSJstitchMismatchNmax 5 -1 5 5',
            '--chimSegmentMin 10',
            '--chimOutType WithinBAM HardClip',
            '--chimJunctionOverhangMin 10',
            '--chimScoreDropMax 30',
            '--chimScoreJunctionNonGTAG 0',
            '--chimScoreSeparation 1',
            '--chimSegmentReadGapMax 3',
            '--chimMultimapNmax 50',
            '|',
            'arriba',
            f'-x /dev/stdin',
            f'-o {self.outdir}/fusions.tsv',
            f'-O {self.outdir}/fusions.discarded.tsv',
            f'-a {self.assembly_fa}',
            f'-g {self.annotation_gtf}',
        ]

        if self.blacklist_tsv is not None:
            lines += [f'-b {self.blacklist_tsv}']
        else:  # no blacklist file provided
            lines += ['-f blacklist']  # disable blacklist filtering
        
        if self.known_fusions_tsv is not None:
            lines += [f'-k {self.known_fusions_tsv}']
        if self.known_fusions_tsv is not None:
            lines += [f'-t {self.known_fusions_tsv}']
        if self.protein_domains_gff3 is not None:
            lines += [f'-p {self.protein_domains_gff3}']
        
        lines += [
            f'1> {self.outdir}/STAR-arriba.log',
            f'2> {self.outdir}/STAR-arriba.log',
        ]
        
        self.call(self.CMD_LINEBREAK.join(lines))
