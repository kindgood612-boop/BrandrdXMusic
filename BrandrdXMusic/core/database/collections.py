# هذا الملف يحتوي على تعريفات قواعد البيانات والمتغيرات الموجودة في الذاكرة (Cache)
from BrandrdXMusic.core.mongo import mongodb, pymongodb

# Database Collections
authdb = mongodb.adminauth
authuserdb = mongodb.authuser
autoenddb = mongodb.autoend
assdb = mongodb.assistants
blacklist_chatdb = mongodb.blacklistChat
blockeddb = mongodb.blockedusers
chatsdb = mongodb.chats
chattopdb = mongodb.chattopdb
channeldb = mongodb.cplaymode
countdb = mongodb.upcount
gbansdb = mongodb.gban
langdb = mongodb.language
onoffdb = mongodb.onoffper
playmodedb = mongodb.playmode
playtypedb = mongodb.playtypedb
skipdb = mongodb.skipmode
sudoersdb = mongodb.sudoers
usersdb = mongodb.tgusersdb
privatedb = mongodb.privatechats
suggdb = mongodb.suggestion
cleandb = mongodb.cleanmode
queriesdb = mongodb.queries
userdb = mongodb.userstats
videodb = mongodb.vipvideocalls
chatsdbc = mongodb.chatsc  # for clone
usersdbc = mongodb.tgusersdbc  # for clone

# Memory Cache variables
active = []
activevideo = []
assistantdict = {}
autoend = {}
count = {}
channelconnect = {}
langm = {}
loop = {}
maintenance = []
nonadmin = {}
pause = {}
playmode = {}
playtype = {}
skipmode = {}
privatechats = {}
cleanmode = []
suggestion = {}
mute = {}
audio = {}
video = {}
