import os
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
    cytobands_tsv: Optional[str]

    unsorted_bam: str
    sorted_bam: str

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

        self.run_star_and_arriba()
        self.sort_bam()
        self.draw_fusions()

    def run_star_and_arriba(self):
        os.makedirs(f'{self.outdir}/STAR', exist_ok=True)
        self.unsorted_bam = f'{self.outdir}/STAR/Aligned.out.bam'
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
            f'tee {self.unsorted_bam}',
            '|',
            'arriba',
            '-x /dev/stdin',
            f'-o {self.outdir}/fusions.tsv',
            f'-O {self.outdir}/fusions.discarded.tsv',
            f'-a {self.assembly_fa}',
            f'-g {self.annotation_gtf}',
        ]

        if self.blacklist_tsv is not None:
            lines += [f'-b {self.blacklist_tsv}']
        else:
            lines += ['-f blacklist']

        if self.known_fusions_tsv is not None:
            lines += [f'-k {self.known_fusions_tsv}', f'-t {self.known_fusions_tsv}']

        if self.protein_domains_gff3 is not None:
            lines += [f'-p {self.protein_domains_gff3}']

        lines += [
            f'1> {self.outdir}/STAR-arriba.log',
            f'2> {self.outdir}/STAR-arriba.log',
        ]

        self.call(self.CMD_LINEBREAK.join(lines))

    def sort_bam(self):
        self.sorted_bam = f'{self.outdir}/STAR/Aligned.sortedByCoord.out.bam'
        lines = [
            'samtools sort',
            f'-@ {self.threads}',
            f'-o {self.sorted_bam}',
            self.unsorted_bam,
        ]
        self.call(self.CMD_LINEBREAK.join(lines))
        self.call(f'samtools index {self.sorted_bam}')
        self.call(f'rm {self.unsorted_bam}')

    def draw_fusions(self) -> None:
        lines = [
            'draw_fusions.R',
            f'--fusions={self.outdir}/fusions.tsv',
            f'--annotation={self.annotation_gtf}',
            f'--output={self.outdir}/fusions.pdf',
            f'--alignments={self.sorted_bam}',
        ]

        if self.cytobands_tsv is not None:
            lines += [f'--cytobands={self.cytobands_tsv}']

        if self.protein_domains_gff3 is not None:
            lines += [f'--proteinDomains={self.protein_domains_gff3}']

        self.call(self.CMD_LINEBREAK.join(lines))
