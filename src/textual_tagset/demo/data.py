from random import choice

selected = (
    "Liberty Baxter, Nevada Bray, Tasha Quinn, Teegan Mays, Omar Hendrix, "
    "Shelley Frost, Hyatt Serrano, Mariko Tyler, Grant Hernandez, Kiara Bolton, "
    "Lucy Hahn, Vladimir Mcmillan, Alvin Byrd, Melanie Coleman, Edan Brady, "
    "John Hahn, Wyatt Gross, Lionel Knapp, Montana Hoover, Ursa Kiddv, "
    "Cheyenne Elliott, Nathan Dixon, Jayme Witt, Patricia Barrett, Christen Zimmerman, "
    "Lesley Booth, Victoria Salinas, Philip Walls, Pearl Martin, Garrett Guzman, "
    "Brady Decker, Ebony Sampson, Fletcher Ellis, Stewart Crawford, Graiden Mcdowell"
).split(", ")

deselected = (
    "Isaiah Larson, Owen Leach, Carter Bowman, Cyrus Pruitt, Bernard Talley, "
    "Angelica Yates, Garth Bates, Noble Garcia, Florence Pugh, Benedict Glass, "
    "Logan Kline, Blythe Perkins, Keith Leach, Lisandra Barnes, Baxter Bruce, "
    "Alfreda Vega, Alana Reyes, Nelle Sosa, Acton Ortiz, Yoshi Wilson, "
    "Emi Rice, Kalia Washington, Channing Huber, Martina Dyer, Leilani Alford, "
    "Tucker Phillips, Belle Dodson, Vance Robertson, Conan Weaver, Felicia Huber, "
    "Kyra Oneil, Shaine Wise, Jamal Finch, Roary Noble, Rafael Stewart"
).split(", ")

firstnames = list(set(item.split()[0] for item in selected+deselected if item.split()[0]))
lastnames = list(set(item.split()[1] for item in  selected+deselected if item.split()[1]))

def random_name():
    return f"{choice(firstnames)} {choice(lastnames)}"

def random_names(n):
    names = set()
    while len(names) < n:
        names.add(random_name())
    return names