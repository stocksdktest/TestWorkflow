# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='config.proto',
  package='stock_testing',
  syntax='proto3',
  serialized_options=_b('\n\026com.chi.ssetest.protosB\013SetupConfig'),
  serialized_pb=_b('\n\x0c\x63onfig.proto\x12\rstock_testing\"\xb0\x01\n\x10MarketPermission\x12\r\n\x05Level\x18\x01 \x01(\t\x12\x10\n\x08\x43\x66\x66Level\x18\x02 \x01(\t\x12\x10\n\x08\x44\x63\x65Level\x18\x03 \x01(\t\x12\x11\n\tCzceLevel\x18\x04 \x01(\t\x12\x0f\n\x07\x46\x65Level\x18\x05 \x01(\t\x12\x0f\n\x07GILevel\x18\x06 \x01(\t\x12\x11\n\tShfeLevel\x18\x07 \x01(\t\x12\x10\n\x08IneLevel\x18\x08 \x01(\t\x12\x0f\n\x07HKPerms\x18\t \x03(\t\"\x13\n\x04Site\x12\x0b\n\x03ips\x18\x01 \x03(\t\"\xf3\x01\n\tSDKConfig\x12\x15\n\rappKeyAndroid\x18\x01 \x01(\t\x12\x11\n\tappKeyIOS\x18\x02 \x01(\t\x12>\n\x0bserverSites\x18\x03 \x03(\x0b\x32).stock_testing.SDKConfig.ServerSitesEntry\x12\x33\n\nmarketPerm\x18\x04 \x01(\x0b\x32\x1f.stock_testing.MarketPermission\x1aG\n\x10ServerSitesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.stock_testing.Site:\x02\x38\x01\"m\n\x0eTestcaseConfig\x12\x12\n\ntestcaseID\x18\x01 \x01(\t\x12\x1a\n\x12\x63ontinueWhenFailed\x18\x02 \x01(\x08\x12\x18\n\x10roundIntervalSec\x18\x03 \x01(\x03\x12\x11\n\tparamStrs\x18\x04 \x03(\t\"G\n\x0bStoreConfig\x12\x10\n\x08mongoUri\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x62Name\x18\x02 \x01(\t\x12\x16\n\x0e\x63ollectionName\x18\x03 \x01(\t\"\xc1\x01\n\x0cRunnerConfig\x12\r\n\x05jobID\x18\x01 \x01(\t\x12\x10\n\x08runnerID\x18\x02 \x01(\t\x12+\n\tsdkConfig\x18\x03 \x01(\x0b\x32\x18.stock_testing.SDKConfig\x12\x32\n\x0b\x63\x61sesConfig\x18\x04 \x03(\x0b\x32\x1d.stock_testing.TestcaseConfig\x12/\n\x0bstoreConfig\x18\x05 \x01(\x0b\x32\x1a.stock_testing.StoreConfigB%\n\x16\x63om.chi.ssetest.protosB\x0bSetupConfigb\x06proto3')
)




_MARKETPERMISSION = _descriptor.Descriptor(
  name='MarketPermission',
  full_name='stock_testing.MarketPermission',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Level', full_name='stock_testing.MarketPermission.Level', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='CffLevel', full_name='stock_testing.MarketPermission.CffLevel', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='DceLevel', full_name='stock_testing.MarketPermission.DceLevel', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='CzceLevel', full_name='stock_testing.MarketPermission.CzceLevel', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='FeLevel', full_name='stock_testing.MarketPermission.FeLevel', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='GILevel', full_name='stock_testing.MarketPermission.GILevel', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ShfeLevel', full_name='stock_testing.MarketPermission.ShfeLevel', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='IneLevel', full_name='stock_testing.MarketPermission.IneLevel', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='HKPerms', full_name='stock_testing.MarketPermission.HKPerms', index=8,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=208,
)


_SITE = _descriptor.Descriptor(
  name='Site',
  full_name='stock_testing.Site',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ips', full_name='stock_testing.Site.ips', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=210,
  serialized_end=229,
)


_SDKCONFIG_SERVERSITESENTRY = _descriptor.Descriptor(
  name='ServerSitesEntry',
  full_name='stock_testing.SDKConfig.ServerSitesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='stock_testing.SDKConfig.ServerSitesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='stock_testing.SDKConfig.ServerSitesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=404,
  serialized_end=475,
)

_SDKCONFIG = _descriptor.Descriptor(
  name='SDKConfig',
  full_name='stock_testing.SDKConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='appKeyAndroid', full_name='stock_testing.SDKConfig.appKeyAndroid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='appKeyIOS', full_name='stock_testing.SDKConfig.appKeyIOS', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serverSites', full_name='stock_testing.SDKConfig.serverSites', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='marketPerm', full_name='stock_testing.SDKConfig.marketPerm', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SDKCONFIG_SERVERSITESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=232,
  serialized_end=475,
)


