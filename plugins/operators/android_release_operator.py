from airflow.utils.decorators import apply_defaults

from operators.release_ci_operator import ReleaseCIOperator

class AndroidReleaseOperator(ReleaseCIOperator):
    @apply_defaults
    def __init__(self, repo_name, tag_id, tag_sha, runner_conf, release_xcom_key='android_release',*args, **kwargs):
        super(AndroidReleaseOperator, self).__init__(
            repo_name=repo_name,
            tag_id=tag_id,
            tag_sha=tag_sha,
            queue='android',
            runner_conf=runner_conf,
            release_xcom_key=release_xcom_key,
            *args,
            **kwargs
        )
        self.remote_path = '/release/Android/%s/' % (tag_id)

    def verify_release(self, release_files):
        if release_files is None or len(release_files) < 2:
            return False

        # TODO: type check and md5 check
        expected_type='application/vnd.android.package-archive'
        expected_names=['app-debug.apk', 'app-debug-androidTest.apk']

        for file in release_files:
            if file.type == expected_type and file.name in expected_names:
                expected_names.remove(file.name)

        return len(expected_names) == 0

    def verify_directory(self, files):
        if files is None or len(files) != 3:
            return False

        expected_names=['app-debug.apk', 'app-debug-androidTest.apk', 'md5sum.txt']
        files.sort()
        expected_names.sort()

        return files == expected_names



if __name__ == '__main__':
    android_release = AndroidReleaseOperator(
        task_id='android_release1',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20191229-0.0.1',
        tag_sha='bc809c40b8a24566f02a77182ea702093da89521',
        runner_conf='fake_runner_conf'
    )
    android_release.execute("")