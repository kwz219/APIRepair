"""
GithubEvent类,记录GitHub事件的信息
"""

import json
import urllib.request as request

class GithubEvent(object):
    def __init__(self,json):
        super(GithubEvent, self).__init__()
        self.id=json["id"]
        self.actor_info=json["actor"]
        self.repo_info=json["repo"]

class PushEvent(GithubEvent):
    def __init__(self,json):
        super(PushEvent, self).__init__(json)
        self.sha=json["payload"]["commits"][0]["sha"]
        self.parent_sha=""
        self.files=[]
        self.message=json["payload"]["commits"][0]["message"]
        self.url=json["payload"]["commits"][0]["url"]
        self.readURL()
    def readURL(self):
        html=request.urlopen(self.url)
        hjson=json.loads(html.read())
        print(hjson.keys())
        self.parent_sha=hjson['parents'][0]['sha']
        self.files=hjson['files']
        print(hjson)
    def getPatches(self):
        patches=[]
        for file in self.files:
            print(file)
            patch={"patch":file["patch"],"rawurl":file["raw_url"],"parent_rawurl":file["raw_url"].replace(self.sha,self.parent_sha)}
            patches.append(patch)
        return patches

    def printAll(self):
        print("id:",self.id)
        print("actorinfo:",self.actor_info)
        print("repoinfo:",self.repo_info)
        print("sha",self.sha)
        print("message",self.message)
        print("url",self.url)

def testPushEvent():
    test_json={"id":"2489651169","type":"PushEvent","actor":{"id":8770348,"login":"HouseMonitor","gravatar_id":"","url":"https://api.github.com/users/HouseMonitor","avatar_url":"https://avatars.githubusercontent.com/u/8770348?"},"repo":{"id":24030380,"name":"HouseMonitor/Logs2014-2015","url":"https://api.github.com/repos/HouseMonitor/Logs2014-2015"},"payload":{"push_id":536864036,"size":1,"distinct_size":1,"ref":"refs/heads/master","head":"3e84515dc75cd395fc74549b2f2647885563f3cf","before":"0b8540a22ee6d99b0d068874597c4db2aed15776","commits":[{"sha":"3e84515dc75cd395fc74549b2f2647885563f3cf","author":{"email":"17e72c8f1b0781cefad8c299a70b47a752ed01a6@gmail.com","name":"Matej Drolc"},"message":"automated commit","distinct":"true","url":"https://api.github.com/repos/HouseMonitor/Logs2014-2015/commits/3e84515dc75cd395fc74549b2f2647885563f3cf"}]},"public":"true","created_at":"2015-01-01T15:00:12Z"}
    pushevent=PushEvent(json=test_json)
    #pushevent.printAll()
    patches=pushevent.getPatches()
    for pa in patches:
        print(pa)

if __name__ =="__main__":
    testPushEvent()


