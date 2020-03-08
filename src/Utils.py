import re
import pandas as pd

class Utils:

    ##########################
    ## Fuction: Punctuation ##
    ##########################
    ## • Remove punctuation ##
    ##########################
    def punctuation(self, var):
        
        if type(var) == str:
            var = pd.Series(var)
        
        var = var.apply(lambda x: re.sub('[ÁÂÀÃ]', 'A', x.upper()))
        var = var.apply(lambda x: re.sub('[ÉÊ]'  , 'E', x.upper()))
        var = var.apply(lambda x: re.sub('[Í]'   , 'I', x.upper()))
        var = var.apply(lambda x: re.sub('[ÓOO]' , 'O', x.upper()))
        var = var.apply(lambda x: re.sub('[ÚÜ]'  , 'U', x.upper()))
        var = var.apply(lambda x: re.sub('[Ç]'   , 'C', x.upper()))
        var = var.apply(lambda x: re.sub('[Ñ]'   , 'N', x.upper()))
        return var
    ##########################
