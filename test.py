import noveldown

a = noveldown.query("WanderingInn")
b = a.chapters[0]
print(a.chapters[3].content)
noveldown.download(a, end=5)
