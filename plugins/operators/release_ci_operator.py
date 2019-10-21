from github import Github

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator
from hooks.github_hook import GithubHook

class ReleaseFile(object):
    def __init__(self, git_release_asset):
        self.name = git_release_asset.name
        self.type = git_release_asset
        self.url = git_release_asset.browser_download_url

class AndroidCIOperator(StockOperator):
    @apply_defaults
    def __init__(self, tag_id, tag_sha, runner_conf, *args, **kwargs):
        super(AndroidCIOperator, self).__init__(queue='android', runner_conf=runner_conf, *args, **kwargs)
        self.tag_id = tag_id
        self.tag_sha = tag_sha

    def verify_release(self, context):
        """
        This is the main method to derive when creating an operator.
        Context is the same dictionary used as when rendering jinja templates.

        Refer to get_template_context for more context.
        """
        raise NotImplementedError()

    def execute(self, context):
        github_client = GithubHook(conn_id='sdktest')