_TESTCASECONFIG = _descriptor.Descriptor(
  name='TestcaseConfig',
  full_name='stock_testing.TestcaseConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='testcaseID', full_name='stock_testing.TestcaseConfig.testcaseID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='continueWhenFailed', full_name='stock_testing.TestcaseConfig.continueWhenFailed', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='roundIntervalSec', full_name='stock_testing.TestcaseConfig.roundIntervalSec', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='paramStrs', full_name='stock_testing.TestcaseConfig.paramStrs', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=477,
  serialized_end=586,
)


_STORECONFIG = _descriptor.Descriptor(
  name='StoreConfig',
  full_name='stock_testing.StoreConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mongoUri', full_name='stock_testing.StoreConfig.mongoUri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dbName', full_name='stock_testing.StoreConfig.dbName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collectionName', full_name='stock_testing.StoreConfig.collectionName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=588,
  serialized_end=659,
)


_RUNNERCONFIG = _descriptor.Descriptor(
  name='RunnerConfig',
  full_name='stock_testing.RunnerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobID', full_name='stock_testing.RunnerConfig.jobID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='runnerID', full_name='stock_testing.RunnerConfig.runnerID', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sdkConfig', full_name='stock_testing.RunnerConfig.sdkConfig', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='casesConfig', full_name='stock_testing.RunnerConfig.casesConfig', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='storeConfig', full_name='stock_testing.RunnerConfig.storeConfig', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=662,
  serialized_end=855,
)

_SDKCONFIG_SERVERSITESENTRY.fields_by_name['value'].message_type = _SITE
_SDKCONFIG_SERVERSITESENTRY.containing_type = _SDKCONFIG
_SDKCONFIG.fields_by_name['serverSites'].message_type = _SDKCONFIG_SERVERSITESENTRY
_SDKCONFIG.fields_by_name['marketPerm'].message_type = _MARKETPERMISSION
_RUNNERCONFIG.fields_by_name['sdkConfig'].message_type = _SDKCONFIG
_RUNNERCONFIG.fields_by_name['casesConfig'].message_type = _TESTCASECONFIG
_RUNNERCONFIG.fields_by_name['storeConfig'].message_type = _STORECONFIG
DESCRIPTOR.message_types_by_name['MarketPermission'] = _MARKETPERMISSION
DESCRIPTOR.message_types_by_name['Site'] = _SITE
DESCRIPTOR.message_types_by_name['SDKConfig'] = _SDKCONFIG
DESCRIPTOR.message_types_by_name['TestcaseConfig'] = _TESTCASECONFIG
DESCRIPTOR.message_types_by_name['StoreConfig'] = _STORECONFIG
DESCRIPTOR.message_types_by_name['RunnerConfig'] = _RUNNERCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MarketPermission = _reflection.GeneratedProtocolMessageType('MarketPermission', (_message.Message,), dict(
  DESCRIPTOR = _MARKETPERMISSION,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:stock_testing.MarketPermission)
  ))
_sym_db.RegisterMessage(MarketPermission)

Site = _reflection.GeneratedProtocolMessageType('Site', (_message.Message,), dict(
  DESCRIPTOR = _SITE,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:stock_testing.Site)
  ))
_sym_db.RegisterMessage(Site)

SDKConfig = _reflection.GeneratedProtocolMessageType('SDKConfig', (_message.Message,), dict(

  ServerSitesEntry = _reflection.GeneratedProtocolMessageType('ServerSitesEntry', (_message.Message,), dict(
    DESCRIPTOR = _SDKCONFIG_SERVERSITESENTRY,
    __module__ = 'config_pb2'
    # @@protoc_insertion_point(class_scope:stock_testing.SDKConfig.ServerSitesEntry)
    ))
  ,
  DESCRIPTOR = _SDKCONFIG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:stock_testing.SDKConfig)
  ))
_sym_db.RegisterMessage(SDKConfig)
_sym_db.RegisterMessage(SDKConfig.ServerSitesEntry)

TestcaseConfig = _reflection.GeneratedProtocolMessageType('TestcaseConfig', (_message.Message,), dict(
  DESCRIPTOR = _TESTCASECONFIG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:stock_testing.TestcaseConfig)
  ))
_sym_db.RegisterMessage(TestcaseConfig)

StoreConfig = _reflection.GeneratedProtocolMessageType('StoreConfig', (_message.Message,), dict(
  DESCRIPTOR = _STORECONFIG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:stock_testing.StoreConfig)
  ))
_sym_db.RegisterMessage(StoreConfig)

RunnerConfig = _reflection.GeneratedProtocolMessageType('RunnerConfig', (_message.Message,), dict(
  DESCRIPTOR = _RUNNERCONFIG,
  __module__ = 'config_pb2'
  # @@protoc_insertion_point(class_scope:stock_testing.RunnerConfig)
  ))
_sym_db.RegisterMessage(RunnerConfig)


DESCRIPTOR._options = None
_SDKCONFIG_SERVERSITESENTRY._options = None
# @@protoc_insertion_point(module_scope)
