from classes import GraphicNovel

novel_name = "Batman: The Court of Owls"
issues = ["Batman (2011) #1", 
          "Batman (2011) #2",
          "Batman (2011) #3",
          "Batman (2011) #4",
          "Batman (2011) #5",
          "Batman (2011) #6",
          "Batman (2011) #7"]
writers = ["Scott Snyder"]
pencillers = ["Greg Capullo"]
inkers = ["Jonathan Glapion"]
colorists = ["FCO Plascencia"]
letterers = ["Richard Starkings", "Jimmy Betancourt"]
editors = ["Mike Marts", "Janelle Asselin", "Katie Kubert", "Harvey Richards"]

batman_court = GraphicNovel(novel_name, issues, writers, pencillers, 
                            inkers, colorists, letterers, editors)

print(batman_court.name)