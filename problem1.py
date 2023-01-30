from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from folium import IFrame
import folium
import math
import codecs
import sys
from folium.plugins import FloatImage

geolocator = Nominatim(user_agent="python121")
image_file = 'legends white bg.PNG'


class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def printSolution(self, dist):
        print()
        print("Minimum possible distance from Home to Destination is :" ,round(dist[1], 3), " kilometres")


    def minDistance(self, dist, sptSet):
        min = float("inf")
        min_index = 0

        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def dijkstra(self, src):
        dist = [float("inf")] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):

            u = self.minDistance(dist, sptSet)

            sptSet[u] = True

            for v in range(self.V):

                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]

        self.printSolution(dist)




class Map:
    citylink = geolocator.reverse("3.0319924887507144, 101.37344116244806")
    poslaju = geolocator.reverse("3.112924170027219, 101.63982650389863")
    gdex = geolocator.reverse("3.265154613796736, 101.68024844550233")
    jandt = geolocator.reverse("2.9441205329488325, 101.7901521759029 ")
    dhl = geolocator.reverse("3.2127230893650065, 101.57467295692778")
    tooltiphome = "From address: "
    tooltipdest = "To address: "

    g = Graph(7)

    citylinkpoints = []
    poslajupoints = []
    gdexpoints = []
    jandtpoints = []
    dhlpoints = []

    map1 = folium.Map(
        location=[3.1390, 101.6869],
        tiles='cartodbpositron',
        zoom_start=10,
    )


    def __init__(self):
        None

    def markhubs(self):
        folium.Marker(location=[self.citylink.latitude, self.citylink.longitude], tooltip="City-link Express").add_to(self.map1)
        folium.Marker(location=[self.poslaju.latitude, self.poslaju.longitude], tooltip="PosLaju").add_to(self.map1)
        folium.Marker(location=[self.gdex.latitude, self.gdex.longitude], tooltip="GDEX").add_to(self.map1)
        folium.Marker(location=[self.jandt.latitude, self.jandt.longitude], tooltip="J&T Express").add_to(self.map1)
        folium.Marker(location=[self.dhl.latitude, self.dhl.longitude], tooltip="DHL").add_to(self.map1)
        self.map1.save("maphubs.html")

    def markhomedest(self, locationhome, locationdest):
        folium.CircleMarker(location=[locationhome.latitude, locationhome.longitude],
                            tooltip=self.tooltiphome + locationhome.address, radius=20, color="crimson", fill=True).add_to(self.map1)
        folium.CircleMarker(location=[locationdest.latitude, locationdest.longitude],
                            tooltip=self.tooltipdest + locationdest.address, radius=20, color="green", fill=True).add_to(self.map1)

    def setpointsfordelivery(self, homeaddress, destaddress, finaldistances, minindex):
        self.citylinkpoints.append(tuple([homeaddress.latitude, homeaddress.longitude]))
        self.citylinkpoints.append(tuple([self.citylink.latitude, self.citylink.longitude]))
        self.citylinkpoints.append(tuple([destaddress.latitude, destaddress.longitude]))

        self.poslajupoints.append(tuple([homeaddress.latitude, homeaddress.longitude]))
        self.poslajupoints.append(tuple([self.poslaju.latitude, self.poslaju.longitude]))
        self.poslajupoints.append(tuple([destaddress.latitude, destaddress.longitude]))

        self.gdexpoints.append(tuple([homeaddress.latitude, homeaddress.longitude]))
        self.gdexpoints.append(tuple([self.gdex.latitude, self.gdex.longitude]))
        self.gdexpoints.append(tuple([destaddress.latitude, destaddress.longitude]))

        self.jandtpoints.append(tuple([homeaddress.latitude, homeaddress.longitude]))
        self.jandtpoints.append(tuple([self.jandt.latitude, self.jandt.longitude]))
        self.jandtpoints.append(tuple([destaddress.latitude, destaddress.longitude]))

        self.dhlpoints.append(tuple([homeaddress.latitude, homeaddress.longitude]))
        self.dhlpoints.append(tuple([self.dhl.latitude, self.dhl.longitude]))
        self.dhlpoints.append(tuple([destaddress.latitude, destaddress.longitude]))

        self.markdeliveryroutes(finaldistances, minindex)

    def markdeliveryroutes(self, finaldistances, minindex):
        folium.PolyLine(self.citylinkpoints, color="#0AB68B", weight=20, opacity=0.5,
                        tooltip="Route for City-link Express : Distance " + str(finaldistances[0]) + "km").add_to(self.map1)
        folium.PolyLine(self.poslajupoints, color="#FF7400", weight=20, opacity=0.5,
                        tooltip="Route for Pos Laju : Distance " + str(finaldistances[1]) + "km").add_to(self.map1)
        folium.PolyLine(self.gdexpoints, color="#03254C", weight=20, opacity=0.5,
                        tooltip="Route for GDEX : Distance " + str(finaldistances[2]) + "km").add_to(self.map1)
        folium.PolyLine(self.jandtpoints, color="#F80000", weight=20, opacity=0.5,
                        tooltip="Route for J&T : Distance " + str(finaldistances[3]) + "km").add_to(self.map1)
        folium.PolyLine(self.dhlpoints, color="#FFFb05", weight=20, opacity=0.5,
                        tooltip="Route for DHL : Distance " + str(finaldistances[4]) + "km").add_to(self.map1)

        if minindex == 0:
            folium.PolyLine(self.citylinkpoints, color="green", weight=5, opacity=1, tooltip="Best Route").add_to(self.map1)
        elif minindex == 1:
            folium.PolyLine(self.poslajupoints, color="green", weight=5, opacity=1, tooltip="Best Route").add_to(self.map1)
        elif minindex == 2:
            folium.PolyLine(self.gdexpoints, color="green", weight=5, opacity=1, tooltip="Best Route").add_to(self.map1)
        elif minindex == 3:
            folium.PolyLine(self.jandtpoints, color="green", weight=5, opacity=1, tooltip="Best Route").add_to(self.map1)
        elif minindex == 4:
            folium.PolyLine(self.dhlpoints, color="green", weight=5, opacity=1, tooltip="Best Route").add_to(self.map1)

    def printmap(self):
        FloatImage(image_file, bottom=-5, left=76).add_to(self.map1)
        self.map1.save("mapdeliverypath.html")

