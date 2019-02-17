'''
Translate markdown .md file to html file. 
'''
import argparse

FONT_SIZE = (12, 36, 24, 18, 16, 14, 13, 13, 13)

def main():
    args = parseArgs()
    with open(args.output, 'w+') as html:
        def write(*args, **kw):
            print(*args, file = html, **kw)
        # write('<!DOCTYPE html>')
        write('<html><body>')
        with open(args.input, 'r') as md:
            for line in md:
                write(translateLine(line))
        write('</body></html>')
    print('Done. Written to', args.output)

def parseArgs():
    parser = argparse.ArgumentParser(description = 'Convert markdown to html')
    parser.add_argument('--input', '-i', type = str, default = 'raw.md', help = 'input markdown file')
    parser.add_argument('--output', '-o', type = str, default = 'build.html', help = 'output html file')
    return parser.parse_args()

def translateLine(raw):
    n_hash = 0
    while raw.startswith('#'):
        n_hash += 1
        raw = raw[1:]
    tag = n_hash2Tag(n_hash)
    s = raw.strip() + '&nbsp;'
    s = handleLinks(s)
    return tag % s

def n_hash2Tag(n_hash):
    styles = []
    styles.append('font-size: %dpt;' % FONT_SIZE[n_hash])
    # styles.append('line-height: 1.2;')
    if n_hash >= 1:
        styles.append('margin-top: 0;')
        styles.append('padding-top: 2pt;')
        styles.append('padding-bottom: 2pt;')
        styles.append('margin-bottom: 0;')
        styles.append('font-weight: bold;')
    style = 'style="%s"' % ' '.join(styles)
    if n_hash == 0:
        tag = f'<span {style}>%s</span><br />'
    if n_hash >= 1:
        tag = f'<h{n_hash} {style}>%s</h{n_hash}>'
        if n_hash in (1, 2):
            tag += '<hr />'
    return tag

def handleLinks(s):
    # before[text](link)after
    try:
        while '](' in s:
            left, right = s.split('](', 1)
            brack_pos = left.rfind('[')
            before = left[:brack_pos]
            text = left[brack_pos + 1:]
            link, after = right.split(')', 1)
            s = '%s<a href="%s">%s</a>%s' % (before, link, text, after)
    except Exception as e:
        print(e, 'illegal line:', s)
    return s

if __name__ == '__main__':
    main()
