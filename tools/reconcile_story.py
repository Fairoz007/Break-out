from pathlib import Path
R=Path(__file__).resolve().parents[1]
for p in [R/'STORY.md',* (R/'docs/chapters').glob('*.md'),*(R/'docs/characters').glob('*.md')]:
    s=p.read_text(encoding='utf-8')
    s=s.replace('Mercer’s provocation','Silas’s provocation').replace('Mercer’s intimidation','his own intimidation')
    s=s.replace('Noah safely stops a machine while Adrian reads the route','Adrian holds the idle press isolation lever while Noah clears its screen; Noah then holds the inspection lamp while Adrian reads the diagram')
    s=s.replace('Adrian holds the isolated machine brake while Noah retrieves and memorizes the diagram','Adrian holds the idle press isolation lever while Noah clears its screen; Noah then holds the inspection lamp while Adrian reads the diagram')
    s=s.replace('an interlocked power isolation and hand-operated machinery sequence','a fictional A/B/C selector operated by Adrian while Noah holds the mechanical brake; Adrian selects B')
    s=s.replace('a fictional A/B/C selector interlocked with Adrian’s held brake wheel; Noah selects B','a fictional A/B/C selector operated by Adrian while Noah holds the mechanical brake; Adrian selects B')
    s=s.replace('`CHAR_INMATE`: yard antagonist Mercer acting on Silas’s intimidation test, workshop workers and background population require distinct silhouette/outfit variations. Mercer provokes Noah over the approved photograph, then retreats after guard intervention; he is not secretly VANTAGE leadership.','`CHAR_INMATE`: workshop workers and background population require distinct silhouette/outfit variations. Silas personally provokes Noah over the approved photograph, then retreats after guard intervention; he is not secretly VANTAGE leadership.')
    p.write_text(s,encoding='utf-8')
