import numpy as np

def tb(D_eq):
    '''
    This implements the Thurai and Bringi drop shape relationship.
    Input: Equivalent Volume Drop Diameter
    Returns: Major/Minor Axis
    '''
    if D_eq < 0.7:
        return 1.0;
    elif D_eq < 1.5:
        return 1.173 - 0.5165*D_eq + 0.4698*D_eq**2 - 0.1317*D_eq**3 - \
                8.5e-3*D_eq**4
    else:
        return 1.065 - 6.25e-2*D_eq - 3.99e-3*D_eq**2 + 7.66e-4*D_eq**3 - \
                4.095e-5*D_eq**4 

def pb(D_eq):
    '''
    This implements the Pruppacher and Beard drop shape relationship
    Usage: pb(D_eq)
    Input: Equivalent Volume Drop Diameter
    Returns: Major/Minor Axis
    
    '''
    return 1.03-0.062*D_eq

def bc(D_eq):
    '''
    This implements the Beard and Chuang drop shape relationship.
    Input: Equivalent Volume Drop Diameter
    Returns: Major/Minor Axis
    '''
    return 1.0048 + 5.7e-04 *np.power(D_eq,1) - 2.628e-02 * np.power(D_eq,2) + \
            3.682e-03*np.power(D_eq,3) -1.677e-04 *np.power(D_eq,4)
