import sn
import mwclient
from mwclient import Site
import numpy as np
import mwparserfromhell

agent = 'Bot for project at CWRU using mwclient/' + mwclient.__ver__
site = Site(('https', 'bots.snpedia.com'), path='/')
for cat in site.allcategories():
    print(cat)

genome = sn.parse("genomes/123.23andme.54")


def cross_ref_snpedia(user_snps, snpedia):
    print('Loaded SNPs from SNPedia')
    page_list = []
    for i, snp in enumerate(user_snps):
        if i % 50000 == 0:
            print(i)
        if snp.name.lower() in snpedia:
            try:
                page_name = snp.name + '(' + snp.genotype[0] + ';' + snp.genotype[1] + ')'
                page_list = np.append(page_list, page_name)
            except IndexError:
                continue
    print(page_list[:100])
    print(page_list.shape)
    return page_list


def get_snp_info(snp_page):
    snp = site.pages[snp_page]
    wikicode = mwparserfromhell.parse(snp.text())
    try:
        genotype = wikicode.filter_templates()[0]
        allele_1 = genotype.get('allele1').value
        allele_2 = genotype.get('allele2').value
        magnitude = genotype.get('magnitude').value
        summary = genotype.get('summary').value
        print(snp_page, magnitude, summary)
    except IndexError:
        pass
    except ValueError:
        pass


def get_snpedia_saved():
    snp_list = np.load('snpedia.npy')
    return set(snp_list)


def get_snpedia():
    snps = site.Categories['SNPs on chromosome 1']
    snp_list = np.array([])
    for i, snp in enumerate(snps):
        snp_list = np.append(snp_list, snp.name.lower())
    np.save('snpedia', snp_list)
    return set(snp_list)


snpedia = get_snpedia_saved()
page_list = cross_ref_snpedia(genome, snpedia)
for page in page_list:
    get_snp_info(page)
