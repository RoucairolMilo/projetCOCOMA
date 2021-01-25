import numpy as np
import copy

gridSize = (10, 10)
d = 4

robots = [(2,7), (5, 4), (8, 2)]

obj = [(2,5), (5,7), (4,5), (5,3), (7,2), (8,4)]

def cost(start, tour) :
    if tour == [] :
        return 0
    subtours = []
    for etape in tour :
        st = tour.copy()
        st.remove(etape)
        subtours.append( np.abs(start[0]-etape[0]) +  np.abs(start[1]-etape[1]) + cost(etape, st))
    return min(subtours)

def utility(start, tour) :
    return 10 - cost(start, tour)

def initZones() :
    zones = []
    for rob in robots :
        offer =[]
        for o in obj :
            if np.abs(rob[0]-o[0])< d and np.abs(rob[1]-o[1])< d :
                offer.append(o)
        zones.append(offer)
    return zones

def partage(zone) :
    if(zone == []):
        return [[[], []]]
    zonebis = zone.copy()
    ajout = zonebis.pop(0)
    prevPartage = partage(zonebis)
    l =[]
    for i in prevPartage :
        gauche = copy.deepcopy(i)
        gauche[0].append(ajout)
        droite = copy.deepcopy(i)
        droite[1].append(ajout)

        l.append(gauche)
        l.append(droite)

    return l

