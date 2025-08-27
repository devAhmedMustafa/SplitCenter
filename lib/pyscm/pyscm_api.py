from . import pyscm

class PyscmApi:

    @staticmethod
    def version():
        return pyscm.version()

    @staticmethod
    def init(repoPath: str):
        return pyscm.init(repoPath)

    @staticmethod
    def add(repoPath: str, filePath: str):
        return pyscm.add(repoPath, filePath)

    @staticmethod
    def commit(repoPath: str, message: str, author: str):
        return pyscm.commit(repoPath, message, author)

    @staticmethod
    def checkout(repoPath: str, commitHash: str):
        return pyscm.checkout(repoPath, commitHash)

    @staticmethod
    def negotiate(repoPath: str, requestedCommitId: str):
        return pyscm.negotiate(repoPath, requestedCommitId)