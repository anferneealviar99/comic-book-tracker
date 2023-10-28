class ComicBookIssue:
    def __init__(self, name, volume, number, publisher, writer="", penciller="", inker="", colorist="", letterer="", editor="", trade_id=0):
        self.series = name 
        self.volume = volume
        self.number = number
        self.publisher = publisher
        self.writer = writer
        self.penciller = penciller 
        self.inker = inker
        self.colorist = colorist
        self.letterer = letterer
        self.editor = editor 
        
class Trade:
    def __init__(self, name, publisher, issues, writers, pencillers, inkers, colorists, letterers, editors=""):
        self.name = name
        self.publisher = publisher
        self.issues = issues
        self.writers = writers
        self.pencillers = pencillers 
        self.inkers = inkers
        self.colorists = colorists
        self.letterers = letterers 
        self.editors = editors
    


class InvalidComicIssueException(Exception):
    # Raised when issue details retrieved from Metron is None
    pass


#TODO change classes 