class TrackerEntry:
    def __init__(self, comicBookDetails, status, rating=None, review=None):
        self.comicBookDetails = comicBookDetails
        self.status = status 
        self.rating = rating 
        self.review = review  

class GraphicNovel:
    def __init__(self, name, issues, writers, pencillers, inkers, colorists, letterers, editors):
        self.name = name
        self.issues = issues
        self.writers = writers
        self.pencillers = pencillers 
        self.inkers = inkers
        self.colorists = colorists
        self.letterers = letterers 
    
class ComicBookIssue:
    def __init__(self, name, publisher, writer, penciller, inker, colorist, letterer, editor):
        self.name = name 
        self.publisher = publisher
        self.writer = writer
        self.penciller = penciller 
        self.inker = inker
        self.colorist = colorist
        self.letterer = letterer
        self.editor = editor 

#TODO change classes 