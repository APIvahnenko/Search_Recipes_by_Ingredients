#!/usr/bin/env python3

import re
from stemming.porter2 import stem
from operator import itemgetter

class Preprocessor:    
    def TagWebPageUrl(self):
        # Add URLSTART and URLEND.
        
        return None
    
    def TagWebPageTitle(self):
        # Add TITLESTART and TITLEEND.
        
        return None
    
    def TagWebPageContent(self):
        # Add CONTENTSTART, CONTENTEND, LINKSTART, and LINKEND.
        
        return None
    
    def CombineWebPageUrlTitleAndContent(self):
        # Combine tagged URL, tagged title, and tagged content.
        
        return None
    
    def Tokenise(self, line):
        # Do not tokenise special tag words.
        # Refer previous codes.
        
        return None
        
    def CaseFold(self, tokens):
        # Do not case fold special tag words.
        # Refer previous codes.
        
        return None
        
    def RemoveStopWords(self, tokens, stopWords):
        # Do not remove special tag words.
        # Refer previous codes.
        
        return None
        
    def PorterStem(self, tokens):
        # Do not Porter stem special tag words.
        # Refer previous codes.
        
        return None
    
    def AssignPositionsInWebPage(self, terms):
        # Skip special tag words.
        # Refer previous codes.
        
        return None
    
    def GetUrlPositionsInWebPage(self):        
        return None
        
    def GetTitlePosisitionsInWebPage(self):
        return None
        
    def GetLinkPositionsInWebPage(self):
        return None
    
    def AddToTermSequence(self, termsWithPositions, webPageId, termSequence):
        # Refer prevous codes.
        
        return None
        
    def SortTermSequence(self, termSequence):
        # Refer previous codes.
        
        return None
    
    










