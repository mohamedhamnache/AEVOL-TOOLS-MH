import requests
import json
import config
class Helper ():
    def __init__(self):
        pass

    def SiteList(self):
        sites =[]
        r = requests.get(config.G5K_API_BASE_URL+'/sites/', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))
        json_data = json.loads(r.text)
        items =json_data['items']
        for item in items :
            sites.append(item['name'])
        return sites



    def reservationsSites(self):
        reservationList =[]
        sites = self.SiteList()
        #print(sites)
        for site in sites :
            s = site.split("-")
            site =s[0]
            reservations =0
            r = requests.get(config.G5K_API_BASE_URL+'/sites/'+site.lower()+'/status', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))         
            json_data = json.loads(r.text)
            nodes= json_data['nodes']
            for nodeName in nodes :
                node=nodes[nodeName]             
                reservations= reservations + len(node['reservations'])
            reservationList.append(reservations)
        return reservationList

    def clusterList(self):
        result=[]
        sites = self.SiteList()
        for site in sites:
            s = site.split("-")
            site =s[0]
            r =requests.get(config.G5K_API_BASE_URL+'/sites/'+site.lower()+'/clusters/', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))
            json_data = json.loads(r.text)
            items = json_data['items']             
            clusters=[]    
            for item in items :    
                clusters.append(item['uid'])
            result.append({
                "site":site,
                "clusters" :clusters})
        return result
            
    def nodesPerSite(self):
        siteCluster = self.clusterList()
        nbNodes =0 
        nodesSite =[]    
        for item in siteCluster :
            for cluster in item['clusters']:
                r =requests.get(config.G5K_API_BASE_URL+'/sites/'+item['site'].lower()+'/clusters/'+cluster+'/nodes/', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))
                json_data = json.loads(r.text)
                #print(json_data['total'])
                nbNodes = nbNodes + int(json_data['total'])
            nodesSite.append(nbNodes)
            nbNodes =0
        return nodesSite

    def pickSite(self):
        usageRates =[]
        pickedSite =""
        rate =0
        rateMin =1000
        i=0
        sites = self.SiteList()
        reservations = self.reservationsSites()
        nodeSites = self.nodesPerSite()
        for site in sites :
            rate =reservations[i]/nodeSites[i]
            usageRates.append(rate)
            if (rate<rateMin):
                rateMin =rate
                pickedSite = site
            i = i+1
        return pickedSite,usageRates,usageRates



            
