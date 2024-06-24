"""
Scripts to transform policyengine variables to taxsim
"""

def export_single_household( policyengine_situation : dict ) -> dict :
    """
    Takes policyengine 'situation' and converts to taxsim variables
    Args:
        policyengine_situation    : structured dict with policyengine household
    Returns:
        dict with named taxsim variables
    """
    output = dict()
    return output