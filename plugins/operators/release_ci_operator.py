from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator
from hooks.github_hook import GithubHook
from airflow.contrib.hooks.ftp_hook import FTPHook
from ftplib import error_perm
from utils import *

import os
import hashlib
# TODO: 试着去获得filetype
FILE_TYPE_FAKE = 'application/vnd.android.package-archive'

class ReleaseFile(object):
    def __init__(self, name, type, filepath):
        if not name:
            return
        self.name = name
        self.type = type
        self.filepath = filepath
        self.md5sum = None

    def __str__(self):
        return 'ReleaseFile(name=%s, type=%s, url=%s, md5=%s)' % (self.name, self.type, self.filepath, self.md5sum)

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
        self.remote_path = ''
        self.local_path = '/tmp/%s/' % self.tag_sha

        os.makedirs(os.path.dirname(self.local_path), exist_ok=True)

    def verify_release(self, release_files):
        """
        :param release_files
        :type release_files: list(ReleaseFile)
        """
        raise NotImplementedError()

    def verify_directory(self, files):
        """
        :param files:
        :type: files: list(str)
        """
        raise NotImplementedError()

    def execute(self, context):
        github_client = GithubHook(conn_id=self.repo_name)
        repo = github_client.get_repo(self.repo_name)
        ftp_client = FTPHook(ftp_conn_id='ftp_default')
        conn = ftp_client.get_conn()

        if repo is None:
            raise AirflowException('repo %s not found' % self.repo_name)

        if not github_client.check_release_sha(repo, self.tag_id, self.tag_sha):
            raise AirflowException('tag %s sha %s not match' % (self.tag_id, self.tag_sha))

        try:
            release_assets = ftp_client.list_directory(self.remote_path)
        except error_perm as e:
            raise AirflowException('Directory %s not exsit in ftp server' % (self.remote_path))

        if not self.verify_directory(release_assets):
            raise AirflowException('release files not verify: %s' % release_assets)

        print(release_assets)
        asset_checksum = dict()

        for filename in release_assets:
            if filename != 'md5sum.txt':
                continue
            filepath = self.local_path + filename
            downloader = FTP_Downloader()
            downloader.download(remote_path=self.remote_path + 'md5sum.txt', local_path=filepath)

            with open(filepath) as checksum_file:
                for line in checksum_file.readlines():
                    if not line or len(line) == 0:
                        continue
                    name = line.split("/")[-1].strip()
                    checksum = line.split()[0]
                    asset_checksum[name] = checksum

        release_files = []
        for filename in release_assets:
            if filename == 'md5sum.txt':
                continue
            filepath = self.remote_path + filename
            release_file = ReleaseFile(name=filename, type=FILE_TYPE_FAKE, filepath=filepath)
            release_file.md5sum = asset_checksum.get(filename, None)
            release_files.append(release_file)

        if not self.verify_release(release_files):
            raise AirflowException('release files not verify: %s' % release_files)

        # print('release_files',release_files)
        import pprint
        pprint.pprint(release_files)

        # TODO: ANNOTATE
        self.xcom_push(context, key=self.release_xcom_key, value=release_files)
        # for file in release_files:
        #     path = '/tmp/%s/%s' % (file.md5sum, file.name)
        #     download_file(url=file.filepath, file_path=path, md5=file.md5sum)
        # conn.close()