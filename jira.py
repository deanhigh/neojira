import json
import os
from pprint import pprint

import requests


class JiraRequest(object):
    base = os.getenv('JIRA_HTTP_URL')
    header = {'content-type': 'application/json'}
    auth = ('user.name', 'password')

    def __init__(self, url):
        self.url = url

    @classmethod
    def search(cls):
        return cls(os.path.join(JiraRequest.base, 'search'))

    @classmethod
    def projects(cls):
        return cls(os.path.join(JiraRequest.base, 'project'))

    @classmethod
    def project(cls, key):
        return cls(os.path.join(JiraRequest.base, 'project/%s' % key))

    def get(self, params=None):
        return requests.get(self.url, auth=self.auth, headers=self.header, params=params)


class PagedJiraRequest(JiraRequest):
    def __init__(self, url):
        super().__init__(url)

    def get(self, params=None):
        start = 0
        pagesize = 10
        total = start+pagesize

        l = list()

        while start < total:
            pp = {'startAt': start, 'maxResults': pagesize}
            if params:
                pp.update(params)

            js = super().get(pp).json()
            total = js['total']
            max_results = js['maxResults']
            start = start + max_results
            print("%d/%d" % (start, total))
            l.extend(js['issues'])

        with open('jira.json', mode='w') as f:
            json.dump(l, f)


def get_issues():
    pprint(PagedJiraRequest.search().get(params={'jql': 'project=24930'}).json())


def get_project():
    json = JiraRequest.project('MCPC').get().json()
    pprint(json)


if __name__ == '__main__':
    #get_project()
    get_issues()