def ZeuthenMCPNego(a1, a2, zones, utiCona1 = 0, utiCona2 = 0 ) :
    print("MCP")

    """
        off = [[ [v for v in zones[a1] if v in zones[a2]],
             []],
           [[],
            [v for v in zones[a1] if v in zones[a2]]]]
    """


    off = [[ [],
             [v for v in zones[a1] if v in zones[a2]]],
           [[v for v in zones[a1] if v in zones[a2]],
            []
            ]]   

    print("start offer :" + str(off))

    MCPround = 0
    utiFaila1 = utility(robots[a1], off[0][0])
    utiFaila2 = utility(robots[a2], off[1][1])

    utiFaila1 = max(utility(robots[a1], off[0][1]), utiCona1)
    utiFaila2 = max(utility(robots[a2], off[1][0]), utiCona2)

    print("utility if no agreement : " + str(utiFaila1) + " : " + str(utiFaila2))
    noConcession = False

    while not  noConcession and MCPround <10 :
        print("\n")
        print("etape de nego : " + str(MCPround))
        MCPround +=1

        ua1a1 = utility(robots[a1], off[0][0])
        ua1a2 = utility(robots[a1], off[1][0])
        ua2a1 = utility(robots[a2], off[0][1])
        ua2a2 = utility(robots[a2], off[1][1])
        iZ1 = 1 if (ua1a1 == utiFaila1) else (ua1a1 - ua1a2) / (ua1a1 - utiFaila1)
        iZ2 = 1 if (ua2a2 == utiFaila2) else (ua2a2 - ua2a1) / (ua2a2 - utiFaila2)
        print("Z1 : " + str(iZ1) + "  Z2 : " + str(iZ2))

        keptOffer = copy.deepcopy(off)
        noConcession = True

        PO = partage([v for v in zones[a1] if v in zones[a2]])
        offera1 = copy.deepcopy(off[0])
        offera2 = copy.deepcopy(off[1])

        keptOffera1 = copy.deepcopy(off[0])
        keptOffera2 = copy.deepcopy(off[1])

        if iZ1 <= iZ2 :
            bestconcession = -1000
            print("a1 concede")
            for tryOffer in PO:
                ua1a1 = utility(robots[a1], tryOffer[0])
                ua1a2 = utility(robots[a1], offera2[0])
                ua2a1 = utility(robots[a2], tryOffer[1])
                ua2a2 = utility(robots[a2], offera2[1])
                Z1 = 1 if (ua1a1 == utiFaila1) else (ua1a1 - ua1a2) / (ua1a1 - utiFaila1)
                Z2 = 1 if (ua2a2 == utiFaila2) else (ua2a2 - ua2a1) / (ua2a2 - utiFaila2)

                print("new Z : " + str(Z1) + " : " + str(Z2) + " pour : " + str(tryOffer))
                # print(str(ua1a2) + " > " + str(ua1a1) + " or " + str(ua2a1) + " > " + str(ua2a2) + " ?")
                print(str(ua1a2) + " > " + str(utility(robots[a1], off[1][0])) + " or " + str(ua2a1) + " > " + str(
                    utility(robots[a2], off[0][1])) + " ?")
                # if (ua1a2 > ua1a1 and Z1 > Z2 and not a1concede) or (ua2a1 > ua2a2 and Z2 > Z1 and a1concede):
                # if (ua1a2 > ua1a1 and not a1concede) or (ua2a1 > ua2a2 and a1concede):
                if ua2a1 > utility(robots[a2], off[0][1]) :
                    # gardable, mais est-elle meilleure ?
                    if ua1a1 > bestconcession:
                        keptOffera1 = copy.deepcopy(tryOffer)
                        bestconcession = ua1a1
                        print("keep at val " + str(bestconcession))
                        noConcession = False
        if iZ2 <= iZ1 :
            bestconcession = -1000
            print("a2 concede")
            for tryOffer in PO:
                ua1a1 = utility(robots[a1], offera1[0])
                ua1a2 = utility(robots[a1], tryOffer[0])
                ua2a1 = utility(robots[a2], offera1[1])
                ua2a2 = utility(robots[a2], tryOffer[1])
                Z1 = 1 if (ua1a1 == utiFaila1) else (ua1a1 - ua1a2) / (ua1a1 - utiFaila1)
                Z2 = 1 if (ua2a2 == utiFaila2) else (ua2a2 - ua2a1) / (ua2a2 - utiFaila2)

                print("new Z : " + str(Z1) + " : " + str(Z2) + " pour : " + str(tryOffer))
                # print(str(ua1a2) + " > " + str(ua1a1) + " or " + str(ua2a1) + " > " + str(ua2a2) + " ?")
                print(str(ua1a2) + " > " + str(utility(robots[a1], off[1][0])) + " or " + str(ua2a1) + " > " + str(
                    utility(robots[a2], off[0][1])) + " ?")
                # if (ua1a2 > ua1a1 and Z1 > Z2 and not a1concede) or (ua2a1 > ua2a2 and Z2 > Z1 and a1concede):
                # if (ua1a2 > ua1a1 and not a1concede) or (ua2a1 > ua2a2 and a1concede):
                if ua1a2 > utility(robots[a1], off[1][0]) :
                    # gardable, mais est-elle meilleure ?
                    if ua2a2 > bestconcession:
                        keptOffera2 = copy.deepcopy(tryOffer)
                        bestconcession = ua2a2
                        print("keep at val " + str(bestconcession))
                        noConcession = False

        #print("utility : " + str( utility(robots[a1], tryOffer[a1][a1])) + " : " + str(utility(robots[a2], tryOffer[a2][a2])))
        keptOffer = [copy.deepcopy(keptOffera1), copy.deepcopy(keptOffera2)]
        deal = False
        if(keptOffera1 == keptOffera2) :
            print("yaaaay")
            deal = True
        print("newOffer : " + str(keptOffer))

        if(noConcession or deal) :
            print("pas de nouvel accord trouvé, on arrête la négo")
            print(keptOffer)

            ostar = keptOffer
            ua1ostar = utility(robots[a1], ostar[0][0])
            ua2ostar = utility(robots[a2], ostar[0][1])

            print(ua1ostar)
            print(ua2ostar)
            print(utiFaila1)
            print(utiFaila2)

            nashprod = (ua1ostar-utiFaila1)*(ua2ostar-utiFaila2)

            print("nashprod = " + str(nashprod))

            return ua1ostar, ua2ostar, keptOffer


        off = copy.deepcopy(keptOffer)

round = 0

finished = False
Zones = initZones()

utir1, utir2, _ = ZeuthenMCPNego(0, 1, Zones)
ZeuthenMCPNego(2, 1, Zones, utiCona2= utir2 )

"""
while not finished :
    round += 1
"""


