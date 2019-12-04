from repository.neo4j import Neo4jRepository
from py2neo import Node, Relationship
from util.github import filter_props

class PullRepository( Neo4jRepository):

    def __init__( self, db):
        self.db = db

    def save(self, pull):
        tx = self.db.begin()
        # Nó da pull
        unnodepull = Node("pull", **filter_props(pull))
        tx.create(unnodepull)
        # Nó do usuário
        unnodeuser = Node("user", **filter_props(pull["user"]))
        tx.merge(unnodeuser, "user", "id")
        reluserpull = Relationship(unnodeuser, "CRIOU", unnodepull)
        tx.create(reluserpull)
        # Condicional
        if("merged_by" in pull):
            # Nó do merged_by
            unnodemergedby = Node("user", **filter_props(pull["merged_by"]))
            tx.merge(unnodemergedby, "user", "id")
            relmergedbypull = Relationship(unnodemergedby, "DEU_MERGE_EM", unnodepull)
            tx.create(relmergedbypull)
        # Condicional
        if(pull["milestone"]):
            # nó da milestone
            unnodemilestone = Node("milestone", **filter_props(pull["milestone"]))
            tx.merge(unnodemilestone, "milestone", "id")
            relmilestonepull = Relationship(unnodemilestone, "CONTÉM", unnodepull)
            tx.create(relmilestonepull)
            # nó do criador do milestone
            unnodemilestonecreator = Node("user", **filter_props(pull["milestone"]["creator"]))
            tx.merge(unnodemilestonecreator, "user", "id")
            relcreatormilestone = Relationship(unnodemilestonecreator, "CRIOU", unnodemilestone)
            tx.create(relcreatormilestone)
        # Nós das labels
        lsnodelabel = [
            Node("label", **filter_props(label)) 
            for label in pull['labels']
        ]
        for nodelabel in lsnodelabel:
            tx.merge(nodelabel, "label", "id")
            rellabelpull = Relationship(nodelabel, "ROTULA", unnodepull)
            tx.create(rellabelpull)
        # Nós dos assignees
        lsnodeassignee = [
            Node("user", **filter_props(assignee))
            for assignee in pull["assignees"]
        ]
        for nodeassignee in lsnodeassignee:
            tx.merge(nodeassignee, "user", "id")
            relassigneepull = Relationship(nodeassignee, "ADMINISTRA", unnodepull)
            tx.create(relassigneepull)
        # Nós dos reviewers
        lsnodereviewers = [
            Node("user", **filter_props(reviewer))
            for reviewer in pull["requested_reviewers"]
        ]
        for nodereviewer in lsnodereviewers:
            tx.merge(nodereviewer, "user", "id")
            relreviewerissue = Relationship(nodereviewer, "CHAMADO_PARA_REVISAR", unnodepull)
            tx.create(relreviewerissue)
        # Nós dos teams
        lsnodeteams = [
            Node("team", **filter_props(team))
            for team in pull["requested_teams"]
        ]
        for nodeteam in lsnodeteams:
            tx.merge(nodeteam, "team", "id")
            relteamissue = Relationship(nodeteam, "CHAMADO_PARA_REVISAR", unnodepull)
            tx.create(relteamissue)
        # Concluir
        tx.commit()



