import pandas as pd
import numpy as np

def dir_to_text(degree):
    
    # text    
    directions = np.array('N NE E SE S SW W NW N'.split())
    bins = np.arange(22.5, 383, 45) 
    arr = directions[np.digitize(degree, bins)]  
    
    return arr