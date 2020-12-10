Data = {}

str = '#login kevin yobeth'
uid = 'adfakljsdf3'

str = str.split()

Data[uid] = {
    'un': str[1],
    'ps': str[2]
}

str2 = '#login aa bb'
uid2 = 'kllkkll'

Data[uid2] = {
    'un': str2[1],
    'ps': str2[2]
}

print(Data[uid])
