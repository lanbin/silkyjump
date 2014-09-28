import sublime, sublime_plugin, re

class SelPathCommand(sublime_plugin.EventListener):
	def __init__(self):
		self.root = ""
		self.selNum = 0
	
	def on_load(self, view):
		filename = view.file_name()
		self.root = re.match(r"(.*)template\/",filename).group()

	def on_selection_modified(self, view):
		rs = view.sel()[0]
		if rs.size() > 0:
			selectTxt = view.substr(rs)
			matches = re.search(r"(\s*)\{\{(!)?[partial|loop](.*)\}\}\n", selectTxt.encode("ascii", "ignore"))
			if matches:
				# duplicate click
				self.selNum += 1
				if self.selNum == 2:
					self.selNum = 0
					# change unicode to string
					partial = matches.group().encode("ascii", "ignore")
					# left
					filepath = re.compile("(.*)\{\{").sub('', partial)
					# right
					filepath = re.compile("\}\}\n").sub('', filepath)
					# split by space
					filepath = filepath.split(" ")[1].replace("\"","").replace("\'", "")
					# open the file
					view.window().open_file(self.root + filepath + ".hbs")
					# set the status
					sublime.status_message("opened: " + self.root + filepath + ".hbs" + " success")



