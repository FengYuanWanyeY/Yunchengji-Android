[app]

title = 云成绩查询
package.name = yunchengji
package.domain = org.yunchengji

source.include_exts = py,png,jpg,kv,atlas,json,txt
source.dir = .

version = 1.0.0

requirements = python3,kivy,requests,openpyxl,pyjnius

presplash.filename = assets/presplash.png
icon.filename = assets/icon.png

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 30
android.ndk = 25b
android.minapi = 21
android.build_tools = 36.1

android.archs = arm64-v8a,armeabi-v7a

[buildozer]

log_level = 2

warn_on_root = 1
