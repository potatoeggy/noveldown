import noveldown

a = noveldown.query("WanderingInn")
b = a.chapters[0]
noveldown.download(a, end=5)
