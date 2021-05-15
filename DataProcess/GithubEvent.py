"""
GithubEvent类,记录GitHub事件的信息
"""
class GithubEvent(object):
    def __init__(self,json):
        super(GithubEvent, self,json).__init__()
        self.data=json
        self.type=json["type"]
        self.sha=json["sha"]
        self.message=json["message"]
        self.parents=json["parents"]
        self.files=json["files"]


