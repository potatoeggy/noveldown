import noveldown

print(noveldown.get_available_ids())
print(noveldown.query("TheWanderingInn"))
noveldown.download("TheWanderingInn")
