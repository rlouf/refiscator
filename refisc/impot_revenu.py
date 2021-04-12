from typing import Dict, Tuple


def impot_revenu(revenu: float, taux: Dict[float, float]) -> Tuple[float, float]:
    """Calcul le taux global d'imposition sur les revenus et l'impôt dû.

    La calcul de l'imposition se fait en taux effectifs et non en taux
    marginaux. Lorsque le revenu tombe entre deux seuils on interpole le taux
    effectif linéairement entre les taux des deux seuils les plus proches.

    Examples
    --------

    Le taux associé au seuil `0` correspond au taux plancher. Pour simuler une
    flat tax à 13% il suffit donc de passer le dictionnaire suivant:

        >>> taux = {0: 0.13}
        >>> impot_revenu(0, taux)
        ... 0
        >>> impot_revenu(10_000, taux)
        ... 1300

    Parameters
    ----------
    revenu:
        Le revenu de l'individu ou du foyer. À la différence de l'IRPP, cet
        impôt a une conception du revenu plus large que celle du revenu du
        travail.
    taux:
        Dictionnaire qui associe à une tranche de revenus son taux global.

    """
    # si le seuil '0' n'est pas précisé nous supposons que le taux d'imposition
    # global est nul.
    if 0 not in taux:
        taux[0] = 0

    seuils = sorted(list(taux))
    for seuil_min, seuil_max in zip(seuils[:-1], seuils[1:]):
        if revenu > seuil_min and revenu < seuil_max:
            taux_min = taux[seuil_min]
            taux_max = taux[seuil_max]
            revenu_relatif = (revenu - seuil_min) / (seuil_max - seuil_min)
            taux_effectif = taux_min + revenu_relatif * (taux_max - taux_min)
            return taux_effectif, revenu * taux_effectif

    taux_effectif = taux[seuil_max]
    return taux_effectif, revenu * taux_effectif
