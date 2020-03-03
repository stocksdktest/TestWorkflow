from airflow.utils.decorators import apply_defaults

from operators.release_ci_operator import ReleaseCIOperator

class IOSReleaseOperator(ReleaseCIOperator):
    @apply_defaults
    def __init__(self, repo_name, tag_id, tag_sha, runner_conf, release_xcom_key='ios_release',*args, **kwargs):
        super(IOSReleaseOperator, self).__init__(
            repo_name=repo_name,
            tag_id=tag_id,
            tag_sha=tag_sha,
            queue='osx',
            runner_conf=runner_conf,
            release_xcom_key=release_xcom_key,
            *args,
            **kwargs
        )
        self.remote_path = '/release/iOS/%s/' % (tag_id)
        print('remote_path', self.remote_path)

    def verify_release(self, release_files):
        if release_files is None or len(release_files) < 1:
            return False

        return True

        # TODO: type check and md5 check
        expected_type='application/vnd.android.package-archive'
        expected_names=['IOSTestRunner.app.zip']

        for file in release_files:
            if file.type == expected_type and file.name in expected_names:
                expected_names.remove(file.name)

        return len(expected_names) == 0

    def verify_directory(self, files):
        if files is None or len(files) != 2:
            return False

        expected_names=['IOSTestRunner.app.zip', 'md5sum.txt']
        files.sort()
        expected_names.sort()

        return files == expected_names

if __name__ == '__main__':
    android_release = IOSReleaseOperator(
        task_id='ios_release1',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id='release-20191227-0.0.1',
        tag_sha='9d4a42d53a201684c3c873e90fbd3f67240447b9',
        runner_conf='fake_runner_conf'
    )
    android_release.execute("")