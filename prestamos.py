import csv


def prestamos_activos (user):
    prestamos = []
    with open('bd_prestamos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6 and row[2] == user and row[5] == 'activo':
                prestamos.append(row)
    return prestamos


    
