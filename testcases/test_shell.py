import os

ADB_SHELL_PATH =  'E://adb//test.sh'

def gen_adbShell(args):
    print(args)
    sh = open(ADB_SHELL_PATH,'w')
    sh.write("#! /bin/bash\n")
    sh.write(" ".join(args))
    sh.close()


if __name__ == '__main__':
    args = [
        'am', 'instrument', '-w', '-r',
        '-e', 'debug', 'false',
        '-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
        '-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
        '-e', 'collector_file', 'test.log',
        '-e', 'runner_config', 'CgRUSi0xEipSVU4tQS04ZmViOWZhMy03MWNlLTQxOTUtYTdjYy1jNTU2MDExY2NiODAaYQosSjZJUGxrNUFFVSsyL1lpNTlyZlluc0ZRdGR0T2dBbzlHQXp5c3g4Y2lPTT0SLFZWVzBGbm83QkVadDFhL3k2S0xNMzZ1ajlxY2p3N0NBSER3V1pLRGxXRHM9IgMKATIiIwoIQUhMSVNUXzEYAyIVeyJwYXJhbSI6ICIwLDEyLDIsMSJ9IiMKCEFITElTVF8yGAMiFXsicGFyYW0iOiAiMCwxMiwyLDEifSImCg1EUkxJTktRVU9URV8xGAMiE3siY29kZSI6ICJIVFNDLnVrIn0iNwoNRFJRVU9URUxJU1RfMRgDIiR7ImNvZGUiOiAiZ2RyIiwgInBhcmFtIjogIjAsMTAsMywxIn0iJAoJT0hMQ1NVQl8xGAMiFXsiY29kZSI6ICI2MDAwMDAuc2gifSIzCgpPSExDVEVTVF8xGAMiI3sic3RrIjogIjA2ODg2LmhrIiwgInR5cGUiOiAiZGF5ayJ9Ij8KCk9ITENURVNUXzIYAyIveyJzdGsiOiAiMDY4ODYuaGsiLCAidHlwZSI6ICJkYXlrIiwgInN1YiI6ICIxIn0iIgoJVUtRVU9URV8xGAMiE3siY29kZSI6ICJIVFNDLnVrIn0iQgoQQkFOS1VBSVNPUlRJTkdfMRgDIix7InN5bWJvbCI6ICJOb3Rpb24iLCAicGFyYW0xIjogIjAsMTIsaHNsLDAifSJCChBCQU5LVUFJU09SVElOR18yGAMiLHsic3ltYm9sIjogIk5vdGlvbiIsICJwYXJhbTEiOiAiMCwxMixoc2wsMCJ9IkUKEVBMQVRFSU5ERVhRVU9URV8xGAMiFnsiQ09ERVMiOiAiQTIwMDEwLmJrIn0iFnsiQ09ERVMiOiAiQTIwMDEwLmJrIn0iRQoRUExBVEVJTkRFWFFVT1RFXzIYAyIueyJDT0RFUyI6ICJBMjAwMTAuYmsiLCAiQ09TVE9NRklMRURTIjogIm51bGwifSIvChRTVUJORVdTVE9DS1JBTktJTkdfMRgDIhV7InBhcmFtIjogIjAsMTAsMywxIn0iMwoYU1VCTkVXQk9ORFNUT0NLUkFOS0lOR18xGAMiFXsicGFyYW0iOiAiMCwxMCwzLDEifSI4CgtNT1JFUFJJQ0VfMRgDIid7ImNvZGUiOiAiMDY4ODYuaGsiLCAic3VidHlwZSI6ICIxMDAxIn0iJwoLTU9SRVBSSUNFXzIYAyIWeyJjb2RlIjogIklDMTkxMC5jZmYifSJLCgZUSUNLXzEYAyI/eyJDT0RFUyI6ICI2MDAwMDAuc2giLCAiUEFHRVMiOiAiMCwxMDAsLTEiLCAiU1VCVFlQRVMiOiAiMTAwMSJ9IjoKDUhLU1RPQ0tJTkZPXzEYAyIneyJjb2RlIjogIjAwMDA1LmhrIiwgInN1YnR5cGUiOiAiMTAwMSJ9ImgKDkJBTktVQUlRVU9URV8xGAMiKHsiY29kZSI6ICI2MDA0MjUuc2giLCAicGFyYW1zIjogIlRyYWRlIn0iKnsiY29kZSI6ICJzd182MDA0MjUuc2giLCAicGFyYW1zIjogIm51bGwifQ==',
        'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
    ]
    gen_adbShell(args)