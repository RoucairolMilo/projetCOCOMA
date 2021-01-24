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

"""
def initOffers() :
    offers = []
    for rob in robots :
        offer =[]
        for rob2 in robots :
            offerTo = []
            if rob == rob2 :
                for o in obj :
                    if np.abs(rob[0]-o[0])< d and np.abs(rob[1]-o[1])< d :
                        offerTo.append(o)
            offer.append(offerTo)
        offers.append(offer)
    return offers

def initOffersZeuthen() :
    offers = []
    for rob in range(len(robots)) :
        offer =[[] for _ in range(len(robots))]
        for o in obj :
            if np.abs(robots[rob][0] - o[0]) < d and np.abs(robots[rob][1] - o[1]) < d:
                assigned = False
                for rob2 in range(len(robots)) :
                    if np.abs(robots[rob2][0] - o[0]) < d and np.abs(robots[rob2][1] - o[1]) < d and rob != rob2 and not assigned:
                        #on lui refile
                        assigned = True
                        offer[rob2].append(o)
                if not assigned :
                    offer[rob].append(o)
        offers.append(offer)
    return offers
"""



def MCPNego(a1, a2, zones) :
    print("MCP")


    off = [[ [v for v in zones[a1] if v in zones[a2]],
             []],
           [[],
            [v for v in zones[a1] if v in zones[a2]]]]




    MCPround = 0

    utiFaila1 = utility(robots[a1], off[0][0])
    utiFaila2 = utility(robots[a2], off[1][1])

    #utilité de l'agent 1 suivant l'offre de l'agent1 ...
    ua1a1 = utility(robots[a1], off[0][0])
    ua1a2 = utility(robots[a1], off[1][0])
    ua2a1 = utility(robots[a2], off[0][1])
    ua2a2 = utility(robots[a2], off[1][1])

    print("start utility : " + str(ua1a1) + " : " + str(ua2a2))
    noConcession = False
    while not  noConcession :
        print("\n")
        print("etape de nego : " + str(MCPround))
        MCPround +=1

        ua1a1 = utility(robots[a1], off[0][0])
        ua1a2 = utility(robots[a1], off[1][0])
        ua2a1 = utility(robots[a2], off[0][1])
        ua2a2 = utility(robots[a2], off[1][1])
        Z1 = 1 if  (ua1a1 == utiFaila1) else (ua1a1 - ua1a2)/(ua1a1-utiFaila1)
        Z2 = 1 if  (ua2a2 == utiFaila2) else (ua2a1 - ua2a2)/(ua2a2-utiFaila2)

        print("Z1 : " + str(Z1) + "  Z2 : " + str(Z2))

        keptOffer = copy.deepcopy(off)
        noConcession = True
        if Z1 < Z2 or (Z1 == Z2 and np.random.rand() < 0.5) :
            print("a1 concede")
            #a1 doit prendre un objectif à a2
            bestconcession = utility(robots[a1], off[0][0])
            for el in off[0][0] :
                tryOffer = copy.deepcopy(off)
                tryOffer[0][0].remove(el)
                tryOffer[0][1].append(el)

                ua1a1 = utility(robots[a1], tryOffer[0][0])
                ua1a2 = utility(robots[a1], tryOffer[1][0])
                ua2a1 = utility(robots[a2], tryOffer[0][1])
                ua2a2 = utility(robots[a2], tryOffer[1][1])
                Z1 = 1 if (ua1a1 == utiFaila1) else (ua1a1 - ua1a2) / (ua1a1 - utiFaila1)
                Z2 = 1 if (ua2a2 == utiFaila2) else (ua2a1 - ua2a2) / (ua2a2 - utiFaila2)

                print("new Z : " + str(Z1) + " : " + str(Z2) + " pour : " + str(tryOffer))
                print(str(ua1a2) + " > " + str(ua1a1) + "  or  " +str(ua2a1)+ " > " + str(ua2a2) + " ?")
                if Z2 >= Z1:
                    # gardable, mais est-elle meilleure ?
                    if bestconcession == 0:
                        keptOffer = copy.deepcopy(tryOffer)
                        bestconcession = ua1a1
                        noConcession = False
                    else:
                        if ua1a1 > bestconcession:
                            keptOffer = copy.deepcopy(tryOffer)
                            bestconcession = ua1a1
                            noConcession = False

        else :
            print("a2 concede")
            bestconcession = utility(robots[a2], off[1][1])
            for el in off[1][1]:
                tryOffer = copy.deepcopy(off)
                tryOffer[1][1].remove(el)
                tryOffer[1][0].append(el)

                ua1a1 = utility(robots[a1], tryOffer[0][0])
                ua1a2 = utility(robots[a1], tryOffer[1][0])
                ua2a1 = utility(robots[a2], tryOffer[0][1])
                ua2a2 = utility(robots[a2], tryOffer[1][1])
                Z1 = 1 if (ua1a1 == utiFaila1) else (ua1a1 - ua1a2) / (ua1a1 - utiFaila1)
                Z2 = 1 if (ua2a2 == utiFaila2) else (ua2a1 - ua2a2) / (ua2a2 - utiFaila2)
                # print("new offer : " + str(tryOffer))
                print("new Z : " + str(Z1) + " : " + str(Z2) + " pour : " + str(tryOffer))
                print(str(ua1a2) + " > " + str(ua1a1) + "  or  " + str(ua2a1) + " > " + str(ua2a2) + " ?")
                if Z1 >= Z2:
                    # gardable, mais est-elle meilleure ?
                    if bestconcession == 0:
                        keptOffer = copy.deepcopy(tryOffer)
                        bestconcession = ua2a2
                        noConcession = False
                    else:
                        if ua2a2 > bestconcession:
                            keptOffer = copy.deepcopy(tryOffer)
                            bestconcession = ua2a2
                            noConcession = False


        #print("utility : " + str( utility(robots[a1], tryOffer[a1][a1])) + " : " + str(utility(robots[a2], tryOffer[a2][a2])))
        print("newOffer : " + str(keptOffer))
        if(noConcession) :
            print("pas de nouvel accord trouvé, on arrête la négo")
            print(keptOffer)

            ostar = keptOffer
            ua1ostar = utility(robots[0], ostar[0][0])
            ua2ostar = utility(robots[1], ostar[0][1])

            print(ua1ostar)
            print(ua2ostar)
            print(utiFaila1)
            print(utiFaila2)

            nashprod = (ua1ostar-utiFaila1)*(ua2ostar-utiFaila2)

            print("nashprod = " + str(nashprod))

            return keptOffer #on suppose que c'est un accord viable TODO : tester ça


        off = copy.deepcopy(keptOffer)







round = 0

finished = False
Zones = initZones()

MCPNego(0, 1, Zones)


"""
while not finished :
    round += 1
"""


