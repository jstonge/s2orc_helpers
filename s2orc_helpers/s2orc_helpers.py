import re

"""Main module."""
def get_start_headers(paper, annot):
    headers = paper['content']['annotations'][annot]
    if headers:
        return [int(_) for _ in re.findall('(?<=start\":)\d+', headers)]

def grab_citations(paper, start, end):
    end_str = re.escape(paper['content']['text'][start:end])
    return re.findall(rf'([^.]*?{end_str}.+?\.)', paper['content']['text'])


def get_bibid_source(paper, source):
    bibentry = paper['content']['annotations']['bibentry']
    re_pat_split = '({"attributes":{.+?},"end":\d+,"start":\d+})'
    bibentry = [re.split(",", _) for _ in re.findall(re_pat_split, bibentry)]
    
    matched_id_re = '(?<=\"matched_paper_id\":)\d+'
    bib_id_re = '(?<=\"id\":\")[a-z]\d+'
    
    matched_paper_ids = {
        int(re.findall(matched_id_re, ' '.join(entry))[0]): re.findall(bib_id_re, ' '.join(entry))[0]
        for entry in bibentry 
        if re.search('matched_paper_id', ' '.join(entry))
    }
    return matched_paper_ids.get(source)


def parse_res(paper, annot, source=None):
    """
    annotation types:
    ================
    - type1: paragraph
    - type2: figureref, sectionheader -> sections, tableref
    - type3: 'authors'

    Desc
    ====
    bibauthor: Authors in the bibliography
    bibentry: Cited papers in the bibliography
    bibref: Citations in the papers

     ('abstract', 'author', 'authoraffiliation', 'authorfirstname', 
      'authorlastname', 'bibauthor', 'bibauthorfirstname', 'bibauthorlastname', 
      'bibentry', 'bibref', 'bibtitle', 'bibvenue', 'figure', 
      'formula',  'publisher', 'table', 'title', 'venue')
    """
    # subset[0]['content']['annotations'].keys()
    # paper, annot = papers_broido[0], 'figurecaption'
    
    paragraphs = paper['content']['annotations']['paragraph']
    if annot in ['sectionheader', 'figureref', 'tableref', 'figurecaption']:
        headers = paper['content']['annotations'][annot]
        paper['content']['text'][103213:103548]
        if headers is not None:
            corpusIds = []
            sections = []
            content = []
            # headers = paper['content']['annotations']['tableref']
            start_headers = [int(_) for _ in re.findall('(?<=start\":)\d+', headers)]
            tot_sections = len(start_headers)-1
            if paragraphs is not None:
                section = 1
                for start, end in zip(start_headers[:-1], start_headers[1:]):
                    text = paper['content']['text'][start:(end-1)]
                    corpusIds.append(paper['corpusid'])
                    sections.append(f'{section}/{tot_sections}')
                    content.append(text)
                    section += 1
    
            return {'corpusid': corpusIds, 'sections': sections, 'text': content}
    

    elif annot in 'bibref':
        pass

def parse_bibref(paper, source):
    # paper = papers_broido[0]
    rel_bibid = get_bibid_source(paper, source)
    # paper['externalids']
    bibentry = paper['content']['annotations']['bibref']
    re_pat_split = '({"attributes":{.+?},"end":\d+,"start":\d+})'
    bibentry = [re.split(",", _) for _ in re.findall(re_pat_split, bibentry)]

    out = []
    for entry in bibentry:
        # entry = bibentry[0]
        entries = {}
        matched_id = re.findall('(?<=\"ref_id\":\")[a-z]\d+' , ', '.join(entry))[0]
        if matched_id == rel_bibid:
            for field in entry:
            
                k = re.findall("\w+", re.split(":", field)[0])[0]
                v = re.findall("\w+", re.split(":", field)[1])[0]
                
                if v.isdigit():
                    v = int(v)

                entries.update({k:v})
            out.append(entries)

    
    return [grab_citations(paper, ref['start'], ref['end']) for ref in out]


papers_broido = []
import json

with open("broido_debate.jsonl") as f:
    for line in f:
        papers_broido.append(json.loads(line))

papers_broido[1]['externalids']['doi']
papers_broido[1]['content']['source']

all_titles = []
for i in range(len(papers_broido)):
    if papers_broido[i]['content']['annotations']['title'] is not None:
        try:
            for x in json.loads(papers_broido[i]['content']['annotations']['title']):
                all_titles.append(papers_broido[i]['content']['text'][x['start']:x['end']])
        except:
            print(i)

all_titles = list(set(all_titles))

all_titles[30]

foo = json.loads(papers_broido[90]['content']['annotations']['title'])
papers_broido[90]['content']['text'][1:147]

all_titles



fig_caption = parse_res(papers_broido[17], "figurecaption")