class Customer(Map):
    homeaddress = ""
    destaddress = ""
    directdistance = None
    citylinkdistance= [0] * 3
    poslajudistance = [0] * 3
    gdexdistance = [0] * 3
    jandtdistance = [0] * 3
    dhldistance = [0] * 3
    finaldistances = []
    rankdist = []
    rankfinal = []
    distancescore = {"citylink" : 0,
                     "dhl" : 0,
                     "poslaju" : 0,
                     "jnt" : 0,
                     "gdex" : 0,
                     }
    minindex = 0
    m = Map()
    m.markhubs()
    rankcitylink = None
    rankposlaju = None
    rankgdex = None
    rankjnt = None
    rankdhl = None






    def __int__(self):
        self.m.markhubs()

    def sethomedest(self, homestring, deststring):
        self.homeaddress = geolocator.geocode(homestring)
        self.destaddress = geolocator.geocode(deststring)
        self.m.markhomedest(self.homeaddress, self.destaddress)

    def finddirectdistance(self):
        self.directdistance = geodesic((self.homeaddress.latitude, self.homeaddress.longitude), (self.destaddress.latitude, self.destaddress.longitude)).kilometers
        self.directdistance = round(self.directdistance, 3)
        print("Direct Distance between \n\"" + self.homeaddress.address + "\"" + " and")
        print("\"" + self.destaddress.address + "\" is " + str(self.directdistance) + " kilometres")

    def computealldistances(self):
        self.citylinkdistance[1] = round(geodesic((self.homeaddress.latitude, self.homeaddress.longitude),
                                           (self.citylink.latitude, self.citylink.longitude)).kilometers, 3)
        self.citylinkdistance[2] = round(geodesic((self.destaddress.latitude, self.destaddress.longitude),
                                           (self.citylink.latitude, self.citylink.longitude)).kilometers, 3)
        self.citylinkdistance[0] = round(self.citylinkdistance[1] + self.citylinkdistance[2],3)

        self.poslajudistance[1] = round(geodesic((self.homeaddress.latitude, self.homeaddress.longitude),
                                           (self.poslaju.latitude, self.poslaju.longitude)).kilometers, 3)
        self.poslajudistance[2] = round(geodesic((self.destaddress.latitude, self.destaddress.longitude),
                                           (self.poslaju.latitude, self.poslaju.longitude)).kilometers, 3)
        self.poslajudistance[0] = round((self.poslajudistance[1] + self.poslajudistance[2]), 3)

        self.gdexdistance[1] = round(geodesic((self.homeaddress.latitude, self.homeaddress.longitude),
                                           (self.gdex.latitude, self.gdex.longitude)).kilometers, 3)
        self.gdexdistance[2] = round(geodesic((self.destaddress.latitude, self.destaddress.longitude),
                                           (self.gdex.latitude, self.gdex.longitude)).kilometers, 3)
        self.gdexdistance[0] = round(self.gdexdistance[1] + self.gdexdistance[2], 3)

        self.jandtdistance[1] = round(geodesic((self.homeaddress.latitude, self.homeaddress.longitude),
                                           (self.jandt.latitude, self.jandt.longitude)).kilometers, 3)
        self.jandtdistance[2] = round(geodesic((self.destaddress.latitude, self.destaddress.longitude),
                                           (self.jandt.latitude, self.jandt.longitude)).kilometers, 3)
        self.jandtdistance[0] = round(self.jandtdistance[1] + self.jandtdistance[2], 3)

        self.dhldistance[1] = round(geodesic((self.homeaddress.latitude, self.homeaddress.longitude),
                                           (self.dhl.latitude, self.dhl.longitude)).kilometers, 3)
        self.dhldistance[2] = round(geodesic((self.destaddress.latitude, self.destaddress.longitude),
                                           (self.dhl.latitude, self.dhl.longitude)).kilometers, 3)
        self.dhldistance[0] = round(self.dhldistance[1] + self.dhldistance[2], 3)

        self.finaldistances = [self.citylinkdistance[0], self.poslajudistance[0], self.gdexdistance[0], self.jandtdistance[0], self.dhldistance[0]]
        self.minindex = self.finaldistances.index(min(self.finaldistances))

    def printalldistances(self):
        self.computealldistances()
        print("\nDistances with respect to hubs: ")
        print("\nCityLink")
        print("Total distance: " + str(self.citylinkdistance[1]) + " + " + str(self.citylinkdistance[2]) + " = " + str(
            self.citylinkdistance[0]) + " kilometres")
        print("\nPosLaju")
        print("Total distance: " + str(self.poslajudistance[1]) + " + " + str(self.poslajudistance[2]) + " = " + str(self.poslajudistance[0]) + " kilometres")
        print("\nGDEX")
        print("Total distance: " + str(self.gdexdistance[1]) + " + " + str(self.gdexdistance[2]) + " = " + str(self.gdexdistance[0]) + " kilometres")
        print("\nJ&T")
        print("Total distance: " + str(self.jandtdistance[1]) + " + " + str(self.jandtdistance[2]) + " = " + str(self.jandtdistance[0]) + " kilometres")
        print("\nDHL")
        print("Total distance: " + str(self.dhldistance[1]) + " + " + str(self.dhldistance[2]) + " = " + str(self.dhldistance[0]) + " kilometres")

    def initgraph(self):
        self.g.graph = [[0, 0, self.citylinkdistance[1], self.poslajudistance[1], self.gdexdistance[1], self.jandtdistance[1], self.dhldistance[1]],

                   [0, 0, 0, 0, 0, 0, 0],

                   [0, self.citylinkdistance[2], 0, 0, 0, 0, 0],

                   [0, self.poslajudistance[2], 0, 0, 0, 0, 0],

                   [0, self.gdexdistance[2], 0, 0, 0, 0, 0],

                   [0, self.jandtdistance[2], 0, 0, 0, 0, 0],

                   [0, self.dhldistance[2], 0, 0, 0, 0, 0],

                   ];
        self.g.dijkstra(0)

    def setpointsfordelivery(self):
        self.m.setpointsfordelivery(self.homeaddress, self.destaddress, self.finaldistances, self.minindex)

    def printfinaldist(self):
        print(self.finaldistances)

    def printmap(self):
        self.m.printmap()

    def getrankfinal(self):
        self.distdict = {"citylink": self.citylinkdistance[0],
                         "poslaju": self.poslajudistance[0],
                         "gdex": self.gdexdistance[0],
                         "jnt": self.jandtdistance[0],
                         "dhl": self.dhldistance[0]}
        score = 5
        for i in range(5):
            current = min(self.distdict, key=self.distdict.get)

            self.distancescore[current] = score
            self.distdict.pop(current)
            score -= 1

        return self.distancescore




    def calcscore(self):
        self.distancescore = { "citylink" : self.rankfinal[0]}