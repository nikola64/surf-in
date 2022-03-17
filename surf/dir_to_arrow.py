import pandas as pd
import numpy as np

def dir_to_arrow(degree):
    
    '''
    # df string
    df_s = df_serie.copy()    
    #directions = np.array('N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW N'.split())
    #bins = np.arange(11.25, 372, 22.5)
    directions = np.array('N NE E SE S SW W NW N'.split())
    bins = np.arange(22.5, 383, 45)
    df_s = directions[np.digitize(df_s, bins)]  
    '''
    
    # arrow    
    directions = np.array(r'&#129139; &#129150; &#129144; &#129148; &#129145; &#129149; &#129146; &#129150; &#129139;'.split())

    bins = np.arange(22.5, 383, 45) 
    arr = directions[np.digitize(degree, bins)]  
    
    return arr