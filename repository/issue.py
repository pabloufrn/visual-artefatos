from repository.neo4j import Neo4jRepository
from py2neo import Node, Relationship
from util.github import filter_props


class IssueRepository( Neo4jRepository):

    def __init__( self, db):
        self.db = db

    def save(self, issue):
        tx = self.db.begin()
        # Nó da issue
        unnodeissue = Node("pull" if "pull_request" in issue else "issue", **filter_props(issue))
        tx.create(unnodeissue)
        # Nó do usuário
        unnodeuser = Node("user", **filter_props(issue["user"]))
        tx.merge(unnodeuser, "user", "id")
        reluserissue = Relationship(unnodeuser, "CRIOU", unnodeissue)
        tx.create(reluserissue)
        # Condicional
        if(issue["milestone"]):
            # nó da milestone
            unnodemilestone = Node("milestone", **filter_props(issue["milestone"]))
            tx.merge(unnodemilestone, "milestone", "id")
            relmilestoneissue = Relationship(unnodemilestone, "CONTÉM", unnodeissue)
            tx.create(relmilestoneissue)
            # nó do criador do milestone
            unnodemilestonecreator = Node("user", **filter_props(issue["milestone"]["creator"]))
            tx.merge(unnodemilestonecreator, "user", "id")
            relcreatormilestone = Relationship(unnodemilestonecreator, "CRIOU", unnodemilestone)
            tx.create(relcreatormilestone)
        # Nós das labels
        lsnodelabel = [
            Node("label", **filter_props(label)) 
            for label in issue['labels']
        ]
        for nodelabel in lsnodelabel:
            tx.merge(nodelabel, "label", "id")
            rellabelissue = Relationship(nodelabel, "ROTULA", unnodeissue)
            tx.create(rellabelissue)
        # Nós dos assignees
        lsnodeassignee = [
            Node("user", **filter_props(assignee))
            for assignee in issue["assignees"]
        ]
        for nodeassignee in lsnodeassignee:
            tx.merge(nodeassignee, "user", "id")
            relassigneeissue = Relationship(nodeassignee, "ADMINISTRA", unnodeissue)
            tx.create(relassigneeissue)
        # Concluir
        tx.commit()



