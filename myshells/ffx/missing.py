def missing(name, pre_existing, limit = 255):
    m = round((limit - pre_existing * 4) / 4) - 1
    return f"{name}: {m}"

master4 = {
    "Potesferafisica": 22,
    "Potesferamagica": 21,
    "Difesferafisica": 10,
    "Difesferamagica": 17,
    "Rapidosfera" : 18,
    "Fortunosfera": 1,
    "Mirasfera": 4,
    "Destrosfera": 19
}

for name, value in master4.items():
    print(missing(name, value, 128 if name == "Fortunosfera" else 255))
