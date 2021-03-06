from .base import base64_encode, base64_decode, test_base64_str, generate_id, download_file, bytes_to_dict, \
    command_to_script, LogChunkCache
from .adb import start_adb_server, scan_local_device, connect_to_device, exec_adb_cmd, spawn_logcat, \
    parse_logcat, get_app_version
from .ios import spawn_xcrun_log, parse_sim_log, config_plist, xctest_cmd