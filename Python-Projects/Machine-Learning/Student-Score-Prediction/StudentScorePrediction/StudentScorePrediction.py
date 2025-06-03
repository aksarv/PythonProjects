import pandas
from sklearn.neighbors import KNeighborsRegressor

student_file = pandas.read_csv('student-mat.csv', sep=';')

data = []
labels = []

for i in range(0, len(student_file['absences'])-20):
    data.append([student_file['absences'][i], student_file['failures'][i], student_file['studytime'][i], student_file['age'][i], student_file['G1'][i], student_file['G2'][i]])
    labels.append(student_file['G3'][i])

model = KNeighborsRegressor(15)

model.fit(data, labels)

i = int(input('Enter row to test (1-20):'))

i += 374

prediction = model.predict([[student_file['absences'][i], student_file['failures'][i], student_file['studytime'][i], student_file['age'][i], student_file['G1'][i], student_file['G2'][i]]])

print(f'The student grade for index {i} is {str(prediction[0])}')
print('Calculated from the following input data:')
print(f"{[student_file['absences'][i], student_file['failures'][i], student_file['studytime'][i], student_file['age'][i], student_file['G1'][i], student_file['G2'][i]]} and {student_file['G3'][i]} is the actual grade")


