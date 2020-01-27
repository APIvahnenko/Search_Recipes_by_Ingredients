#!/usr/bin/env python3

class WebContentsParser:
    webContentsFile = None
    
    def __int__(self, webContentsFile):
        self.OpenWebContentsFile(webContentsFile)
        
        # Create Preprocessor object.
        # Create Database object.


    
    def __del__(self):
        self.CloseWebContentsFile()
    
        # Delete Database object?
        # Delete Database object?
    
    def OpenWebContentsFile(self, webContentsFile):
        if self.webContentsFile != None:
            return None
        
        self.webContentsFile = webContentsFile
        
        try:
            self.webContentsFile = open(self.webContentsFile)
        except:
            exit('ERROR: %s cannot be opened.' % self.webContentsFile)
    
    def CloseWebContentsFile(self):
        self.webContentsFile.close()
        self.webContentsFile = None
        
    def ParseWebContents(self):
        # Get web page URL and title.
        # Get web page content.
        # Call Preprocessor.TagWebPageUrl().
        # Call Preprocessor.TagWebPageTitle().
        # Call Preprocessor.TagWebPageContent().
        # Call Preprocessor.CombineWebPageUrlTitleAndContent().
        # Call Preprocessor.Tokenise().
        # Call Preprocessor.CaseFold().
        # Call Preprocessor.RemoveStopWords().
        # Call Preprocessor.PorterStem().
        # Call Preprocessor.AssignPositionsInWebPage().
        # Call Preprocessor.GetUrlPositionsInWebPage().
        # Call Preprocessor.GetTitlePositionsInWebPage().
        # Call Preprocessor.GetLinkPositionsInWebPage().
        # Call Preprocessor.AddToTermSequence() for web page URL, title, and content.
        # Call Preprocessor.SortTermSequence().
        # Call Database.AddToTermIndexTable() to add sorted term sequence.
        # Call Database.AddToWebPageInfoTable() to add web page information.
        # Continue to parse and process next web page.
        
        return None
