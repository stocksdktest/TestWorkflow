from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator
from hooks.github_hook import GithubHook
from utils import download_file

class ReleaseFile(object):
    def __init__(self, git_release_asset=None):
        if not git_release_asset:
            return
        self.name = git_release_asset.name
        self.type = git_release_asset.content_type
        self.url = git_release_asset.browser_download_url
        self.md5sum = None

    def __str__(self):
        return 'ReleaseFile(name=%s, type=%s, url=%s, md5=%s)' % (self.name, self.type, self.url, self.md5sum)

    def __repr__(self):
        return self.__str__()

class ReleaseCIOperator(StockOperator):
    @apply_defaults
    def __init__(self, repo_name, tag_id, tag_sha, release_xcom_key, queue, runner_conf, *args, **kwargs):
        super(ReleaseCIOperator, self).__init__(queue=queue, runner_conf=runner_conf, *args, **kwargs)
        self.repo_name = repo_name
        self.tag_id = tag_id
        self.tag_sha = tag_sha
        self.release_xcom_key = release_xcom_key

    def verify_release(self, release_files):
        """
        :param release_files
        :type release_files: list(ReleaseFile)
        """
        raise NotImplementedError()

    def execute(self, context):
        github_client = GithubHook(conn_id=self.repo_name)
        repo = github_client.get_repo(self.repo_name)
        if repo is None:
            raise AirflowException('repo %s not found' % self.repo_name)

        if not github_client.check_release_sha(repo, self.tag_id, self.tag_sha):
            raise AirflowException('tag %s sha %s not match' % (self.tag_id, self.tag_sha))

        release_assets = github_client.get_release_assets(repo, self.tag_id)
        asset_checksum = dict()
        for asset_item in release_assets:
            if asset_item.name != 'md5sum.txt':
                continue
            path = '/tmp/%s/md5sum.txt' % self.tag_sha
            download_file(url=asset_item.browser_download_url, file_path=path)
            with open(path) as checksum_file:
                for line in checksum_file.readlines():
                    if not line or len(line) == 0:
                        continue
                    name = line.split("/")[-1].strip()
                    checksum = line.split()[0]
                    asset_checksum[name] = checksum

        release_files = []
        for asset_item in release_assets:
            if asset_item.name == 'md5sum.txt':
                continue
            release_file = ReleaseFile(asset_item)
            release_file.md5sum = asset_checksum.get(release_file.name, None)
            release_files.append(release_file)

        if not self.verify_release(release_files):
            raise AirflowException('release files not verify: %s' % release_files)

        self.xcom_push(context, key=self.release_xcom_key, value=release_files)
